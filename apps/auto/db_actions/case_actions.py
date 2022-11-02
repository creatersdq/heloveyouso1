from apps.models.case_copy import (Case, CaseRc)
from apps.core.date_base import session_maker

# def create_case(name:str,url:str,headers:str,data:str,return_msg:str,result:str,status:int):
#     with session_maker() as db:
#         db.add(Case(name=name,url=url,headers=headers,data=data,return_msg=return_msg,test_result=result,test_status=status))

# 增加测试用例
def create_case(companycode:str,businesscode:str,name:str):
    with session_maker() as db:
        casedata = db.query(Case).filter(Case.companyCode==companycode,Case.businessCode==businesscode,Case.name==name,Case.test_status==0).first()
        if casedata == None:
            # print('add')
            db.add(Case(companyCode=companycode,businessCode=businesscode,name=name,test_status=0))


# 新增测试用例
def create_rc_case(project_name: str, project_id: int, url: str, data: str, headers: str, return_msg: str,
                   method: str, case_name: str, plan_name: str, plan_id: int, test_result: str):

    with session_maker() as db:
        db.add(CaseRc(url=url, headers=headers, data=data, project_name=project_name, test_result=test_result,
                      project_id=project_id, method=method, name=case_name, plan_id=plan_id, return_msg=return_msg,
                      plan_name=plan_name, type="接口自动化", test_status=1))

# 更新测试用例
def update_case(companycode:str,businesscode:str,name:str,msg:dict):
    with session_maker() as db:
        db.query(Case).filter(Case.companyCode==companycode,Case.businessCode==businesscode,Case.name==name,Case.test_status==0).update(msg)


# a = create_case("GuoRenDrug","099100AF",'1')

