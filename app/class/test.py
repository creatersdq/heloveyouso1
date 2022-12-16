from classes.test1 import add
import os

if __name__ == "__main__":
    cwd_dir = os.getcwd()
    print(cwd_dir)
    os.system("celery")
    a = 1
    b = 1
    name = add(a, b)
    print(name)
