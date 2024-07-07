from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

from sqlalchemy.orm import declarative_base


try:
    connect = os.environ.get("POSTGRES_URI")
    print(connect)
    engine = create_engine(connect)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    Base = declarative_base()

except Exception as e:
    raise Exception("Error Conexion DB", e)
