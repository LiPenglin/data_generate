import json
import os
import sys
import time
from dataclasses import dataclass
from faker import Faker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config import *


@dataclass(frozen=True)
class Item:
    item_id: str
    item_type: str
    project: str
    properties: dict
    event: str = 'item_set'

    def __repr__(self):
        return json.dumps({
            "type": self.event,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "project": self.project,
            "properties": self.properties
        })

    def dump(self, **kwargs):
        print(self, file=kwargs['file_name'])


def get_ts():
    back = int(random.random() * 366)
    return int(round((time.time() - back * 24 * 60 * 60 - back * 60 * 60) * 1000))


if __name__ == '__main__':
    num = int(input('input item sum: '))
    project = input('input project name: ')

    if not os.path.exists(FILE_PREFIX):
        os.makedirs(FILE_PREFIX)

    factory = Faker("zh_CN")
    base_path = f'{FILE_PREFIX}/item'
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    file = f'{base_path}/{project}.dat'
    LOG.info(f'start write item. [file="{file}", num="{num}", project="{project}"]')
    with open(file, mode='w', encoding='utf-8') as f:
        for i in range(num):
            properties = {
                "country": factory.country(),
                "province": factory.province(),
                "company": factory.company(),
                "job": factory.job(),
                "name": factory.name(),
                "credit_card": factory.credit_card_number(),
                "phone_number": factory.phone_number(),
            }
            profile = Item(
                item_id=factory.md5(),
                item_type="suspect",
                project=project,
                properties=properties)
            profile.dump(file_name=f)
    LOG.info('successfully.')
