from apps.core.date_base import session_maker
from apps.models.project import TestProject
from apps.models.plan import TestPlan


def get_project_id(prj_name):
    with session_maker() as db:
        return db.query(TestProject.id).filter(TestProject.projectName == prj_name).all()[0][0]


def update_test_plan(plan_no: str, value: str):
    with session_maker() as db:
        db.query(TestPlan).filter(TestPlan.planNo == plan_no, TestPlan.type == 1).update({"reportAddress": value})
