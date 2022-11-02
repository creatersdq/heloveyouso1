import requests


class MyHttp:
    '''配置要测试请求服务器的ip、端口、域名等信息，封装http请求方法，http头设置'''

    def __init__(self, protocol, host, port, header=""):
        # 从配置文件中读取接口服务器IP、域名，端口
        self.protocol = protocol
        self.host = host
        self.port = port
        self.headers = header  # http 头

        # install cookie #自动管理cookie

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def get_protocol(self):
        return self.protocol

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port

    # 设置http头
    def set_header(self, headers):
        self.headers = headers

    # 封装HTTP GET请求方法
    def get(self, url, params=''):
        url = self.protocol + '://' + self.host + ':' + str(self.port) + url + params

        print('发起的请求为：%s' % url)
        try:
            request = requests.get(url, headers=self.headers)
            response = request.json()
            return response
        except Exception as e:
            print('发送请求失败，原因：%s' % e)
            return None

    # 封装HTTP POST请求方法
    def post(self, url, data=''):
        url = self.protocol + '://' + self.host + ':' + str(self.port) + url

        print('发起的请求为：%s' % url)
        try:
            response = requests.post(url=url, data=data)
            response = response.json()
            return response
        except Exception as e:
            print('发送请求失败，原因：%s' % e)
            return None