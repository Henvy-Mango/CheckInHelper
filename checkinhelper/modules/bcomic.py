from checkinhelper.tools.exceptions import CheckinHelperException
from checkinhelper.tools.utils import request, get_time, log


class bcomicCheckin(object):
    SIGN_URL = 'https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn'
    USER_AGENT = 'okhttp/3.12.12'
    DATA_TEXT = '{}'

    def __init__(self, cookie: str = None):
        self._cookie = cookie

    def get_header(self):
        header = {
            'User-Agent': self.USER_AGENT,
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        return header

    @property
    def _sign_info(self):
        query = {
            'appkey': 'cc8617fd6961e070',
            'mobi_app': 'android_comic',
            'version': '3.12.0',
            'build': '36012002',
            'channel': 'xiaomi',
            'platform': 'android',
            'device': 'android',
            'buvid': 'XY0A94A068E89A9D2A8E48BD5089252B18BFB',
            'machine': 'Xiaomi+MI+6',
            'is_teenager': '0',
            'access_key': self._cookie,
            'ts': get_time()
        }
        try:
            response = request(
                'post', self.SIGN_URL, params=query, headers=self.get_header(),
                data=self.DATA_TEXT).json()
        except Exception as e:
            raise Exception(e)
        return response

    # {'code': 0, 'msg': '', 'data': {}}
    # {'code': 'invalid_argument', 'msg': 'clockin clockin is duplicate', 'meta': {'argument': 'clockin'}}

    def run(self):
        sign_info = self._sign_info
        log.debug(f'bcomic json data {sign_info}')

        status = sign_info.get('code')

        if status != 0:
            log.info('bcomic 重复签到')
            raise CheckinHelperException('Failed to checkin:\n{}'.format(sign_info.get('msg')))

        msg = '签到成功'

        message = {
            'today': '',
            'msg': msg,
            'end': ''
        }

        return self.message.format(**message)

    @property
    def message(self):
        return MESSAGE_TEMPLATE


MESSAGE_TEMPLATE = '''
    {today:#^18}
    👀{msg}
    {end:#^18}'''

if __name__ == "__main__":
    print(bcomicCheckin("c0ddcaa522681b09f82028c4a7d60951").run())
