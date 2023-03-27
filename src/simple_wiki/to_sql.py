import json
from xml.etree import ElementTree as ET

import requests
from ..sql import engine
from ..sql.models import SimpleWikiEntry
from tqdm import tqdm
from sqlalchemy.orm import Session
from ..util import dump_to_file


def _exists(id):
    with Session(engine) as session:
        return session.query(SimpleWikiEntry).filter_by(id=id).first() is not None


def _save_wiki(id, title, text, text_clean, session: Session = None):
    if not id or not title or not text or not text_clean:
        return
    entry = SimpleWikiEntry(
        id=id, title=title, text=text, text_clean=text_clean)
    session.add(entry)


def get_clean_text(text):
    try:
        content = requests.post(
            "http://localhost:6000/clean",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"text": text})
        ).content
        l = json.loads(content)
        return l["text"]
    except:
        return ""


def load_simple_wiki_sql():
    p = "data/simple_wiki/page-articles.xml"
    page_tag = "{http://www.mediawiki.org/xml/export-0.10/}page"
    id_tag = "{http://www.mediawiki.org/xml/export-0.10/}id"
    title_tag = "{http://www.mediawiki.org/xml/export-0.10/}title"
    text_tag = "{http://www.mediawiki.org/xml/export-0.10/}revision/{http://www.mediawiki.org/xml/export-0.10/}text"
    tree = ET.parse(p)
    root = tree.getroot()
    pages = root.findall(page_tag)
    with Session(engine) as session:
        for page in tqdm(pages):
            id = page.find(id_tag).text
            title = page.find(title_tag).text
            text = page.find(text_tag).text
            text_clean = get_clean_text(text)
            if not _exists(id):
                _save_wiki(id, title, text, text_clean, session=session)
        session.commit()
