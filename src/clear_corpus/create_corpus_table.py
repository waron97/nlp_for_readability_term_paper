from ..sql.models import ClearCorpusEntry
from ..sql.engine import engine
from sqlalchemy import exists, insert, select
from sqlalchemy.orm import Session
import csv


def create_corpus_table():
    with open("data/clear_corpus.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        h = next(reader)
        with Session(engine) as session:
            for row in reader:
                (
                    row_id,
                    last_changed,
                    author,
                    title,
                    anthology,
                    url,
                    source,
                    pub_year,
                    category,
                    location,
                    license,
                    mpa_max,
                    mpa_max_int,
                    mpa_avg,
                    excerpt,
                    google_wc,
                    joon,
                    british_wc,
                    british_words,
                    sentence_count,
                    sentence_count_v2,
                    paragraphs,
                    bt,
                    bt_se,
                    fk,
                    fk_grade,
                    ari,
                    smog,
                    ndc,
                    carec,
                    carec_m,
                    cares,
                    cml2ri,
                    *_
                ) = row

                if session.query(exists().where(ClearCorpusEntry.id == row_id)).scalar():
                    continue

                entry = ClearCorpusEntry(
                    id=row_id,
                    last_changed=last_changed,
                    author=author,
                    title=title,
                    anthology=anthology,
                    url=url,
                    source=source,
                    pub_year=pub_year,
                    category=category,
                    location=location,
                    license=license,
                    mpaa_max=mpa_max,
                    mpaa_max_int=mpa_max_int,
                    mpaa_avg=mpa_avg,
                    excerpt=excerpt,
                    google_wc=google_wc,
                    sentence_count=sentence_count,
                    paragraphs=paragraphs,
                    bt=bt,
                    se=bt_se,
                    fk=fk,
                    fk_grade=fk_grade,
                    ari=ari,
                    smog=smog,
                    ndc=ndc,
                    carec=carec,
                    carec_m=carec_m,
                    cml2ri=cml2ri,
                )

                session.add(entry)
            session.commit()
