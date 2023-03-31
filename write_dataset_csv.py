import csv
from src.sql import engine
from src.sql.models import ClassifierDataset
from sqlalchemy.orm.session import Session
import random


def main():
    train_rows = []
    test_rows = []
    train_csv_path = "data/dataset_train.csv"
    test_csv_path = "data/dataset_test.csv"
    with Session(engine) as session:
        q = session.query(ClassifierDataset)
        train_rows_standard = []
        train_rows_simple = []

        for item in q:
            row = [item.id, item.level, item.text]
            if item.partition == "train":
                if item.level == "simple":
                    train_rows_simple.append(row)
                elif item.level == "standard":
                    train_rows_standard.append(row)
            else:
                test_rows.append(row)

        random.shuffle(train_rows_standard)
        train_rows.extend(train_rows_simple)
        train_rows.extend(train_rows_standard[:len(train_rows_simple)])

    with open(train_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(train_rows)
    with open(test_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(test_rows)


if __name__ == '__main__':
    main()
