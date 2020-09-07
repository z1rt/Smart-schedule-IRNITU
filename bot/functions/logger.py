import logging

# создаём logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

format = '%(asctime)s [%(levelname)s] %(filename)s: %(message)s'
formatter = logging.Formatter(format, datefmt='%d.%m.%Y %H:%M:%S')

# создаём консольный handler и задаём уровень
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# создаём файловый handler и задаём уровень
file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(logging.INFO)

# добавляем formatter
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# добавляем к logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
