from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager


class DateBaseCommon(object):
    def __init__(
            self,
            DATABASE_NAME,
            DATABASE_USERNAME,
            DATABASE_PASSWORD,
            DATABASE_HOST,
            DATABASE_PORT
    ) -> any:
        """

        :param DATABASE_NAME:
        :param DATABASE_USERNAME:
        :param DATABASE_PASSWORD:
        :param DATABASE_HOST:
        :param DATABASE_PORT:
        """
        self.engine = create_engine(
            "mysql+pymysql://{}:{}@{}:{}/{}".format(
                DATABASE_USERNAME,
                DATABASE_PASSWORD,
                DATABASE_HOST,
                DATABASE_PORT,
                DATABASE_NAME
            ),
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=False
        )

        self.Base = declarative_base()
        self.SessionType = scoped_session(
            sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False
            )
        )

        self.s = self.SessionType()

    @contextmanager
    def session_maker(self):
        try:
            yield self.s
            self.s.commit()
        except:
            self.s.rollback()
            raise
        finally:
            self.s.close()
