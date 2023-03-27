from ..sql import engine
from ..sql.models import DatasetEntry, DatasetWikiText
from sqlalchemy.orm import Session
from ..util import dump_to_file


def _get_simple_wiki_records(session: Session):
    rows = session.query(DatasetWikiText).all()
    return [
        {
            "topic": row.topic,
            "text": row.simple
        }
        for row in rows
    ]


def _get_standard_wiki_records(session: Session):
    rows = session.query(DatasetWikiText).all()
    return [
        {
            "topic": row.topic,
            "text": row.standard
        }
        for row in rows
    ]


def _get_dataset_records(session: Session):
    rows = session.query(DatasetEntry).all()
    return [
        {
            "topic": row.topic,
            "level": row.level,
            "text": row.text
        }
        for row in rows
    ]


def write_dataset():
    with Session(engine) as session:
        dataset_records = _get_dataset_records(session)
        simple_wiki_records = _get_simple_wiki_records(session)
        standard_wiki_records = _get_standard_wiki_records(session)
        payload = {
            "gpt_generation": dataset_records,
            "wikipedia": {
                "standard": standard_wiki_records,
                "simple": simple_wiki_records
            }
        }
        dump_to_file(payload, "data/dataset/dataset.json")
        for record in dataset_records:
            fname = f"data/dataset/text/{record['topic']}-{record['level']}.txt"
            dump_to_file(record["text"], fname, json=False)
        for record in simple_wiki_records:
            fname = f"data/dataset/text/wikisimple-{record['topic']}.txt"
            dump_to_file(record["text"], fname, json=False)
        for record in standard_wiki_records:
            fname = f"data/dataset/text/wikistandard-{record['topic']}.txt"
            dump_to_file(record["text"], fname, json=False)
