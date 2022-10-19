from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.model import Base


def get_db_connect():
    engine = create_engine('postgresql+psycopg2://admin:root@127.0.0.1/db_cafe', future=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    return session


if __name__ == "__main__":
    get_db_connect()
