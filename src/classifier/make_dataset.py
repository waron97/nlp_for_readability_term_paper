from src.sql.models import WikiArticle, ClassifierDataset
from src.sql import engine
import random
from tqdm import tqdm

from sqlalchemy.orm.session import Session


def _get_paragraphs(text: str):
    paragraphs = text.split("\n\n")
    paragraphs = [
        paragraph.strip() for paragraph in paragraphs
        if len(paragraph.split()) > 20
        and len(paragraph.split()) < 2000
        and "*" not in paragraph
        and "<" not in paragraph
        and ">" not in paragraph
        and "==" not in paragraph
        and "{" not in paragraph
        and "colspan=" not in paragraph
        and "style=" not in paragraph
    ]
    return paragraphs


def make_classifier_dataset():
    with Session(engine) as session:
        len_objects = session.query(ClassifierDataset).count()
        q = session.query(WikiArticle)
        for article in tqdm(q, total=len_objects):
            paragraphs_simple = _get_paragraphs(article.simple_text)
            paragraphs_standard = _get_paragraphs(article.standard_text)
            for p in paragraphs_simple:
                session.add(ClassifierDataset(
                    partition="train",
                    level="simple",
                    text=p,
                ))
            for p in paragraphs_standard:
                session.add(ClassifierDataset(
                    partition="train",
                    level="standard",
                    text=p,
                ))
        session.commit()

        # _ids = session.query(ClassifierDataset.id).all()

        # for _id in _ids:
        #     _id = _id[0]
        #     session.query(ClassifierDataset).filter(
        #         ClassifierDataset.id == _id).update({"partition": "train"})

        # session.commit()

        len_test = 20_000

        simple_ids = session.query(ClassifierDataset.id).filter(
            ClassifierDataset.level == "simple").all()
        standard_ids = session.query(ClassifierDataset.id).filter(
            ClassifierDataset.level == "standard").all()

        simple_ids = [id[0] for id in simple_ids]
        standard_ids = [id[0] for id in standard_ids]
        random.shuffle(simple_ids)
        random.shuffle(standard_ids)

        test_ids_simple = simple_ids[:len_test]
        test_ids_standard = standard_ids[:len_test]

        for _id in [*test_ids_simple, *test_ids_standard]:
            session.query(ClassifierDataset).filter(
                ClassifierDataset.id == _id).update({"partition": "test"})

        session.commit()
