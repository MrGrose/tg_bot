from os import getenv
from typing import Any

from dotenv import load_dotenv
from pytimeparse import parse

import ptbot


def reply(chat_id: int, question: str) -> None:
    num = parse(question)
    if num is None:
        bot.send_message(
            chat_id,
            'Не удалось распознать время.'
            'Пожалуйста, попробуйте еще раз.',
            )
        return None
    timer = bot.send_message(chat_id, 'Запускаю таймер:')
    bot.create_countdown(
        num,
        notify,
        author_id=chat_id,
        message=timer,
        num=num,
    )
    bot.create_timer(num + 1, choose, author_id=chat_id)


def choose(author_id: int) -> None:
    bot.send_message(author_id, 'Время вышло')


def notify(
        secs_left: int,
        author_id: int,
        message: str,
        num: float) -> None:

    text = f'Осталось секунд: {secs_left}'
    counter = num - secs_left
    progressbar = render_progressbar(total=num, iteration=counter)
    display = f'{text}\n{progressbar}'
    bot.update_message(author_id, message, display)


def render_progressbar(
        total: Any,
        iteration: Any,
        prefix: str = '',
        suffix: str = '',
        length: int = 30,
        fill: str = '█',
        zfill: str = '░') -> str:

    iteration = min(total, iteration)
    percent = '{0:.1f}'
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main() -> None:
    global bot
    load_dotenv()
    tg_token = getenv('TOKEN_API')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(reply)
    bot.run_bot()


if __name__ == '__main__':
    main()
