from typing import List, Tuple, TypedDict


class Row(TypedDict):
    id: str
    word: str
    lemma: str
    pos: str
    tag: str
    head: str
    rel: str


class Dependencies:
    rows: List[Row]

    def __init__(self) -> None:
        self.rows = []

    def add_row(self, id, word, lemma, pos, tag, head, rel):
        self.rows.append({
            "id": id,
            "word": word,
            "lemma": lemma,
            "pos": pos,
            "tag": tag,
            "head": head,
            "rel": rel
        })

    def __repr__(self) -> str:
        lines = []
        for row in self.rows:
            lines.append("\t".join(row.values()))
        return "\n".join(lines)
