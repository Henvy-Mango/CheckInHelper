from random import randint
from time import sleep

from . import notifiers
from ._version import __version__
from .modules import *
from .tools.config import config
from .tools.utils import log, get_cookies

banner = """
███╗   ██╗ █████╗  ██████╗ ███╗   ███╗██╗
████╗  ██║██╔══██╗██╔═══██╗████╗ ████║██║
██╔██╗ ██║███████║██║   ██║██╔████╔██║██║
██║╚██╗██║██╔══██║██║   ██║██║╚██╔╝██║██║
██║ ╚████║██║  ██║╚██████╔╝██║ ╚═╝ ██║██║
╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝
"""
exit_code = 0
tasks = {
    'mihoyo': [
        '欧陆签到',
        get_cookies(config.COOKIE_EUDICT),
        eudictCheckin
    ],
    'pdawiki': [
        'PDAWiki签到',
        get_cookies(config.COOKIE_PDAWIKI),
        pdawikiCheckin
    ],
    'jd': [
        '京东签到',
        get_cookies(config.COOKIE_JD),
        jdCheckin
    ],
    'bcomic': [
        '哔站漫画签到',
        get_cookies(config.ACCESSKEY_BCOMIC),
        bcomicCheckin
    ],
    'tsdm': [
        '天使动漫论坛签到',
        get_cookies(config.COOKIE_TSDM),
        tsdmCheckin
    ],
    'mtbbs': [
        'MT论坛签到',
        get_cookies(config.COOKIE_MTBBS),
        mtbbsCheckin
    ],
}


def __run_sign(name, cookies, func):
    success_count = 0
    failure_count = 0
    if not cookies:
        return [success_count, failure_count]

    account_count = len(cookies)
    account_str = 'account' if account_count == 1 else 'accounts'
    log.info(('You have {account_count} 「{name}」 {account_str} configured.').format(
        account_count=account_count, name=name, account_str=account_str
    ))
    global exit_code
    result_list = []
    for i, cookie in enumerate(cookies, start=1):
        log.info(('Preparing to perform tasks for account {i}...').format(i=i))
        try:
            result = func(cookie).run()
            success_count += 1
        except Exception as e:
            result = e
            log.exception('TRACEBACK')
            failure_count += 1
            exit_code = -1
        finally:
            result = f'🌈 No.{i}:\n    {result}\n'
            # result = f'{result}\n'
            result_list.append(result)
        continue

    message_box = [
        success_count,
        failure_count,
        f'🏆 {name}',
        f'☁️ ✔ {success_count} · ✖ {failure_count}',
        ''.join(result_list)
    ]
    return message_box


def main():
    log.info(banner)
    log.info(f'🌀 naomi checkinhelper v{__version__}')

    if config.RUN_ENV == 'prod':
        sleep_secs = randint(10, int(config.MAX_SLEEP_SECS))
        log.info(('Sleep for {} seconds...').format(sleep_secs))
        sleep(sleep_secs)

    log.info(('Starting...'))

    result = {i[0]: __run_sign(i[1][0], i[1][1], i[1][2])
              for i in tasks.items()}
    total_success = sum([i[0] for i in result.values()])
    total_failure = sum([i[1] for i in result.values()])
    message = sum([i[2::] for i in result.values()], [])
    tip = 'WARNING: Please configure environment variables or config.json file first!\n'
    message_box = '\n'.join(message) if message else tip

    log.info(('RESULT:\n') + message_box)
    # The ``` is added to use markdown code block
    markdown_message = f'```\n{message_box}```'
    if message_box != tip:
        try:
            notifiers.send2all(
                status=f' ✔ {total_success} · ✖ {total_failure}', desp=markdown_message)
        except Exception as e:
            log.exception('TRACEBACK')

    if exit_code != 0:
        log.error(('Process finished with exit code {exit_code}').format(
            exit_code=exit_code))
        exit(exit_code)
    log.info('End of process run')
