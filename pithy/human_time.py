#!/usr/bin/python
# coding=utf-8
from datetime import datetime, timedelta
import time

# 日期格式
datetime_formats = ["%Y-%m-%d %H:%M:%SZ",
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d %H:%M:%S%z",
                    "%Y-%m-%d %H:%M:%S.%f",
                    "%Y-%m-%d %H:%M:%S %f",
                    "%Y-%m-%d %H:%M:%S%Z",
                    "%c",
                    "%s",
                    "%Y-%m-%d",
                    # YMD other than ISO
                    "%Y%m%d",
                    "%Y.%m.%d",
                    # Popular MDY formats
                    "%m/%d/%Y",
                    "%m/%d/%y",
                    # DMY with full year
                    "%d %m %Y",
                    "%d-%m-%Y",
                    "%d/%m/%Y",
                    "%d/%m %Y",
                    "%d.%m.%Y",
                    "%d. %m. %Y",
                    "%d %b %Y",
                    "%d %B %Y",
                    "%d. %b %Y",
                    "%d. %B %Y",
                    # MDY with full year
                    "%b %d %Y",
                    "%b %dst %Y",
                    "%b %dnd %Y",
                    "%b %drd %Y",
                    "%b %dth %Y",
                    "%b %d, %Y",
                    "%b %dst, %Y",
                    "%b %dnd, %Y",
                    "%b %drd, %Y",
                    "%b %dth, %Y",
                    "%B %d %Y",
                    "%B %dst %Y",
                    "%B %dnd %Y",
                    "%B %drd %Y",
                    "%B %dth %Y",
                    "%B %d, %Y",
                    "%B %dst, %Y",
                    "%B %dnd, %Y",
                    "%B %drd, %Y",
                    "%B %dth, %Y",
                    # DMY with 2-digit year
                    "%d %m %y",
                    "%d-%m-%y",
                    "%d/%m/%y",
                    "%d/%m-%y",
                    "%d.%m.%y",
                    "%d. %m. %y",
                    "%d %b %y",
                    "%d %B %y",
                    "%d. %b %y",
                    "%d. %B %y",
                    # MDY with 2-digit year
                    "%b %dst %y",
                    "%b %dnd %y",
                    "%b %drd %y",
                    "%b %dth %y",
                    "%B %dst %y",
                    "%B %dnd %y",
                    "%B %drd %y",
                    "%B %dth %y"
                    ]


