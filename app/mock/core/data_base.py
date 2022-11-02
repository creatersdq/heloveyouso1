from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from app.core.conf import setting
from contextlib import contextmanager

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/cn_ud_quality_autotest".format(setting()['DATABASE_USERNAME'],
                                                                                   setting()['DATABASE_PASSWORD'],
                                                                                   setting()['DATABASE_HOST'],
                                                                                   setting()['DATABASE_PORT']),
                       pool_recycle=3600, pool_pre_ping=True, echo=False)

Base = declarative_base()

SessionType = scoped_session(sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=False))


@contextmanager
def session_maker():
    s = SessionType()

    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()
