import click
from threading import Thread

from bot.bot import bot, app
from parser.parser import start_pars


def starting_background_processes():
    '''запуск фоновых процессов'''
    th1 = Thread(target=start_pars)
    th1.start()


@click.group()
def cli():
    pass


@click.command()
def start_bot():
    '''запуск бота локально'''
    bot.skip_pending = True
    bot.remove_webhook()
    print('Бот запущен локально')
    bot.polling(none_stop=True, interval=0)


@click.command()
def parser():
    '''запуск парсера'''
    start_pars()


@click.command()
def runserver():
    '''запуск сервера проекта'''
    starting_background_processes()
    # bot.set_webhook(url=URL + TOKEN)
    app.run()


cli.add_command(start_bot)
cli.add_command(parser)
cli.add_command(runserver)

if __name__ == '__main__':
    cli()

# запускаем фоновые процессы
## срабатывает только при запуске через Gunicorn
starting_background_processes()
