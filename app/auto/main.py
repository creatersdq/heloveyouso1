import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from apps import create_app


apps = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='new_main:apps', host="127.0.0.1", port=8010, reload=True, debug=True)