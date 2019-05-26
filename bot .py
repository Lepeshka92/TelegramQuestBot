import logging
import os
import csv
import json
from collections import namedtuple

import api
import dal


TOKEN = 'TOKEN'
FILE_PATH = r'D:\test.csv'

nodes = {}
Node = namedtuple('Node', 'id text next')
users = dal.UsersDatabase()
telegram = api.TelegramBot(TOKEN)

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] - %(levelname)s - %(message)s',
                    handlers = [logging.FileHandler('log.log'),
                                logging.StreamHandler()]
                    )

def load_csv(path):
    with open(path, 'r', encoding='utf-8') as fd:
        reader = csv.reader(fd, delimiter=';')
        for row in reader:
            v, i = '\n', 0
            for item in row[3::2]:
                i += 1
                v += '\n{}. {}'.format(i, item)
            nodes[row[0]] = Node(row[0], row[1] + v, row[2::2])

def message_handler(messages):
    for msg in messages:
        
        user = users.get_user(msg[0])
        if not user:
            users.add_user(msg[0])
            user = [msg[0], '0']
            logging.info('New user!')
        else:
            user = list(user)
        
        if '/stop' in msg[2]:
            users.del_user(user[0])
            logging.info('Delete user!')
            break

        if msg[2].isdigit():
            v = int(msg[2]) - 1
            l = len(nodes[user[1]].next)
            if v < l and v > -1:
                user[1] = nodes[user[1]].next[v]
                users.upd_user(user[0], user[1])

        text = nodes[user[1]].text
        keys = [[str(i+1) for i in range(len(nodes[user[1]].next))]]
        telegram.send(user[0], text, keys)

if __name__ == "__main__":
    
    if os.path.exists(FILE_PATH):
        load_csv(FILE_PATH)
    else:
        logging.error('Data file not found!')
        os.sys.exit(0)
    
    logging.info('Start listening')
    telegram.listen(message_handler)