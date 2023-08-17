import json
from pika.adapters.blocking_connection import BlockingChannel

from rmq.send.tg_login import tele_login_t
from tg.loginer import user_loginer


def obtain_login_handler(channel: BlockingChannel):
    tele_login = tele_login_t(channel)

    login_data_by_user_id = {}

    def handle_login(ch: BlockingChannel, method, properties, body):


        data = json.loads(body)

        print(" [x] %r:%r" % (method.routing_key, body))

        action = data['type']
        user_id = data['user_id']

        print(action)

        if action == 'login_init':
            tele_login.request_number(user_id)

        elif action == 'pass_phone':
            phone = data['phone']

            loginer = user_loginer(user_id, phone)
            login_data_by_user_id[user_id] = loginer
            loginer.start()

        elif action == 'pass_code':
            loginer: user_loginer = login_data_by_user_id[user_id]
            loginer.put_code(data['code'])

        elif action == 'pass_password':
            loginer: user_loginer = login_data_by_user_id[user_id]
            loginer.put_password(data['password'])


    return handle_login
