class UnifiedResHandle:
    instance = None

    def __init__(self):
        self.success_unified_res = {"errno": "0", "dataType": "OBJECT", "error": "", "data": []}
        self.error_unified_res = {"errno": "1", "dataType": "ERROR", "error": "", "data": []}

    # 单例模式，防止多次调用后，实例化重复的__init__对象
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def with_success(self, msg):
        if msg is None:
            return self.success_unified_res
        else:
            if type(msg) is list:
                try:
                    # 根据字典第一个KEY 进行升序
                    msg.sort(key=lambda elem: elem['{}'.format(elem.keys()[0])])
                    self.success_unified_res['data'] = msg
                except:
                    self.success_unified_res['data'] = msg
            elif type(msg) is dict:
                data = list()
                data.append(msg)
                self.success_unified_res['data'].append(msg)
            else:
                self.success_unified_res['data'] = msg
        return self.success_unified_res

    def with_error(self, msg):
        self.error_unified_res['data'] = msg
        return self.error_unified_res


# un_re_handle = UnifiedResHandle()
ErrorWrapper = UnifiedResHandle()
