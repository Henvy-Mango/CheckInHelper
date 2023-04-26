from checkinhelper.tools.exceptions import CheckinHelperException
from checkinhelper.tools.utils import request, extract_cookie, log


class tsdmCheckin(object):
    SIGN_URL = 'https://www.tsdm39.com/plugin.php?id=minerva:sign_in'
    REFERER_URL = 'https://www.tsdm39.com/plugin.php?id=minerva:sign_in'
    USER_AGENT = 'Mozilla/5.0 (Linux; Android 9) Xiaomi MI 6 id=3e77fbd1ba5ec2d3 (KHTML, like Gecko) net.tsdm.tut/2.3.1.0 Mobile'
    DATA_TEXT = 'client_hash=31EF24BD5B0196905D7BA25300C5CC58&emotion=1&comment=Android%E5%AE%A2%E6%88%B7%E7%AB%AF%E7%AD%BE%E5%88%B0&'

    def __init__(self, cookie: str = None):
        self._cookies = self.get_update_cookie(cookie)
        self._headers = {
            'Referer': self.REFERER_URL,
            'User-Agent': self.USER_AGENT,
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    @staticmethod
    def get_update_cookie(cookie):
        return {'s_gkr8_f779_auth': extract_cookie('s_gkr8_f779_auth', cookie),
                's_gkr8_f779_sid': extract_cookie('s_gkr8_f779_sid', cookie),
                's_gkr8_f779_saltkey': extract_cookie('s_gkr8_f779_saltkey', cookie), }

    @property
    def _sign_info(self):
        try:
            response = request(
                'post', self.SIGN_URL, headers=self._headers, cookies=self._cookies, data=self.DATA_TEXT).json()
        except Exception as e:
            raise Exception(e)
        return response

    # {'status': -1, 'message': 'already_signed'}
    # {'status': 0, 'message': 'signed', 'reward_type': 2, 'reward_value': 14, 'reward_name': '天使币'}

    def run(self):
        sign_info = self._sign_info
        log.debug(sign_info)

        status = sign_info.get('status')

        if status != 0:
            log.info('tsdm 重复签到')
            raise CheckinHelperException('Failed to checkin:\n{}'.format(sign_info.get('message')))

        msg = '获得' + str(sign_info.get('reward_value', '')) + sign_info.get('reward_name', '')
        log.info('tsdm ' + msg)

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
    🤗{msg}
    {end:#^18}'''
