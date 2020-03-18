# Список институтов
def get_institute():
    institute_list = [{'name': 'ИИТиАД', 'inst_id': 1}, {'name': 'ИВТ', 'inst_id': 2}]
    return institute_list


# Список курсов у определённого института
def get_course(inst_id=0, inst_name=''):
    # (данные беруться из базы либо по id либо по названию института)
    courses_list = [{'name': '1 курс', 'course_id': 1}, {'name': '2 курс', 'course_id': 2}]
    return courses_list


# Список групп на определённом курсе
def get_group(cours_id=0):
    groups_list = [{'name': 'ИБб-18-1', 'group_id': 1}, {'name': 'ИБб-18-2', 'group_id': 2}]
    return groups_list


def get_user_info(chat_id=0):
    # (Заполнять словами)
    # Если такого пользоваетля нет в базе данных, то вернуть пустую строку или None
    user_info = {'chat_id': chat_id, 'inst': 'ИИТиАД', 'course': '', 'group': '', 'remining': ''}
    # Если в базе данных какое-то поле пустое, то записать пустую строку или None
    return user_info


# Записываем в базу институт пользователя
def set_user_inst(chat_id=0, inst_id=0):
    pass


# Записываем в базу курс пользователя
def set_user_course(chat_id=0, course_id=0):
    pass


# Записываем в базу группу пользователя
def set_user_group(chat_id=0, group_id=0):
    pass


# Записываем в базу время напоминания (за сколько минут до пары)
def set_user_reminding(chat_id=0, time=0):
    print(f'set_user_reminding, time = {time}')
    pass


# Удаляем информацию об институте пользователя из базы данных
def del_user_inst(chat_id=0):
    pass


# Удаляем информацию о курсе пользователя из базы данных
def del_user_course(chat_id=0):
    pass


# Удаляем информацию о пользователе из базы данных
def del_user_info(chat_id=0):
    print('del_user_info, chat_id:', chat_id)
    pass
