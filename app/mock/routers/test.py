from fastapi import APIRouter
from app.extensions import res_wrapper
from time import sleep, time

router = APIRouter()


@router.get("/time/use")
async def time_use():
    st = time()
    sleep(2)
    return res_wrapper.resp_200(time() - st)
