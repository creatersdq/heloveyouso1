from apps.core.date_base import session_maker
from apps.models.case import Case
from apps.models.project import TestProject
from apps.models.plan import TestPlan
from apps.extensions.logger import log
from apps.models.case import User
from apps.models.case_copy import Config


def create_case(plan_no: str, case_type: str, case_name: str, test_result: str, test_status: int,
                return_msg: str = None, url: str = None, headers: str = None, data: str = None, method: str = None):
    # 新增测试用例
    with session_maker() as db:
        log.get_log("test_case", "INFO",
                    "{},{},{},{},{},{},{}".format(plan_no, case_type, case_name, test_result, test_status, return_msg,
                                                  url))
        plan_project = db.query(
            TestPlan.id,
            TestPlan.planName,
            TestProject.id,
            TestProject.projectName).filter(
            TestPlan.projectId == TestProject.id,
            TestPlan.planNo == plan_no).one()
        # 这里的plan_project.id因为id重复 多次测试为project_id 111
        if plan_project:
            db.add(
                Case(url=url, headers=headers, data=data, projectName=plan_project[3], projectId=plan_project[2],
                     planName=plan_project[1], planId=plan_project[0], method=method, type=case_type, name=case_name,
                     testResult=test_result, testStatus=test_status, returnMsg=return_msg))
        else:
            log.get_log('mysql', 'INFO', plan_project)
            return "TestPlan20210128137969"


def his_trend_data(project_name):
    """统计数据库中近七天的数据"""
    with session_maker() as db:
        return db.execute(

            "SELECT LEFT(a.gmtCreated, 10), COUNT(*),COUNT(a.testResult='PASS' OR NULL),"
            "COUNT(a.testResult='FAILED' OR NULL),COUNT(a.testResult='broken' OR NULL),COUNT(a.testResult='skipped' "
            "OR NULL),COUNT(a.testResult='unknown' OR NULL) "
            "FROM `case` a LEFT JOIN project b ON a.projectId = b.id WHERE b.projectName ='{}' "
            "GROUP BY LEFT (a.gmtCreated,10) ORDER BY a.gmtCreated DESC LIMIT 7".format(
                project_name)
        ).fetchall()


def get_token():
    with session_maker() as db:
        return db.query(User.token).filter(User.account == '18100000005').all()[0][0]


# 修改config表token
def update_config(belong: str, value: str):
    with session_maker() as db:
        db.query(Config).filter(Config.belong == belong).update({"value": value})



if __name__ == '__main__':
    print(his_trend_data("ddd"))