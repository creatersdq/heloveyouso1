from apps.core.test_date_base import session_maker
from apps.models.sms_table.smsdb import CaptCha



def get_token(mobile: str):
    with session_maker() as db:
        return db.query(CaptCha).filter(CaptCha.mobile == mobile).order_by(
            CaptCha.id.desc()).first()

