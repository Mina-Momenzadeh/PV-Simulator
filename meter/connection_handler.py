import pika


class connection_handler:
    """
    This class handles the connection with message broker.

    Attributes
    ----------
    broker_address: str
        The address of RabbitMQ service.
    channel
        Channel used for interacting with RabbitMQ
    queue_name: str
        Name of the message queue in broker.
    """

    def __init__(self, broker_address, queue_name):
        self.broker_address = broker_address
        self.channel = None
        self.queue_name = queue_name

    def create_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.broker_address))
        self.channel = connection.channel()
        self.channel.queue_declare(self.queue_name)

    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)

    def receive_message(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
