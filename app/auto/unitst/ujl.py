# class FooParent(object):
#     def __init__(self):
#         self.parent = 'I\'m the parent.'
#         print('Parent')
#
#     def bar(self, message):
#         print("%s from Parent" % message)
#
#     def foo(self):
#         print("this is from foo")
#         print(self.parent+"231232")
#
# class FooChild(FooParent):
#     def __init__(self):
#         # super(FooChild,self) 首先找到 FooChild 的父类（就是类 FooParent），然后把类 FooChild 的对象转换为类 FooParent 的对象
#         super(FooChild, self).__init__()
#         self.parent = "son"
#         self.aaa=123
#         print('Child')
#
#     def bar(self, message):
#         super(FooChild, self).bar(message)
#         super(FooChild,self).foo()
#         print('Child bar fuction')
#         print(self.parent)
#         print(self.parent)
#         print(self.aaa)
#
#
# # fooChild = FooChild()
# # fooChild.bar('HelloWorld')
# import subprocess
# subprocess.getstatusoutput('pytest new_test.py--html=b.html')

# from apps.extensions.logger import logging
# from apps.unitst.error import xx

# xx()
# # Logging('gg').info('xxx')
# # Logging('cc').info('lll')
# logging.log('ss', 'ERROR', '此投保的起保时间不对')

# 测试
