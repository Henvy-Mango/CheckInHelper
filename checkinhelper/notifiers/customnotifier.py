from checkinhelper.tools.config import config
from .basenotifier import BaseNotifier as Base


class CustomNotifier(Base):
    def __init__(self):
        self.name = 'Custom Notifier'
        self.conf = config.CUSTOM_NOTIFIER if config.CUSTOM_NOTIFIER else {}
        self.token = self.url = self.conf.get('url')
        self.data = self.conf.get('data')
        self.retcode_key = self.conf.get('retcode_key')
        self.retcode_value = self.conf.get('retcode_value')

    def send(self, text=Base.app, status=Base.status, desp=Base.desp):
        if not self.token:
            return self.push('post', '')

        title = f'{text} {status}'
        if self.conf['merge_title_and_desp']:
            title = f'{text} {status}\n\n{desp}'
        if self.conf['set_data_title'] and self.conf['set_data_sub_title']:
            self.conf['data'][self.conf['set_data_title']] = {self.conf['set_data_sub_title']: title}
        elif self.conf['set_data_title'] and self.conf['set_data_desp']:
            self.conf['data'][self.conf['set_data_title']] = title
            self.conf['data'][self.conf['set_data_desp']] = desp
        elif self.conf['set_data_title']:
            self.conf['data'][self.conf['set_data_title']] = title

        if self.conf['method'].upper() == 'GET':
            return self.push('get', self.url, params=self.data)
        elif self.conf['method'].upper() == 'POST' and self.conf['data_type'].lower(
        ) == 'json':
            return self.push('post', self.url, json=self.data)
        else:
            return self.push('post', self.url, data=self.data)
