import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append(curPath)
# sys.path.append('/Users/uniondrug/Desktop/code/policy/cn_ud_test_mock/apps/public/script/claim_records_script.py')

project = "cn_ud_test_mock"
sys.path.append(os.getcwd().split(project)[0] + project)
from apps.public.mock_claim_records import insert_claim_records_script
c = sys.argv
print(c)



print(c[1], c[2])
insert_claim_records_script(int(c[1]), int(c[2]))

