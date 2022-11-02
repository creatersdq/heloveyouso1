import hashlib
import time


class sign_tools:

    @staticmethod
    def get_sign(body):
        # 拼接字符串
        list = []
        for i in body.items():
            if i[1] != "" and i[0] != "sign":
                list.append(i[1])
        sort = "".join(sorted(list))
        result = sort
        return result

    @staticmethod
    def jiami(params):
        # 加密
        m = hashlib.sha1()
        m.update(params.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def res_sign() -> dict:
        # 获得时间戳
        time_stamp = int(time.time())
        nonce = "94092762BDA12EF580DA1B773738DE5E1"
        body = {
            "nonce": nonce,
            "timestamp": str(time_stamp),
            "token": "uniondrug"
        }

        data = sign_tools.get_sign(body)
        sign = sign_tools.jiami(data)

        sign_dict = {"nonce": nonce, "sign": sign, "timestamp": time_stamp}
        return sign_dict
