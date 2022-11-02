from requests import request
from jsonpath import jsonpath
from apps.extensions.logger import log


# def front_handle(args):
#     """case_parent_code = 0 的前置操作"""
#     method = args['method'].upper()
#     url = args['url']
#
#     print("前置参数：", args)

class Unitst(object):
    def get_class_attribute_value(self):
        class_dict = {}
        class_list = dir(self)
        for i in class_list:
            if '__' not in i and "get_class_attribute_value" != i and 'login' != i:
                class_dict[i] = getattr(self, i)
        return str(class_dict)

    def login(self, args):
        # 仅仅对于excel中的第一行标题为登录的，且relevance中有值，后续用到；把它存到类属性中去，后续在请求头中使用
        url = args['url']
        method = args['method']
        params = eval(args['body'])
        header = eval(args['headers'])
        res = request(method=method, url=url, json=params, headers=header).json()
        relevance = eval(args['relevance'])
        try:
            for i in relevance:
                relevance_params = jsonpath(res, '$..{}'.format(i))
                if relevance_params:
                    setattr(self, i, relevance_params[0])
            return res
        except Exception as e:
            raise e


# if __name__ == '__main__':
#     u = Unitst()
#     u.get_class_attribute_value()
