from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/data.db", echo=False)
