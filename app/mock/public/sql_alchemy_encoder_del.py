import json
from sqlalchemy.ext.declarative import DeclarativeMeta


# 解析处理类
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        使用自定义类将sqlalchemy对象转换成JSON字符串
        :param obj:
        :return:
        """
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)
