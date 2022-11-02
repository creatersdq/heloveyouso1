from jsonpath import jsonpath
from requests import request
from apps.extensions.logger import log
from apps.unify.tools.deal_request import common_request
from apps.unify.tools.tools import Unitst

u = Unitst()


def deal_test_step(args):
    # 处理测试步骤
    if args['case_title'] == '登录':  # 仅仅对于excel中的第一行标题为登录的，且relevance中有值，后续用到；把它存到类属性中去，后续在请求头中使用
        res = u.login(args)
        return res
    else:
        log.get_log(
            "test_unify",
            'INFO',
            "******111******开始处理步骤******映射类中的所有属性和值为：{} ;入参数据为 {};".format(u.get_class_attribute_value(), args))

        method = args['method'].upper()
        url = args['url']
        params = str(args['body'])
        relevance = eval(args['relevance'])
        header = args['headers']
        header_dict = eval(header)
        if """##""" in header:  # 请求头中有# 说明需要登录的token或其他字段，从映射类中获取
            for k, v in header_dict.items():
                if """##""" in v:
                    header_dict[k] = getattr(u, k)
            header = header_dict
        else:
            header = eval(header)

        if relevance == [] and """##""" not in params:  # 入参中不需要其他接口返回的参数，且返参中的字段其他接口不需要继续使用
            log.get_log(
                "test_unify",
                'INFO',
                "*******AAA******入参中不需要其他接口返回的参数，且返参中的字段其他接口不需要继续使用*******用例id为 {}; 请求方式为 {} ;入参为 {} ；URL为：{}".format(
                    args['id'], method, eval(params), url))
            params = eval(params)
            res = common_request(method, url, header, params)
            log.get_log(
                "test_unify",
                'INFO',
                "*******AAA******用例id为 {}; 返参为 {} ".format(args['id'], res))
            return res
        elif relevance != [] and """##""" not in params:  # 入参中不需要其他接口返回的参数，返参中的字段有其他接口需要继续使用
            log.get_log(
                "test_unify",
                'INFO',
                "******BBB******入参中不需要其他接口返回的参数，返参中的字段有其他接口需要继续使用******用例id为 {}; 请求方式为 {} ;入参为 {} ；URL为：{}".format(
                    args['id'], method, eval(params), url))
            params = eval(params)
            res = common_request(method, url, header, params)
            log.get_log(
                "test_unify",
                'INFO',
                "******BBB******用例id为 {}; 返参为 {} ".format(args['id'], res))
            for i in relevance:  # 循环读取列表中的数据
                relevance_params = jsonpath(res, '$..{}'.format(i))  # 取出返参中的数据
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******BBB******用例id为 {}; 读取的数据为 {} ".format(args['id'], relevance_params))
                if relevance_params:  # 返参中存在relevance列表中值得字段
                    setattr(u, i, relevance_params[0])  # 把下面参数需要的值取出，放到Units类的属性中，后面使用getattr()方法获取
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******BBB******用例id为 {}; 映射类中的所有属性和值为： {} ".format(args['id'], u.get_class_attribute_value()))
            return res
        elif """##""" in params:  # 入参中需要其他接口返回的参数
            log.get_log(
                "test_unify",
                'INFO',
                "******CCC******入参中需要其他接口返回的参数******获取映射数据字段之前******用例id为 {}; 请求方式为 {} ;入参为 {} ；URL为：{}；映射类中的所有属性和值为： "
                "{} ".format(
                    args['id'], method, eval(params), url, u.get_class_attribute_value()))
            params = eval(params)
            for k, v in params.items():
                if """##""" in str(v):
                    if hasattr(u, k):
                        # 把之前接口返参中的字段从映射中取到，赋值给使用#field#占位的参数
                        params[k] = getattr(u, k)
            log.get_log(
                "test_unify",
                'INFO',
                "******CCC******入参中需要其他接口返回的参数******获取映射数据字段之后******用例id为 {}; 请求方式为 {} ;入参为 {} ；URL为：{}".format(
                    args['id'], method, params, url))
            res = common_request(method, url, header, params)
            log.get_log(
                "test_unify",
                'INFO',
                "******CCC******用例id为 {}; 返参为 {} ".format(args['id'], res))
            # 判断relevance是否为空，来处理是否需要把它添加到映射类中
            if relevance != []:  # 入参中需要其他接口返回的参数，且返参中的字段其他接口需要继续使用
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******CCC******设置类属性之前******用例id为 {}; relevance的值为:{}; 返参为:{}; 映射类中的所有属性和值为： {} ".format(
                        args['id'], relevance, res,
                        u.get_class_attribute_value()))
                for i in relevance:
                    relevance_params = jsonpath(res, '$..{}'.format(i))  # 取出返参中的数据
                    if relevance_params:  # 返参中存在relevance列表中值得字段
                        setattr(u, i, relevance_params[0])  # 把下面参数需要的值取出，放到Unitst类的属性中，后面使用getattr()方法获取
                log.get_log(
                    "test_unify",
                    'INFO',
                    "******CCC******设置类属性之后******用例id为 {}; 映射类中的所有属性和值为： {} ".format(args['id'],
                                                                                     u.get_class_attribute_value()))
                return res
            else:  # 入参中需要其他接口返回的参数，返参中的字段其他接口不需要继续使用；不处理relevance
                return res
