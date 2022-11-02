from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from apps.core.conf import setting
from contextlib import contextmanager
from apps.extensions.logger import log

# from apps.core.timestamp_mixin import TimestampMixin


engine = create_engine("mysql+pymysql://{}:{}@{}:{}/cn_ud_quality_autotest".format(setting()['DATABASE_USERNAME'],
                                                                                   setting()['DATABASE_PASSWORD'],
                                                                                   setting()['DATABASE_HOST'],
                                                                                   setting()['DATABASE_PORT']),
                       pool_recycle=3400, pool_pre_ping=True)

Base = declarative_base()

SessionType = scoped_session(
    sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=False))


@contextmanager
def session_maker():
    s = SessionType()
    try:
        yield s
        s.commit()
    except Exception as e:
        log.get_log("Exception", "ERROR", e)
        s.rollback()
        raise
    finally:
        s.close()
