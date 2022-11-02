import datetime
import json

from apps.curd.curd_redis import redis_query


class PolicyBase(object):

    def __init__(self, dev):
        """
        :param dev: 环境
        """
        self.dev = dev  # 环境，测试:test,RC:rc
        # 配置文件
        self.__config = redis_query(name='cn_ud_test_mock')
        self.config_mock = json.loads(self.__config["mock_config"])
        self.config_server = json.loads(self.__config["server_config"])
        # 域名
        self.jm_domain = self.config_mock["DOMAIN_" + dev]["JM_INSURE"]  # 财务
        self.module_domain = self.config_mock["DOMAIN_" + dev]["MODULE"]  # MODULE
        self.gatway_domain = self.config_mock["DOMAIN_" + dev]["GATEWAY"]  # GATWAY
        # header
        self.request_header = {"Content-Type": "application/json"}  # 通用header-json
        # API
        self.api_claim = self.config_mock["MODULE_API"]["API_CLAIM"]  # 理赔数据推送
        self.api_invoice_register = self.config_mock["MODULE_API"]["API_INVOICE_REGISTER"]  # 发票数据推送
        self.api_order_attachments = self.config_mock["MODULE_API"]["API_ORDER_ATTACHMENTS"]  # 订单影像件推送
        self.api_invoice_push = self.config_mock["MODULE_API"]["API_INVOICE_PUSH"]  # 发票推送保司api
        self.api_image_push = self.config_mock["MODULE_API"]["API_IMAGE_PUSH"]  # 影像件推送保司api
        self.api_order_data_push = self.config_mock["GATEWAY_API"]["API_GUARANTEE_ORDER"]  # 保障订单推送
        self.api_claim_data_push = self.config_mock["GATEWAY_API"]["API_GUARANTEE_CLAIM"]  # 保障理赔推送
        self.api_get_pool_amount = self.config_mock["JM_API"]["QUERY_POOL_CLAIM_AMOUNT"]  # 查询资金池
        # 预设接口入参
        self.data_get_pool_amount = self.config_mock["INTERFACE_DATA"]["GET_POOL_AMOUMT"]
        self.data_claim = self.config_mock["INTERFACE_DATA"]["API_CLAIM"]
        self.data_invoice = self.config_mock["INTERFACE_DATA"]["API_INVOICE_REGISTER"]
        self.data_pool_claim = self.config_mock["MOCK_DATA"]["DATA_POOL_CLAIM"]
        self.data_order_attachments = self.config_mock["INTERFACE_DATA"]["API_ORDER_ATTACHMENTS"]
        self.data_order_data_push = self.config_mock["INTERFACE_DATA"]["API_GUARANTEE_ORDER"]
        self.data_claim_data_push = self.config_mock["INTERFACE_DATA"]["API_GUARANTEE_CLAIM"]
        # 测试数据
        self.pool_id_list = self.config_mock["POOL_CLAIM"][("id_list_" + dev)]
        self.today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.today_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.attachments_1 = self.config_mock["MOCK_DATA"]["ORDER_ATTACHMENTS_1"]
        self.attachments_2 = self.config_mock["MOCK_DATA"]["ORDER_ATTACHMENTS_2"]
        self.attachments_3 = self.config_mock["MOCK_DATA"]["ORDER_ATTACHMENTS_3"]
        self.attachments_4 = self.config_mock["MOCK_DATA"]["ORDER_ATTACHMENTS_4"]

    def get_config(self):
        return self.__config


if __name__ == "__main__":
    c = PolicyBase('test')
    c1 = c.get_config()
    print(c1)
    print(type(c1))
