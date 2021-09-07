from checkinhelper.tools.exceptions import CookiesExpired, CheckinHelperException
from checkinhelper.tools.utils import request, log


class jdCheckin(object):
    SIGN_URL = 'https://api.m.jd.com/client.action?functionId=signBeanAct&clientVersion=9.4.6&build=87373&client=android&d_brand=Xiaomi&d_model=MI6&osVersion=9&screen=1920*1080&partner=xiaomi001&oaid=d857d840abde1f81&eid=eidA0b08812331seMSXA0dsXTqCiZPyfRGm6vzElwknpHMi61klgN61j7mbK/k5GugV13EpRMi8HxRU3MGMDTMzJXwkB1YWe/noOtdFpOfcoQqhfuoVU&sdkVersion=28&lang=zh_CN&uuid=f35b4417b0f0d211&aid=f35b4417b0f0d211&area=19_1666_36267_36275&networkType=4g&wifiBssid=unknown&uts=0f31TVRjBSu27%2B9mkBTAWQXEgXkEDpkDTHrB1EheDBJVLQHI2nzsiZu3%2BDkyY5Sw7rKdptm94IQk%2FR1eRr9yEiHwthc%2Bg9s2QamSE49kkEvsM%2F4ij4Zl9bBRccn%2BgUpoSNXUmIaSbAIxSKM6qCONhn%2BE3X8xjSa6vQ3l6S2C3wW0Dq%2B%2Fqhc0WSCetVVxWPgCLOEX0zh4qWf%2FRvgQ9H%2Bevg%3D%3D&st=1617124794386&sign=df5cf803efbc55903103e1b1b394ef4f&sv=112'
    USER_AGENT = 'okhttp/3.12.1'
    DATA_TEXT = 'body=%7B%22eid%22%3A%22eidA0b08812331seMSXA0dsXTqCiZPyfRGm6vzElwknpHMi61klgN61j7mbK%2Fk5GugV13EpRMi8HxRU3MGMDTMzJXwkB1YWe%2FnoOtdFpOfcoQqhfuoVU%22%2C%22fp%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22rnVersion%22%3A%224.7%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%7D&'

    def __init__(self, cookie: str = None):
        self._cookie = cookie

    def get_header(self):
        header = {
            'Cookie': self._cookie,
            'User-Agent': self.USER_AGENT,
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        return header

    @property
    def _sign_info(self):
        try:
            response = request(
                'post', self.SIGN_URL, headers=self.get_header(), data=self.DATA_TEXT).json()
        except Exception as e:
            raise Exception(e)
        return response

    # {'code': '0', 'data': {'signedRan': 'B', 'status': '1', 'beanUserType': 1, 'awardType': '1', 'dailyAward': {'type': '1', 'title': '签到成功，', 'subTitle': '恭喜您获得', 'beanAward': {'beanCount': '1', 'beanImgUrl': 'https://m.360buyimg.com/njmobilecms/jfs/t23452/19/1797778090/8622/14e40996/5b69974eN9880f531.png'}}, 'signRemind': {'title': '领京豆', 'content': '签到领京豆啦，断签会错过连签礼包哦', 'popImgUrl': 'https://m.360buyimg.com/njmobilecms/jfs/t25144/349/281504248/8702/2397c397/5b6ab64fN016b2a9d.png', 'beanHomeLink': '{"des":"m","params":{"url":"https://bean.m.jd.com"}}'}, 'signAiRan': 'A', 'growthResult': {'addedGrowth': 10, 'growth': 1240, 'level': 5, 'levelUp': False, 'beanSent': False}, 'totalUserBean': '603', 'continuousDays': '18', 'tomorrowSendBeans': 0, 'activityFlag': False}}
    # {'code': '0', 'data': {'signedRan': 'B', 'status': '2', 'beanUserType': 1, 'awardType': '1', 'dailyAward': {'type': '1', 'title': '今天已签到，', 'subTitle': '获得奖励', 'beanAward': {'beanCount': '1', 'beanImgUrl': 'https://m.360buyimg.com/njmobilecms/jfs/t23452/19/1797778090/8622/14e40996/5b69974eN9880f531.png'}}, 'signRemind': {'title': '领京豆', 'content': '签到领京豆啦，断签会错过连签礼包哦', 'popImgUrl': 'https://m.360buyimg.com/njmobilecms/jfs/t25144/349/281504248/8702/2397c397/5b6ab64fN016b2a9d.png', 'beanHomeLink': '{"des":"m","params":{"url":"https://bean.m.jd.com"}}'}, 'continuousDays': '18', 'tomorrowSendBeans': 0}}

    def run(self):
        sign_info = self._sign_info
        log.debug(sign_info)

        if sign_info.get('code') != '0':
            raise CookiesExpired(f'jd cookies expired {sign_info.get("echo")}')

        status = sign_info.get('data').get('status')

        data = sign_info.get('data')
        award = sign_info.get('data').get('continuityAward')
        if award is None:
            award = sign_info.get('data').get('dailyAward')

        if status == '1':
            msg = award.get('title') + '获得' + \
                  award.get('beanAward').get('beanCount') + '京豆'
            total = '😎总共' + data.get('totalUserBean') + '京豆'
        else:
            msg = award.get('title').split('，')[0]
            total = '🤷‍'
            if msg == '今天已签到':
                log.info('jd 重复签到')
                raise CheckinHelperException('Failed to checkin:\n{}'.format(msg))

        continuous = sign_info.get('data').get('continuousDays')

        message = {
            'today': '',
            'msg': msg,
            'continuous': continuous,
            'total': total,
            'end': ''
        }

        return self.message.format(**message)

    @property
    def message(self):
        return MESSAGE_TEMPLATE


MESSAGE_TEMPLATE = '''
    {today:#^18}
    🔅{msg}
    🏃‍连续签到: {continuous} 天
    {total}
    {end:#^18}'''

if __name__ == "__main__":
    print(jdCheckin(
        "pin=jd_5e5be3bd68b3e; wskey=AAJgRSA2AECNhCtEmQrpzr0uyTyTOm68eOCCMh1G8GTDrh-nQDJhj9x6dmGB8Z4F-mdWvuYf_2RacjrXp0wKKOw86mR-BQjz; whwswswws=sUPPeQAuADxnbtLJ2GeiKOmO67ndipxPpGoPStLPZe3RaIz5+oje0ZZbRkf+PiKZlFEEWXzwQ9VaC0sH") \
          .run())
