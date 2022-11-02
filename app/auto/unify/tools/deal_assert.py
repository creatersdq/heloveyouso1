from jsonpath import jsonpath

from apps.extensions.logger import log


class DealAssert(object):
    """断言类"""

    def __init__(self, i, response: dict):
        self.args = i
        self.assert_type = eval(i['assert_type'])
        self.assert_field = eval(i['assert_field'])
        self.assert_value = eval(i['assert_value'])
        self.response = response

    def deal_params(self):
        """每个字段仅允许断言一次，即入参args中的assert_field列表中的数据不允许重复"""
        # 处理入参数据为[["type","field","value"],["type1","field1","value1"],["type2","field2","value2"]]
        list_first = []
        for i in self.assert_field:
            list_two = []
            list_two.append(self.assert_type[self.assert_field.index(i)])
            list_two.append(i)
            list_two.append(self.assert_value[self.assert_field.index(i)])
            list_first.append(list_two)
        return list_first

    def equal_assert(self, field, value):
        """
        断言等于  '='
        {
        "name":"张三",
        "age":"19"
         }
        断言name的值是"张三"
        """
        res = jsonpath(self.response, '$..{}'.format(field))  # 取出返参中的数据
        if isinstance(res, bool):
            log.get_log(
                "test_unify",
                'INFO',
                "******断言等于验证不通过--接口返参中没有找到 {} 字段，******用例id为 {} ;校验字段为:{},校验值为:{},入参数据为 {}; 接口返回为：{}".format(field,
                                                                                                              self.args[
                                                                                                                  'id'],
                                                                                                              field,
                                                                                                              value,
                                                                                                              self.args,
                                                                                                              self.response))
            return False
        else:
            res = res[0]
        if res == value:
            log.get_log(
                "test_unify",
                'INFO',
                "******断言等于--验证通过******用例id为 {};校验字段为:{},校验值为:{},入参数据为 {}; 接口返回为：{}".format(self.args['id'],
                                                                                            field, value, self.args,
                                                                                            self.response))
            return True
        else:
            log.get_log(
                "test_unify",
                'INFO',
                "******断言等于--验证不通过******用例id为 {}; 校验字段为：{}; 校验值为：{}; 接口该字段返回值为：{}; 接口入参数据为 {}; 接口返回为：{}".format(
                    self.args['id'], field, value, res, self.args, self.response))
            return False

    def include_assert(self, field, value):
        """
        断言返参中包含某某字段   'include'
        {
        "name":"张三",
        "age":"19"
        }
        断言结构体中包含name字段
        """
        res = jsonpath(self.response, '$..{}'.format(field))
        if res:
            log.get_log(
                "test_unify",
                'INFO',
                "******断言包含--验证通过******用例id为 {};入参为：{};接口返参为：{}".format(self.args['id'], self.args, self.response))
            return True
        else:
            log.get_log(
                "test_unify",
                'INFO',
                "******断言包含--验证不通过******用例id为 {},校验的字段为:{};接口返参为:{}".format(self.args['id'], field, self.response))
            return False

    def data_type(self, field, value):
        """
        断言返参中某个类型是某某类型   'data_type'
        {
        "name":"张三",
        "like":[
                "读书",
                "跑步"
                ]
        }
        断言like字段的value类型是列表
        """

        res = jsonpath(self.response, '$..{}'.format(field))  # 取出返参中的数据
        if isinstance(res, bool):
            log.get_log(
                "test_unify",
                'INFO',
                "******断言字段类型--验证不通过--接口返参中没有找到 {} 字段，******用例id为 {} ; 校验字段为:{}, 校验值为:{}, 入参数据为 {}; 接口返回为：{}".format(
                    field,
                    self.args[
                        'id'],
                    field,
                    value,
                    self.args,
                    self.response))
            return False
        else:
            res = res[0]
        if value == 'list':
            if isinstance(res, list):

                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--list--验证通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}; 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            else:
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--list--验证不通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}, 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))

            return isinstance(res, list)
        elif value == 'bool':
            if isinstance(res, bool):

                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--bool--验证通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{},入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            else:
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--bool--验证不通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}, 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            return isinstance(res, bool)
        elif value == 'dict':
            if isinstance(res, dict):

                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--dict--验证通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}; 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            else:
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--dict--验证不通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}, 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            return isinstance(res, dict)
        elif value == 'int':
            if isinstance(res, int):

                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--int--验证通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}; 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            else:
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--int--验证不通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}; 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            return isinstance(res, int)
        elif value == 'float':
            if isinstance(res, float):

                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--float--验证通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}; 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            else:
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--float--验证不通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}; 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            return isinstance(res, float)
        elif value == 'str':
            if isinstance(res, str):

                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--str--验证通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}; 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            else:
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******断言字段类型--str--验证不通过******用例id为 {}；校验字段为：{}; 校验值为：{}; 校验字段返回:{}; 入参为：{}; 接口返参为：{}".format(
                        self.args['id'],
                        field, value, res,
                        self.args,
                        self.response))
            return isinstance(res, str)
        else:
            log.get_log(
                "test_unify",
                'INFO',
                "******断言字段类型--验证不通过--字段类型验证不支持 {}--{} 的验证******用例id为 {}；入参为：{};接口返参为：{}".format(field, value,
                                                                                                 self.args['id'],
                                                                                                 self.args,
                                                                                                 self.response))
            return False

    def not_null(self, field, value):
        """
        断言非空     'not_null'
        {
        "name":"张三",
        "age":"19"
        }
        断言name数据不为空
        """

        res = jsonpath(self.response, '$..{}'.format(field))  # 取出返参中的数据
        if isinstance(res, bool):
            log.get_log(
                "test_unify",
                'INFO',
                "******断言非空--验证不通过--接口返参中没有找到 {} 字段，******用例id为 {} ;入参数据为 {}; 接口返回为：{}".format(field, self.args['id'],
                                                                                               self.args,
                                                                                               self.response))

            return False
        else:
            res = res[0]
        if res:
            log.get_log(
                "test_unify",
                'INFO',
                "******断言非空--验证通过******用例id为 {}; 验证字段为：{}; 入参数据为 {}; 接口返回为：{}".format(self.args['id'], field,
                                                                                      self.args,
                                                                                      self.response))
            return True
        else:
            log.get_log(
                "test_unify",
                'INFO',
                "******断言非空--验证不通过******用例id为 {}; 验证字段为：{}; 入参数据为 {}; 接口返回为：{}".format(self.args['id'], field,
                                                                                       self.args,
                                                                                       self.response))
            return False

    def deal_assert(self):
        """断言统一处理"""
        assert_data = self.deal_params()
        for i in assert_data:
            if i[0] == '=':
                result = self.equal_assert(i[1], i[2])
                if not result:
                    return False
            elif i[0] == 'include':
                result = self.include_assert(i[1], i[2])
                if not result:
                    return False
            elif i[0] == 'data_type':
                result = self.data_type(i[1], i[2])
                if not result:
                    return False
            elif i[0] == 'not_null':
                result = self.not_null(i[1], i[2])
                if not result:
                    return False
        return True

# if __name__ == '__main__':
#     args = {
#         "id": 1,
#         "assert_type": "['=','=','data_type','include','not_null']",
#         "assert_field": "['a','b','c','d','e']",
#         "assert_value": "['10','20','str','','']"
#
#     }
#     response = {"a": '10', "b": '20', "c": 'True', "d": 1.2, "e": 444}
#
#     res = DealAssert(args, response).deal_assert()
#     print("res:", res)
