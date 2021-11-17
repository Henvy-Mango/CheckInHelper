import requests
from bs4 import BeautifulSoup

from checkinhelper.tools.exceptions import CheckinHelperException
from checkinhelper.tools.utils import request, extract_cookie, log


class mtbbsCheckin(object):
    SIGN_URL = 'https://bbs.binmt.cc/k_misign-sign.html?operation=qiandao&format=button&formhash=7162a56d&inajax=1&ajaxtarget=midaben_sign'
    REFERER_URL = 'https://bbs.binmt.cc/'
    USER_AGENT = 'Mozilla/5.0 (Linux; Android 11; M2011K2C Build/RKQ1.200928.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36'

    def __init__(self, cookie: str = None):
        self._cookies = self.get_update_cookie(self.REFERER_URL, cookie)
        self._headers = {
            'Referer': self.REFERER_URL,
            'User-Agent': self.USER_AGENT,
            'Accept-Encoding': 'gzip, deflate, br',
        }

    @staticmethod
    def get_update_cookie(url, cookie):
        cookie_tmp = {'cQWy_2132_saltkey': extract_cookie('cQWy_2132_saltkey', cookie),
                      'cQWy_2132_sid': extract_cookie('cQWy_2132_sid', cookie),
                      'cQWy_2132_auth': extract_cookie('cQWy_2132_auth', cookie), }

        session = requests.session()
        session.cookies.update(cookie_tmp)
        session.get(url)

        cookie_session = session.cookies.get_dict()
        return cookie_session

    @property
    def _sign_info(self):
        try:
            response = request(
                'get', self.SIGN_URL, headers=self._headers, cookies=self._cookies).text
        except Exception as e:
            raise Exception(e)
        return response

    def run(self):
        sign_info = self._sign_info
        log.debug(sign_info)

        data = sign_info.split('CDATA')[1].split('[')[1].split(']')[0]

        if data != '今日已签':
            soup = BeautifulSoup(data, 'html.parser')
            continuous = soup.find(class_='nums').text.strip().split('连续')[1]
            msg = soup.find(class_='con').text.strip().replace(' ', '')
        else:
            log.info('mtbbs 重复签到')
            raise CheckinHelperException('Failed to checkin:\n{}'.format(data))

        message = {
            'today': '',
            'continuous': continuous,
            'msg': msg,
            'end': ''
        }

        return self.message.format(**message)

    @property
    def message(self):
        return MESSAGE_TEMPLATE


MESSAGE_TEMPLATE = '''
    {today:#^18}
    🏃连续签到: {continuous} 天
    😍{msg}
    {end:#^18}'''
