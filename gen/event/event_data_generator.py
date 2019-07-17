import hashlib
import json
import time
from datetime import datetime as dt
import pymysql
import random

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config import *
from faker import Faker

factory = Faker("zh_CN")

class Utils(object):

    @classmethod
    def get_lib(cls):
        return LIBS[random.randint(0, len(LIBS)-1)]

    @classmethod
    def get_random_id(cls):
        return factory.unix_time()

    @classmethod
    def get_random_ts_md5_id(cls):
        cls._m.update(str(time.time()).encode())
        return cls._m.hexdigest()

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
    def get_anchor_list(cls):
        anchor_list = []
        for i in range(2000):
            r = {
                ANCHOR['u_id']: factory.md5(),
                ANCHOR['nick_name']: factory.name(),
                ANCHOR['r_id']: factory.numerify(),
                ANCHOR['r_name']: factory.company(),
                ANCHOR['label_e_name']: [factory.currency_name(), factory.currency_name()],
                ANCHOR['label_c_name']:  [factory.currency_name(), factory.currency_name()],
                ANCHOR['award_rank']: random.randint(0, 20000)
            }
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
        with open(f'{FILE_PREFIX}/{name}.dat', mode='a', encoding='utf-8') as f:
            print(json.dumps(data.__dict__), file=f)
        # print(data.__dict__)


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
    PROJECT_NAME = input("input project_name: ")
    day = int(input(f"input day count:"))
    FILE_PREFIX = f'{FILE_PREFIX}/{PROJECT_NAME}'
    if not os.path.exists(FILE_PREFIX):
        os.makedirs(FILE_PREFIX)
    tmp = input(f"input back day num (default 0 - {day}):")
    if tmp:
        BACK_DAY_NUM = int(tmp)
        print(f'generate event data for {BACK_DAY_NUM}')
        start()
    else:
        for i in range(day):
            BACK_DAY_NUM = i
            print(f'generate event data for {BACK_DAY_NUM} ...')
            start()
