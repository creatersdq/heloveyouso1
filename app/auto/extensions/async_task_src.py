from abc import ABCMeta, abstractmethod  # (抽象方法)
from fastapi import background


class AsyncTask(metaclass=ABCMeta):
    def __int__(self):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class DoThreadPool(AsyncTask):
    def run(self):
        pass


class DoCelery(AsyncTask):
    def run(self):
        pass


class DoBackGround(AsyncTask):
    def run(self):
        print("DoBackGround")


def in_the_forest(do_type: any):
    do_type.run()
