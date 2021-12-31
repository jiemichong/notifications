import pika

hostname = 'localhost'
port = 5672

parameters = pika.ConnectionParameters(host=hostname,
                                       port=port
                                       )

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
exchangename = "notifications.topic"
exchangetype = "topic"
channel.exchange_declare(exchange=exchangename,
                         exchange_type=exchangetype, durable=True)

queue_name = 'Customer_Notifications'
channel.queue_declare(queue=queue_name, durable=True)

channel.queue_bind(exchange=exchangename,
                   queue=queue_name, routing_key='booking.*')

channel.basic_publish(
    exchange=exchangename, routing_key="booking.new",
    body='''{ "email": "potatoesops@gmail.com", "message": {"subject" : "Booking Confirmation" , "message": "Your booking has been confirmed for the following date: . Thank you."} }''',
    properties=pika.BasicProperties(delivery_mode=2))

connection.close()
