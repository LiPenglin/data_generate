import random
import logging

ANCHOR = {
    'u_id': 0,
    'nick_name': 1,
    'r_id': 2,
    'r_name': 3,
    'label_e_name': 4,
    'label_c_name': 5,
    'award_rank': 6
}
FILE_PREFIX = '/home/sa_cluster/lpl/data'
# FILE_PREFIX = '/Users/lipenglin/tmp/data'
LIBS = ['python', 'java', 'c', 'scala', 'go']
PROJECT_NAME = 'default'

BACK_DAY_NUM = 0
TOTAL = random.randint(10000, 20000)


def get_logger():
    log = logging.getLogger('lognohup')

    log.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

    # log_file_handler = logging.FileHandler('/Users/lipenglin/tmp/trash/lognohup.log')
    # log_file_handler.setFormatter(log_formatter)

    log_stream_handler = logging.StreamHandler()
    log_stream_handler.setFormatter(log_formatter)

    # log.addHandler(log_file_handler)
    log.addHandler(log_stream_handler)
    return log


LOG = get_logger()
