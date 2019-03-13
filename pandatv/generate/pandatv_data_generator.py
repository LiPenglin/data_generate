import hashlib
import json
import time
from datetime import datetime as dt

import pymysql

from config import *


class Utils(object):
    _m = hashlib.md5()
    _db = pymysql.connect("localhost", "root", "1234", "pandatv")
    _cursor = _db.cursor()

    @classmethod
    def get_lib(cls):
        return LIBS[random.randint(0, len(LIBS)-1)]

    @classmethod
    def get_db(cls):
        return cls._db

    @classmethod
    def get_random_id(cls):
        return random.randint(1, 999)

    @classmethod
    def get_random_ts_md5_id(cls):
        cls._m.update(str(time.time()).encode())
        return cls._m.hexdigest()

    @classmethod
    def get_anchor_by_id(cls, anchor_list, u_id):
        for anchor in anchor_list:
            if anchor[ANCHOR['u_id']] == u_id:
                return anchor

    @classmethod
    def get_ts(cls, back=0):
        return int(round((time.time() - back * 24 * 60 * 60 - back * 60 * 60) * 1000))

    @classmethod
    def get_random_ip(cls):
        ip = ''
        for i in range(4):
            ip += str(random.randint(1, 255))
            if i != 3:
                ip += '.'
        return ip
    @classmethod
    def hello (cls):
       return cls.get_random_ip()


    @classmethod
    def get_anchor_list(cls):
        anchor_list = []
        sql = '''select * from anchor'''
        cls._cursor.execute(sql)
        for r in cls._cursor.fetchall():
            if r[ANCHOR['label_e_name']] != '[]':
                anchor_list.append(r)
        return anchor_list

    @classmethod
    def get_random_num(cls, num):
        return random.randint(0, num)

    @classmethod
    def get_random_anchor(cls, anchor_list):
        anchor_count = len(anchor_list) - 1
        return anchor_list[cls.get_random_num(anchor_count)]

    @classmethod
    def write(cls, name, data):
        with open(FILE_PREFIX + name + '.dat', mode='a', encoding='utf-8') as f:
            print(json.dumps(data.__dict__), file=f)


class Event(object):
    def __init__(self, user_id, properties={}):
        self.distinct_id = user_id
        self.time = Utils.get_ts(BACK_DAY_NUM)
        self.type = 'track'
        self.event = self.__event__
        self.properties = properties
        self.properties['$ip'] = Utils.get_random_ip()
        self.properties['$lib'] = Utils.get_lib()
        self.properties['time'] = dt.now().strftime('%Y-%m-%d %H:%M:%S %f')
        self.project = PROJECT_NAME


class Meta(type):
    def __new__(mcs, name, bases, attrs):
        attrs['__event__'] = name
        return type.__new__(mcs, name, bases, attrs)


class HomePageView(Event, metaclass=Meta):
    def __init__(self, user_id):
        super().__init__(user_id)


class SpecificRoomView(Event, metaclass=Meta):
    def __init__(self, user_id, properties):
        super().__init__(user_id, properties)


class FollowClick(Event, metaclass=Meta):
    def __init__(self, user_id, properties):
        super().__init__(user_id, properties)


class FirstPay(Event, metaclass=Meta):
    def __init__(self, user_id, properties):
        super().__init__(user_id, properties)


def start():
    anchor_list = Utils.get_anchor_list()

    id_list = []
    for i in range(TOTAL):
        # id = Utils.get_random_ts_md5_id()
        id = Utils.get_random_id()
        id_list.append(id)
        home_page_view = HomePageView(id)
        Utils.write('home_page_view', home_page_view)
    print(len(id_list))

    id_list = id_list[::7]
    for id in id_list:
        anchor = Utils.get_random_anchor(anchor_list)
        properties = {
            'r_id': str(anchor[ANCHOR['r_id']]),
            'r_name': anchor[ANCHOR['r_name']]
        }
        specific_room_view = SpecificRoomView(id, properties)
        Utils.write('specific_room_view', specific_room_view)
    print(len(id_list))

    id_list = id_list[::5]
    for id in id_list:
        anchor = Utils.get_random_anchor(anchor_list)
        properties = {
            'u_id': str(anchor[ANCHOR['u_id']])
        }
        follow_click = FollowClick(id, properties)
        Utils.write('follow_click', follow_click)
    print(len(id_list))

    id_list = id_list[::3]
    for id in id_list:
        anchor = Utils.get_random_anchor(anchor_list)
        properties = {
            'r_id': str(anchor[ANCHOR['r_id']]),
            'award_rank': anchor[ANCHOR['award_rank']]
        }
        first_pay = FirstPay(id, properties)
        Utils.write('first_pay', first_pay)
    print(len(id_list))


if __name__ == '__main__':
    tmp = input("input back day num (default 0):")
    if tmp:
        BACK_DAY_NUM = int(tmp)
    print("generate event data...")
    start()
    Utils.get_db().close()
