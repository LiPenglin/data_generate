import json
import time
import sys
import os
import random

from faker import Faker
from dataclasses import dataclass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config import *

@dataclass(frozen=True)
class Profile():
    distinct_id : str
    ts : int
    project : str
    properties : dict
    event : str = 'profile_set'

    def __repr__(self):
        profile = {
                "distinct_id": self.distinct_id,
                "type": self.event,
                "time": self.ts,
                "project": self.project,
                "properties": self.properties
                }
        return json.dumps(profile)

    def dump(self, **kwargs):
        print(self, file=kwargs['file_name'])

def get_ts():
    back = int(random.random()*366)
    return int(round((time.time() - back * 24 * 60 * 60 - back * 60 * 60) * 1000))

if __name__ == '__main__':
    num = int(input('input profile sum: '))
    project = input('input project name: ')

    if not os.path.exists(FILE_PREFIX):
        os.makedirs(FILE_PREFIX)

    factory = Faker("zh_CN")
    base_path = '{FILE_PREFIX}/profile'
    if not os.path.exists('base_path'):
        os.path.makedirs('base_path')

    with open (f'base_path/{project}.dat', mode='w', encoding='utf-8') as f:
        for i in range(num):
            properties = {
                    "$province" : factory.province(),
                    "color" : factory.color_name(),
                    "company" : factory.company(),
                    "credit_card" : factory.credit_card_number(),
                    "currency" : factory.currency(),
                    "job" : factory.job(),
                    "phone_number" : factory.phone_number()
                    }
            profile = Profile(
                    distinct_id=factory.md5(),
                    ts=get_ts(),
                    project=project,
                    properties=properties)
            profile.dump(file_name=f)
