import pytest

'''
简化pytest执行步骤，新增pytest外部参数注入，plan_no由原有conftest从redis取数方式调整为使用外部参数，提升pytest执行测试用例时的纯粹性质
log.get_log("runstatus","Info","执行了")
    conn = RedisPoolConnect.make_redis_conn()
    redis_value = conn.blpop("conftest", timeout=2)
    if redis_value:
        pcj_id = get_project_id(redis_value[1].decode('gbk'))
        data = {"type": 1, "planName": redis_value[1].decode('gbk'), "projectId": pcj_id, "needNo": 1}
        # token = get_token()
        token = '38ccc84ca8cd6fa8688b851f26188d8684777994ccfc71e074742c0b863cd741'

        try:
            res = requests.post(url="http://opentest-backend.uniondrug.net/api/plan/created", data=json.dumps(data),
                                headers={
                                    'token': token, "account":"18100000005"})
            log.get_log("conftest", "INFO", "返回参数json:{},返回参数text:{}".format(res.json(), res.text))
            plan_no = res.json()['data']["plan_no"]
            conn.rpush(redis_value[1].decode('gbk'), plan_no)
            conn.expire(redis_value[1].decode('gbk'),10800) # 设置这个key的有效时间为3个小时
            log.get_log("planNo", "INFO", "{}".format(plan_no))
            return plan_no
        except Exception as e:
            return 'livingzhuanyong'
    else:
        return 'livingzhuanyong'
'''

def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="livingzhuanyong", help="please enter plan_no"
    )


@pytest.fixture(scope='session')
def baidu(request):
    return request.config.getoption("--cmdopt")
