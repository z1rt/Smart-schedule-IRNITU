# Список институтов
def get_institute():
    institute_list = [{'name': 'ИИТиАД', 'inst_id': 1}, {'name': 'ИВТ', 'inst_id': 2}]
    return institute_list


# Список курсов у определённого института
def get_course(inst_id=0):
    courses_list = [{'name': '1 курс', 'course_id': 1}, {'name': '2 курс', 'course_id': 2}]
    return courses_list


# Список групп на определённом курсе
def get_group(cours_id=0):
    groups_list = [{'name': 'ИБб-18-1', 'group_id': 1}, {'name': 'ИБб-18-2', 'group_id': 2}]
    return groups_list


# Записываем в базу институт пользователя
def set_user_inst(chat_id=0, inst_id=0):
    pass


# Записываем в базу курс пользователя
def set_user_course(chat_id=0, course_id=0):
    pass


# Записываем в базу группу пользователя
def set_user_group(chat_id=0, group_id=0):
    pass
