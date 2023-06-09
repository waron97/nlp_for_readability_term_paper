from typing import Optional

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .engine import engine


class Base(DeclarativeBase):
    pass


class ClearCorpusEntry(Base):
    __tablename__ = "clear_corpus"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_changed: Mapped[Optional[str]]
    author: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    anthology: Mapped[Optional[str]]
    url: Mapped[Optional[str]]
    source: Mapped[Optional[str]]
    pub_year: Mapped[Optional[int]]
    category: Mapped[Optional[str]]
    sub_category: Mapped[Optional[str]]
    category: Mapped[Optional[str]]
    location: Mapped[Optional[str]]
    license: Mapped[Optional[str]]
    mpaa_max: Mapped[Optional[str]]
    mpaa_max_int: Mapped[Optional[int]]
    mpaa_avg: Mapped[Optional[float]]
    excerpt: Mapped[Optional[str]]
    google_wc: Mapped[Optional[int]]
    sentence_count: Mapped[Optional[int]]
    paragraphs: Mapped[Optional[int]]
    bt: Mapped[Optional[float]]
    se: Mapped[Optional[float]]
    fk: Mapped[Optional[float]]
    fk_grade: Mapped[Optional[str]]
    ari: Mapped[Optional[float]]
    smog: Mapped[Optional[float]]
    ndc: Mapped[Optional[float]]
    carec: Mapped[Optional[float]]
    carec_m: Mapped[Optional[float]]
    cml2ri: Mapped[Optional[float]]


class ClassifierDataset(Base):
    __tablename__ = "classifier_dataset"

    id: Mapped[int] = mapped_column(primary_key=True)
    partition: Mapped[str]
    text: Mapped[str]
    level: Mapped[str]


class WikiArticle(Base):
    __tablename__ = "wiki_article"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    standard_text: Mapped[str]
    simple_text: Mapped[str]


class DatasetEntry(Base):
    __tablename__ = "dataset"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str]
    level: Mapped[str]
    topic: Mapped[str]
    text: Mapped[str]
    prompt: Mapped[str]


class SimpleWikiEntry(Base):
    __tablename__ = "simple_wiki"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    text: Mapped[str]
    text_clean: Mapped[Optional[str]]


class DatasetWikiText(Base):
    __tablename__ = "dataset_wiki_text"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str]
    simple: Mapped[str]
    standard: Mapped[str]


Base.metadata.create_all(engine)
