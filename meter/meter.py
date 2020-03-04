"""
    This service generates random normal numbers and sends them in json format to RabbitMQ. Sent data is logged in a
    file named meter.log in the log folder.
    The first half of the generated data is sorted ascending and the second part is sorted descending.
    This is done as a way of simulating daily usage profile.
    All the random numbers are generated at once and are sent with a timestamp which is calculated based on the
    current timestamp with 5 seconds difference. It means that except the first timestamp, all the other times are
    generated manually in order to save time.
"""

import json
import logging
import os
from datetime import datetime
from datetime import timedelta
import numpy

from connection_handler import connection_handler

stop_generation = False


def generate_messages():
    mu, sigma = 3, 1.5
    sample_count = 24 * 60 * 60 // 5
    middle_index = sample_count // 2

    values = numpy.random.randn(sample_count) * sigma + mu
    values[0:int(middle_index)].sort()
    values[int(middle_index):sample_count] = sorted(values[int(middle_index):sample_count], reverse=True)
    return values


def send_messages(values, sender):
    sample_time = datetime.now()
    midnight = sample_time.replace(hour=0, minute=0, second=0, microsecond=0)

    for v in values:
        seconds = (sample_time - midnight).seconds  # Time passed from midnight
        index = seconds // 5
        value = round(values[index], 3)
        if value > 9:
            value = 9.0
        if value < 0:
            value = 0.0

        message = json.dumps({'Timestamp': str(sample_time), 'Meter Value': value})
        sender.send_message(message)
        logging.info(message)
        sample_time = sample_time + timedelta(seconds=5)

    stop_generation = True


def main():
    try:
        print('Meter Simulator...')

        log_path = os.path.join('log')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_path = os.path.join(log_path, 'meter.log')
        log_format = '%(asctime)-15s %(message)s'
        logging.basicConfig(filename=log_path, format=log_format, level=logging.INFO)

        sender = connection_handler(broker_address='rabbitmq', queue_name='messages')
        sender.create_connection()
        print('Sending messages started...')
        while True:
            if not stop_generation:  # It only produces numbers for 24 hours
                values = generate_messages()
                send_messages(values, sender)
    except KeyboardInterrupt:
        pass  # exit gracefully when interrupted with CTRL+C


if __name__ == '__main__':
    main()
