from apps.core.date_base import session_maker
from apps.models.project import TestProject


def get_prj_status(project):
    with session_maker() as db:
        return db.query(TestProject.status, TestProject.type, TestProject.id).filter(
            TestProject.projectName == project).all()
