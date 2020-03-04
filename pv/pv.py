"""
    This service receives data from message broker(RabbitMQ) and inserts them in the file output.txt located in the
    output folder.
    I have assumed that PV value is equal to 75% of meter value.
"""

import json
import os

from connection_handler import connection_handler


def get_output_path():
    output_path = os.path.join('output')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_path = os.path.join(output_path, 'output.txt')
    return output_path


def callback(ch, method, properties, body):
    message = json.loads(body)
    pv_val = round(message['Meter Value'] * 0.75, 3)
    total = round(message['Meter Value'] + pv_val, 3)
    with open(get_output_path(), 'a') as output:
        output.write('%-30s %-20s %-10s %10s\n' % (message['Timestamp'], message['Meter Value'], pv_val, total))


def main():
    try:
        print('PV Simulator...')
        with open(get_output_path(), 'w') as output:
            output.write('%-30s %-20s %-10s %10s\n' % ('Timestamp', 'Meter_Value', 'PV_Value', 'Total'))

        receiver = connection_handler(broker_address='rabbitmq', queue_name='messages')
        receiver.create_connection()
        print('Waiting for messages...')
        while True:
            receiver.receive_message(callback)
    except KeyboardInterrupt:
        pass  # exit gracefully when interrupted with CTRL+C


if __name__ == '__main__':
    main()
