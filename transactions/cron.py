import logging

logger = logging.getLogger(__name__)

def my_scheduled_job():
    print('hello')
    with open('text.txt',mode='w',encoding='utf-8') as file:
        file.writelines('hello world')
    logging.info('crob job running')