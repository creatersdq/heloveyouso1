import datetime

from dateutil.relativedelta import relativedelta
from apps.extensions.logger import log

# 当天

today = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

# 当天-年-月
today_month = datetime.date.today().strftime("%Y-%m")

# 当天-年-月-日
today_day = datetime.date.today().strftime("%Y-%m-%d")

# 昨天
yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")

# 前天
before_yesterday = (datetime.datetime.now() + datetime.timedelta(days=-2)).strftime("%Y-%m-%d %H:%M:%S")


class DateCal(object):

    def __init__(self):
        self.start_date = None
        self.end_date = None

    def insure_date_cal(self, effect_num: int, policy_period: int, policy_period_type: int) -> None:

        """
        根据追溯期计算保险起期、止期
        :param: effect_num : 生效间隔日
        :param: policy_period : 保险期间
        :param: policy_period_type : 保险期间类型(1：年，2：月 3：天')
        :return: self.start_date ，self.end_date 保险起期，保险止期
        """

        # 获取当天日期
        now = datetime.date.today()
        # 到签处理
        modified_date = now + relativedelta(days=effect_num)
        # 年
        if policy_period_type == 1:
            # 保险起期计算
            self.start_date = modified_date.strftime("%Y-%m-%d %H:%M:%S")
            # 保险止期=保险起期+保险期间-一天
            self.end_date = modified_date + relativedelta(years=policy_period) + relativedelta(days=-1)
            # 格式处理
            self.end_date = self.end_date.strftime("%Y-%m-%d %23:%59:%59")
        # 月
        elif policy_period_type == 2:
            # 保险起期计算
            self.start_date = modified_date.strftime("%Y-%m-%d %H:%M:%S")
            # 保险止期=保险起期+保险期间-一天
            self.end_date = modified_date + relativedelta(months=policy_period) + relativedelta(days=-1)
            # 格式处理
            self.end_date = self.end_date.strftime("%Y-%m-%d %23:%59:%59")
        # 天
        elif policy_period_type == 3:
            # 保险起期计算
            self.start_date = modified_date.strftime("%Y-%m-%d %H:%M:%S")
            # 保险止期=保险起期+保险期间-一天
            self.end_date = modified_date + relativedelta(days=(policy_period - 1))
            # 格式处理
            self.end_date = self.end_date.strftime("%Y-%m-%d %23:%59:%59")
        else:
            print("计算错误，请检查入参")

        log.get_log("insurance_interconnection", "INFO", "计算保险起期：{},保险止期：{}".format(self.start_date, self.end_date))


if __name__ == '__main__':
    print(today)
    print(yesterday)
    print(before_yesterday)
    print(today_month)
    print(today_day)
    c = DateCal()
    c.insure_date_cal(1, 2, 2)
    print(c.end_date)
    print(c.start_date)
