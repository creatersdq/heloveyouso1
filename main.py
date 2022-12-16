import os
import sys
import uvicorn

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from app import create_app

test_mock_app = create_app()
if __name__ == '__main__':
    uvicorn.run(
        app='main:test_mock_app',
        host='0.0.0.0',
        port=8989,
        debug=True,
        reload=True)
