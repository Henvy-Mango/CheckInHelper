import requests

from checkinhelper.tools.utils import request, extract_cookie, log


class pdawikiCheckin(object):
    SIGN_URL = 'https://www.pdawiki.com/forum/plugin.php?id=mogu_lottery:result'
    REFERER_URL = 'https://www.pdawiki.com/forum/plugin.php?id=mogu_lottery:home&actid=1'
    USER_AGENT = 'Mozilla/5.0 (Linux; Android 11; M2011K2C Build/RKQ1.200928.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/045807 Mobile Safari/537.36 MMWEBID/4858 MicroMessenger/8.0.10.1960(0x28000A3D) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'
    DATA_TEXT = 'actid=1&lottery=&formhash=d00ec163'

    def __init__(self, cookie: str = None):
        self._cookies = self.get_update_cookie(self.REFERER_URL, cookie)
        self._headers = {
            'Referer': self.REFERER_URL,
            'User-Agent': self.USER_AGENT,
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    @staticmethod
    def get_update_cookie(url, cookie):
        cookie_tmp = {'usoK_2132_saltkey': extract_cookie('usoK_2132_saltkey', cookie),
                      'usoK_2132_sid': extract_cookie('usoK_2132_sid', cookie),
                      'usoK_2132_auth': extract_cookie('usoK_2132_auth', cookie), }

        session = requests.session()
        session.get(url)

        cookie_session = session.cookies.get_dict()
        cookie_session.update(cookie_tmp)
        return cookie_session

    @property
    def _sign_info(self):
        try:
            response = request(
                'post', self.SIGN_URL, headers=self._headers, cookies=self._cookies, data=self.DATA_TEXT).json()
        except Exception as e:
            raise Exception(e)
        return response

    # {'result': 1, 'jackpot': '1', 'msg': '恭喜抽得 10 米/Got 10 rice, congrats!'}
    # {'result': 2, 'jackpot': '2', 'msg': '恭喜抽得 30 米/Got 30 rice, congrats!'}
    # {'result': 3, 'jackpot': '3', 'msg': '恭喜抽得 50 米/Got 50 rice, congrats!'}
    # {'result': 6, 'jackpot': '6', 'msg': '恭喜抽得 3 浮云/Got 3 clouds, congrats!'}
    # {'result': 7, 'jackpot': '7', 'msg': '恭喜抽得 10 浮云/Got 10 clouds, congrats!'}
    # {'result': 8, 'jackpot': None, 'msg': '谢谢参与/Thanks for playing!'}
    # {'result': 0, 'msg': '您的抽奖机会已经用完了，请 明天 再来！'}

    def run(self):
        rice = 0
        cloud = 0
        status = 1
        while status != 0:
            sign_info = self._sign_info

            log.debug(f'pdawiki json data {sign_info}')

            status = sign_info.get('result')

            if status == 1 or status == 2 or status == 3 or status == 4:
                rice = rice + int(sign_info.get('msg').split('抽得')[1].split('米')[0])
            elif status == 5 or status == 6 or status == 7:
                cloud = cloud + int(sign_info.get('msg').split('抽得')[1].split('浮云')[0])

        msg = f'抽得{rice}米 {cloud}浮云'
        log.info('pdawiki ' + msg)

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
    ✨{msg}
    {end:#^18}'''

if __name__ == "__main__":
    print(pdawikiCheckin(
        "usoK_2132_saltkey=NW3W1HHO; usoK_2132_sid=bUjpzZ; usoK_2132_auth=5c5dhXk%2BVzHyi%2Fxzh0loInyFD1ZUrKcLGm0oAWSTZrN38gkG2O166BfzLvN1dMJGVk8p%2Bvt0YfrYRH4ouOZP%2BbS7Rdc") \
          .run())
