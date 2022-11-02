from pydantic import BaseModel


class RunCase(BaseModel):
    project: str
    ifCelery: int = None  # 是否开启celery队列
