import requests
import pymysql


class Anchor(object):
    def __init__(self, data):
        self.u_id = data['u_id']
        self.nick_name = data['nick_name']
        self.r_id = data['r_id']
        self.r_name = data['r_name']
        self.label_e_name = data['label_e_name']
        self.label_c_name = data['label_c_name']
        self.award_rank = data['award_rank']

    def get_insert_sql_str(self):
        return '''insert into anchor values ({self.u_id}, '{self.nick_name}', {self.r_id}, '{self.r_name}', "{self.label_e_name}", "{self.label_c_name}", {self.award_rank})'''.format(
            self=self)


db = pymysql.connect("localhost", "root", "Aa.111222", "pandatv")
cursor = db.cursor()


def insert(sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


def get_anchor_data(url, payload):
    data = requests.get(url, payload).json()
    items = data['data']['items']
    anchor_list = []
    for item in items:
        anchor = {
            'u_id': item['userinfo']['rid'],
            'nick_name': item['userinfo']['nickName'],
            'r_id': item['id'],
            'r_name': item['name'],
            'label_e_name': [l['ename'] for l in item['label']],
            'label_c_name': [l['cname'] for l in item['label']],
            'award_rank': item['ticket_rank_info']['rank']
        }
        anchor_list.append(Anchor(anchor))
    return anchor_list


def start():
    url = 'https://www.panda.tv/live_lists'
    page_no = 0
    payload = {
        'pageno': page_no,
        'pagenum': 120
    }
    count = 0
    while True:
        page_no += 1
        payload['pageno'] = page_no
        anchor_list = get_anchor_data(url, payload)

        if anchor_list:
            for anchor in anchor_list:
                # print(anchor.get_insert_sql_str())
                insert(anchor.get_insert_sql_str())
                count += 1
        else:
            break
    print(page_no, count)


if __name__ == '__main__':
    start()
    db.close()
