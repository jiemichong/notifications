import json
import mysql.connector
import amqp_setup
import smtp_setup
from os import environ
from urllib.parse import urlparse


db_url = urlparse(environ.get('db_conn'))


def callback(channel, method, properties, body):
    message_body = json.loads(body)
    email = message_body['email']
    message = message_body['message']
    print(message_body)
    print(message)

    message_subject = message['subject']
    message_text = message['message']
    message_to_send = ("From: %s\r\n" % smtp_setup.SENDER_EMAIL
                       + "To: %s\r\n" % email
                       + "Subject: %s\r\n" % message_subject
                       + "\r\n"
                       + message_text)

    message_to_db = ('subject: ' + message_subject +
                     ", message: " + message_text)

    try:
        cnx = mysql.connector.connect(
            user=db_url.username,
            password=db_url.password,
            host=db_url.hostname,
            port=db_url.port,
            database='notification'
            )

        cursor = cnx.cursor()

        cursor.execute('''
            INSERT INTO `notification` (`email`, `message`)
            VALUES (%s, %s);
            ''', (email, message_to_db))

        cnx.commit()
        cnx.close()

        server = smtp_setup.server
        if smtp_setup.PASSWORD != "notest":
            try:
                # server.starttls()
                print(f"SENDING EMAIL : email: {email}, "
                      "message: " + message_to_send)
                server.sendmail(smtp_setup.SENDER_EMAIL, email,
                                message_to_send)
            except Exception as _e:
                print(f"SMTP FAIL,{email}, {message_to_send},{_e}\n")

        print(f"SUCCESS,{email},{message_text}\n")

    except mysql.connector.Error as err:
        print(f"FAIL,{email},{message_text},{err}\n")


amqp_setup.channel.basic_consume(
    queue=amqp_setup.queue_name, on_message_callback=callback, auto_ack=True)
amqp_setup.channel.start_consuming()
