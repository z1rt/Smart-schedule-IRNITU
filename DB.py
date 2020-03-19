import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
# Устанавливаем соединение
conn = sqlite3.connect(f'{BASE_DIR}+/database.db')


# Инициализация ДБ
def init_db():
    cursor = conn.cursor()
    # Создание таблицы institutes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institutes(
        inst_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        name text
        )
          ''')

    # Создание таблицы courses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses(
        course_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        name text,
        inst_id INTEGER, 
        FOREIGN KEY (inst_id) REFERENCES institutes(inst_id)
        )
          ''')

    # Создание таблицы groups
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups(
        group_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        name text,
        course_id INTEGER, 
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
          ''')

    # Создание таблицы users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        chat_id INTEGER,
        inst_name text,
        course text,
        group_name text,
        remining INTEGER
        )
          ''')

    cursor.close


init_db()


def insert_institutes(institutes=[]):
    cursor = conn.cursor()
    # institutes = [('ИВТ',),('ИИТиАД',),('ИАиТ',)]
    cursor.executemany('INSERT INTO institutes VALUES (NULL,?);', institutes)
    conn.commit()
    cursor.close()


def insert_courses(courses=[]):
    cursor = conn.cursor()
    # courses = [('1 курс',1),('2 курс',1),('3 курс',2)]
    cursor.executemany('INSERT INTO courses VALUES (NULL,?,?);', courses)
    conn.commit()
    cursor.close()


def insert_groups(groups=[]):
    cursor = conn.cursor()
    groups = [('ИБб-18-1', 28), ('ИБб-18-2', 28), ('ИБб-19-1', 27)]
    cursor.executemany('INSERT INTO groups VALUES (NULL,?,?);', groups)
    conn.commit()
    cursor.close()


init_db()


# Список институтов
def get_institute():
    # institute_list = [{'name': 'ИИТиАД', 'inst_id': 1}, {'name': 'ИВТ', 'inst_id': 2}]
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM institutes')
    institute_list = []
    for i in cursor.fetchall():
        inst = {'inst_id': i[0], 'name': i[1]}
        institute_list.append(inst)
    cursor.close()
    return institute_list


# Список курсов у определённого института
def get_course(inst_id=0, inst_name=''):
    # (данные беруться из базы либо по id либо по названию института)
    # courses_list = [{'name': '1 курс', 'course_id': 1}, {'name': '2 курс', 'course_id': 2}]
    cursor = conn.cursor()
    if inst_name:
        cursor.execute('SELECT inst_id FROM institutes WHERE name = (?)', (inst_name,))
        inst_id = cursor.fetchone()[0]
    cursor.execute(f'SELECT * FROM courses WHERE inst_id = (?)', (inst_id,))
    courses_list = []
    for i in cursor.fetchall():
        course = {'course_id': i[0], 'name': i[1]}
        courses_list.append(course)
    cursor.close()

    return courses_list


# Список групп на определённом курсе
def get_group(course_id=0):
    # groups_list = [{'name': 'ИБб-18-1', 'group_id': 1}, {'name': 'ИБб-18-2', 'group_id': 2}]
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM groups WHERE course_id = (?)', (course_id,))
    groups_list = []
    for i in cursor.fetchall():
        group = {'group_id': i[0], 'name': i[1]}
        groups_list.append(group)
    cursor.close()
    return groups_list


def get_user_info(chat_id=0):
    # (Заполнять словами)
    # Если такого пользоваетля нет в базе данных, то вернуть пустую строку или None
    # user_info = {'chat_id': chat_id, 'inst_name': 'Аспирантура', 'course': ' 0 курс', 'group_name': '', 'remining': ''}
    # Если в базе данных какое-то поле пустое, то записать пустую строку или None

    cursor = conn.cursor()
    cursor.execute(f'SELECT inst_name, course, group_name, remining FROM users WHERE chat_id = (?)', (chat_id,))
    data = cursor.fetchone()
    if not data:
        return
    user_info = {'chat_id': chat_id, 'inst_name': data[0], 'course': data[1], 'group': data[2], 'remining': data[3]}
    cursor.close()

    return user_info


# Записываем в базу институт пользователя
def set_user_inst(chat_id=0, inst_id=0):
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM institutes WHERE inst_id = (?)', (inst_id,))
    inst_name = cursor.fetchone()[0]

    cursor.execute('INSERT INTO users VALUES (NULL,?,?,NULL,NULL,NULL);', (chat_id, inst_name))
    conn.commit()
    cursor.close()


# Записываем в базу курс пользователя
def set_user_course(chat_id=0, course_id=0):
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM courses WHERE course_id = (?)', (course_id,))
    course = cursor.fetchone()[0]

    cursor.execute('UPDATE users SET course = (?) WHERE chat_id = (?)', (course, chat_id))
    conn.commit()
    cursor.close()


# Записываем в базу группу пользователя
def set_user_group(chat_id=0, group_id=0):
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM groups WHERE group_id = (?)', (group_id,))
    group_name = cursor.fetchone()[0]

    cursor.execute('UPDATE users SET group_name = (?) WHERE chat_id = (?)', (group_name, chat_id))
    conn.commit()
    cursor.close()


# Записываем в базу время напоминания (за сколько минут до пары)
def set_user_reminding(chat_id=0, time=0):
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET remining = (?) WHERE chat_id = (?)', (time, chat_id))
    conn.commit()
    cursor.close()


# Удаляем информацию о курсе пользователя из базы данных
def del_user_course(chat_id=0):
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET course = NULL WHERE chat_id = (?)', (chat_id,))
    conn.commit()
    cursor.close()


# Удаляем информацию о пользователе из базы данных
def del_user_info(chat_id=0):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE chat_id = (?)', (chat_id,))
    conn.commit()
    cursor.close()
