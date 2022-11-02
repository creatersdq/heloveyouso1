import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append(curPath)
# sys.path.append('/Users/uniondrug/Desktop/code/policy/cn_ud_test_mock/apps/public/script/claim_records__script.py')

project = "cn_ud_test_mock"
sys.path.append(os.getcwd().split(project)[0] + project)
from apps.public.mock_claim_per_records import mock_db_script
c = sys.argv
print(c)



print(c[1], c[2])
mock_db_script(str(c[1]),str(c[2]),str(c[3]), int(c[4]), int(c[5]))

