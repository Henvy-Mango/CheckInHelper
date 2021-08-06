from checkinhelper.tools.exceptions import NoSuchNotifierError
from . import (
    bark,
    coolpush,
    customnotifier,
    dingtalkbot,
    igot,
    pushplus,
    serverchan,
    serverchanturbo,
    telegrambot,
    wechatworkapp,
    wechatworkbot, )

_all_notifiers = {
    'bark': bark.Bark,
    'coolpush': coolpush.CoolPush,
    'custom': customnotifier.CustomNotifier,
    'dingtalkbot': dingtalkbot.DingTalkBot,
    'igot': igot.Igot,
    'pushplus': pushplus.PushPlus,
    'serverchan': serverchan.ServerChan,
    'serverchanturbo': serverchanturbo.ServerChanTurbo,
    'telegrambot': telegrambot.TelegramBot,
    'wechatworkapp': wechatworkapp.WechatWorkApp,
    'wechatworkbot': wechatworkbot.WechatWorkBot,
}


def get_notifiers():
    return list(enumerate(_all_notifiers, start=1))


def get_notifier(name=None):
    notifiers = get_notifiers()
    notifier = [x for x in notifiers if name in x]
    if not notifier:
        raise NoSuchNotifierError(f'No {name} Notifier')
    return _all_notifiers[notifier[0][1]]()


def send2all(text='Naomi Checkin Helper',
             status=': Test',
             desp='💌 Send from checkinhelper project.'):
    for notifier in _all_notifiers:
        get_notifier(notifier).send(text, status, desp)
