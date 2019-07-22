import json
import os
import sys
import time
from dataclasses import dataclass
from faker import Faker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import ids
from config import *


@dataclass(frozen=True)
class Profile:
    distinct_id: str
    ts: int
    project: str
    properties: dict
    event: str = 'profile_set'

    def __repr__(self):
        return json.dumps({
            "distinct_id": self.distinct_id,
            "type": self.event,
            "time": self.ts,
            "project": self.project,
            "properties": self.properties
        })

    def dump(self, **kwargs):
        print(self, file=kwargs['file_name'])


def get_ts():
    back = int(random.random() * 366)
    return int(round((time.time() - back * 24 * 60 * 60 - back * 60 * 60) * 1000))


if __name__ == '__main__':
    # num = int(input('input profile sum: '))
    num = len(ids.IDS)
    project = input('input project name: ')

    if not os.path.exists(FILE_PREFIX):
        os.makedirs(FILE_PREFIX)

    factory = Faker("zh_CN")
    base_path = f'{FILE_PREFIX}/profile'
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    file = f'{base_path}/{project}.dat'
    LOG.info(f'start write profile. [file="{file}", num="{num}", project="{project}"]')
    with open(file, mode='w', encoding='utf-8') as f:
        for i in range(num):
            properties = {
                "$province": factory.province(),
                "color": factory.color_name(),
                "company": factory.company(),
                "credit_card": factory.credit_card_number(),
                "currency": factory.currency(),
                "job": factory.job(),
                "phone_number": factory.phone_number()
            }
            profile = Profile(
                distinct_id=ids.IDS[i],
                ts=get_ts(),
                project=project,
                properties=properties)
            profile.dump(file_name=f)
    LOG.info('successfully.')
