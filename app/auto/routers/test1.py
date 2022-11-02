# from fastapi import APIRouter
# from apps.extensions.logger import logging
# import json
# from apps.worker.tasks import newadd
# from apps.extensions import new_response_wrapper
# from apps.start_up import start_up
# import time
#
# router = APIRouter()
#
#
# @router.get('/test')
# async def xxx():
#     dict_01 = {
#         "name": "asf",
#         "age": "sdd"
#     }
#     # logging.log(parent="test", level="DEBUG", msg=json.dumps(dict_01))
#     new = newadd.delay()
#     # time.sleep(3)
#
#     return 666
#
#
# @router.get('/test/test')
# def docker_test():
#     logging.log(parent="test", level="DEBUG", msg=123123)
#     return new_response_wrapper.resp_200("asdsad")
#
#
# # @router.get('/test/stet_up')
# # def autotest():
# #     cc = autotest_one.delay()
# #     return new_response_wrapper.resp_200("i am ok~~~")
#
# @router.get("/test/start_up")
# def start():
#     start_up()
#     return new_response_wrapper.resp_500("i am ok~~~")
#
#
#
