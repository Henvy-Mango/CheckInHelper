from checkinhelper.tools.utils import request, log


class eudictCheckin(object):
    SIGN_URL = 'https://api.frdic.com/api/v3/user/checkin'
    USER_AGENT = '/eusoft_ting_en_android/9.0.2/390c943f15a24890_v//xiaomi/'
    DATA_TEXT = '{timezone:8}'

    def __init__(self, cookie: str = None):
        self._cookie = cookie

    def get_header(self):
        header = {
            'Authorization': self._cookie,
            'User-Agent': self.USER_AGENT,
            'EudicUserAgent': self.USER_AGENT,
            'EudicTimezone': "8",
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json; charset=utf-8',
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

    def run(self):
        sign_info = self._sign_info

        log.debug(f'eudict json data {sign_info}')

        checkin_date = sign_info.get('checkin_date', 0)
        continuous = sign_info.get('continuous', 0)
        count = sign_info.get('count', 0)

        message = {
            'today': checkin_date,
            'continuous': continuous,
            'count': count,
            'end': ''
        }

        return self.message.format(**message)

    @property
    def message(self):
        return MESSAGE_TEMPLATE


MESSAGE_TEMPLATE = '''
    {today:#^18}
    🏃‍连续签到: {continuous} 天
    👴签到总数: {count} 天
    {end:#^18}'''