class HumanDateTime(object):
    """
    # 解析时间戳
    print(repr(HumanDateTime(1490842267)))
    print(HumanDateTime(1490842267000))
    print(HumanDateTime(1490842267.11111))
    print(HumanDateTime(1490842267111.01))

    # 解析字符串格式日期
    print(HumanDateTime('2017-02-02'))
    print(HumanDateTime('Thu Mar 30 14:21:20 2017'))
    print(HumanDateTime(time.ctime()))
    print(HumanDateTime('2017-3-3'))
    print(HumanDateTime('3/3/2016'))
    print(HumanDateTime('2017-02-02 00:00:00'))

    # 解析datetime或date类型时间
    print(HumanDateTime(datetime(year=2018, month=11, day=30, hour=11)))
    print(HumanDateTime(date(year=2018, month=11, day=30)))

    # 增加减少时间
    print(HumanDateTime('2017-02-02').add_day(1))
    print(HumanDateTime('2017-02-02').sub_day(1))
    print(HumanDateTime('2017-02-02').add_hour(1))
    print(HumanDateTime('2017-02-02').sub_hour(1))
    print(HumanDateTime('2017-02-02').add(days=1, hours=1, weeks=1, minutes=1, seconds=6))
    print(HumanDateTime('2017-02-02').sub(days=1, hours=1, weeks=1, minutes=1, seconds=6))

    # 转换为时间戳
    print(HumanDateTime(1490842267.11111).timestamp_second)
    print(HumanDateTime(1490842267.11111).timestamp_microsecond)
    print(HumanDateTime('2017-02-02 12:12:12.1111').add_day(1).timestamp_microsecond)
    print(HumanDateTime('2017-02-02 12:12:12 1111').add_day(1).timestamp_microsecond)

    # 比较大小
    print(HumanDateTime('2017-02-02 12:12:12 1111') < HumanDateTime('2017-02-02 12:12:11 1111'))
    print(HumanDateTime('2017-02-02 12:12:12 1111') < HumanDateTime('2017-02-02 12:13:11 1111'))
    print(HumanDateTime('2017-02-02 12:12:12 1111') < '2017-02-02 12:11:11')
    print(HumanDateTime('2017-02-02 12:12:12 1111') < '2017-02-02 12:13:11 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') == '2017-02-02 12:13:11 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') == '2017-02-02 12:13:12 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') <= '2017-02-02 12:13:11 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') >= '2017-02-02 12:13:11 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') != time.time())
    print(HumanDateTime('2017-02-02 12:12:12 1111') <= time.time())
    print(HumanDateTime('2017-02-02 12:12:12 1111') >= time.time())

    # 约等于或者接近
    print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:11 1111'))
    print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:10 1111'))
    print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:10 1111', offset=2))
    print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:14 1111', offset=2))

    # 调用datetime的方法和属性
    print(HumanDateTime('2017-02-02 12:12:12 1111').day)
    print(HumanDateTime('2017-02-02 12:12:12 1111').year)
    print(HumanDateTime('2017-02-02 12:12:12 1111').second)
    print(HumanDateTime('2017-02-02 12:12:12 1111').date())
    """
    def __init__(self, time_object=None):

        self._datetime = None

        # 如果没有初始值的话,time_object设置为当前时间
        if not time_object:
            time_object = datetime.now()

        time_object = str(time_object)

        # 如果time_object可转化为数字,则使用时间戳解析,如果不能,使用字符串方式解析
        try:
            time_object = float(time_object)
            self._parse_timestamp(time_object)
        except ValueError:
            self._parse_time_str(time_object)

    def _parse_timestamp(self, time_object):
        """
        解析时间戳
        """
        if len(str(int(time_object))) == 10:
            self._datetime = datetime.fromtimestamp(time_object)
        elif len(str(int(time_object))) == 13:
            self._datetime = datetime.fromtimestamp(time_object / 1000.0)
        else:
            raise ValueError(u'输入的时间格式不正确')

    def _parse_time_str(self, time_object):
        """
        解析时间字符串
        """
        for i in datetime_formats:
            try:
                self._datetime = datetime.strptime(time_object, i)
                break
            except:
                continue

        if not self._datetime:
            raise ValueError(u'输入的时间格式不正确')

    @property
    def timestamp_second(self):
        """
        时间戳(秒)
        """
        return int(self._datetime.strftime("%s"))

    @property
    def timestamp_microsecond(self):
        """
        时间戳(毫秒)
        """
        return int(time.mktime(self._datetime.timetuple()) * 1e3 + self._datetime.microsecond / 1e3)

    def add(self, days=0, weeks=0, hours=0, minutes=0, seconds=0):
        """
        增加时间
        :param days: 天
        :param weeks: 星期
        :param hours: 小时
        :param minutes: 分钟
        :param seconds: 秒
        :return:
        """
        return self.__class__(str(self._datetime +
                                  timedelta(days=days, weeks=weeks, hours=hours, minutes=minutes, seconds=seconds)))

    def sub(self, days=0, weeks=0, hours=0, minutes=0, seconds=0):
        """
        减少时间
        :param days: 天
        :param weeks: 星期
        :param hours: 小时
        :param minutes: 分钟
        :param seconds: 秒
        :return: HumanDateTime对象
        """
        return self.__class__(str(self._datetime +
                                  timedelta(days=-days, weeks=-weeks, hours=-hours, minutes=-minutes, seconds=-seconds)))

    def add_week(self, week):
        """
        增加星期
        :param week: 星期
        :return: HumanDateTime对象
        """
        return self.add(weeks=week)

    def sub_week(self, week):
        """
        减少星期
        :param week: 星期
        :return: HumanDateTime对象
        """
        return self.sub(weeks=week)

    def add_day(self, day):
        """
        增加天
        :param day: 天
        :return: HumanDateTime对象
        """
        return self.add(days=day)

    def sub_day(self, day):
        """
        减少天
        :param day: 天
        :return: HumanDateTime对象
        """
        return self.sub(days=day)

    def add_hour(self, hour):
        """
        增加小时
        :param hour: 小时
        :return: HumanDateTime对象
        """
        return self.add(hours=hour)

    def sub_hour(self, hour):
        """
        减少小时
        :param hour: 小时
        :return: HumanDateTime对象
        """
        return self.sub(hours=hour)

    def add_minute(self, minute):
        """
        增加分钟
        :param minute: 分钟
        :return: HumanDateTime对象
        """
        return self.add(minutes=minute)

    def sub_minute(self, minute):
        """
        减少分钟
        :param minute: 分钟
        :return: HumanDateTime对象
        """
        return self.sub(minutes=minute)

    def approach(self, other, offset=1):
        """
        约等于（接近）
        :param other: 比较对象
        :param offset: 允许的偏差,单位为秒
        :return:
        """
        return abs(self.timestamp_microsecond - self.__class__(other).timestamp_microsecond) <= offset * 1000

    def __lt__(self, other):
        return self.timestamp_microsecond < self.__class__(other).timestamp_microsecond

    def __le__(self, other):
        return self.timestamp_microsecond <= self.__class__(other).timestamp_microsecond

    def __gt__(self, other):
        return self.timestamp_microsecond > self.__class__(other).timestamp_microsecond

    def __ge__(self, other):
        return self.timestamp_microsecond >= self.__class__(other).timestamp_microsecond

    def __eq__(self, other):
        return self.timestamp_microsecond == self.__class__(other).timestamp_microsecond

    def __ne__(self, other):
        return self.timestamp_microsecond != self.__class__(other).timestamp_microsecond

    def __getattr__(self, item):
        return getattr(self._datetime, item)

    def __str__(self):
        return str(self._datetime)

    def __unicode__(self):
        return unicode(self._datetime)

    def __repr__(self):
        return repr(self._datetime)
