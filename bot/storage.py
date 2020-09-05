from pymongo import MongoClient


class MongodbService(object):
    _instance = None
    _client = None
    _db = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._client = MongoClient("localhost", 27017)
        self._db = self._client.Smart_schedule_IRNITU

    def get_data(self, collection) -> list:
        """возвращает список документов из указанной коллекции"""
        return list(self._db[collection].find())

    def save_data(self, collection, data: dict):
        """сохраняет документ в указанную коллекцию"""
        return self._db[collection].insert_one(data)

    def save_institutes(self, institutes: list):
        """сохраняет список институтов в коллекцию institutes"""
        return self._db.institutes.insert_many(institutes)

    def save_courses(self, courses: list):
        """сохраняет список курсов в коллекцию courses"""
        return self._db.courses.insert_many(courses)

    def save_groups(self, groups: list):
        """сохраняет список групп в коллекцию groups"""
        return self._db.groups.insert_many(groups)

    def get_institutes(self) -> list:
        """возвращает список институтов"""
        return list(self._db.institutes.find())

    def get_courses(self, institute='') -> list:
        """возвращает список курсов у определённого института"""
        return list(self._db.courses.find(filter={'institute': {'$regex': f'{institute}*'}}))

    def get_groups(self, course='') -> list:
        """возвращает список групп на определённом курсе"""
        return list(self._db.groups.find(filter={'course': course}))

    def save_or_update_user(self, chat_id: int, institute='', course='', group='', reminder=0):
        """сохраняет или изменяет данные пользователя (коллекция users)"""
        update = {'chat_id': chat_id, 'reminder': 0}
        if institute:
            update['institute'] = institute
        if course:
            update['course'] = course
        if group:
            update['group'] = group
        if reminder:
            update['reminder'] = reminder

        return self._db.users.update_one(filter={'chat_id': chat_id}, update={'$set': update}, upsert=True)

    def get_user(self, chat_id: int):
        return self._db.users.find_one(filter={'chat_id': chat_id})

    def delete_user_or_userdata(self, chat_id: int, delete_only_course: bool = False):
        """удаление пользователя или курса пользователя из базы данных"""
        if delete_only_course:
            return self._db.users.update_one(filter={'chat_id': chat_id}, update={'$unset': {'course': ''}},
                                             upsert=True)
        return self._db.users.delete_one(filter={'chat_id': chat_id})

    def get_schedule(self, group):
        """возвращает расписание группы"""
        return self._db.schedule.find_one(filter={'group': group})
