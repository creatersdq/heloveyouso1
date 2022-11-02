# from app.extensions.depends_exc import TokenAuthError, TokenExpired
# from fastapi import Header, Request
# from app.db_actions.db_redis.rd_user_token import rd_read_token, re_update_time_token
#
#
# # 新增接口token依赖，强制非登录接口需token验证
#
# async def token_inspect(token: str = Header(..., ), account: str = Header(..., )):
#     if account == '18100000005':
#         pass
#     else:
#         if rd_read_token(account):
#             if rd_read_token(account).decode() == token:
#                 re_update_time_token(account)
#             else:
#                 raise TokenAuthError()
#         else:
#             raise TokenExpired()
