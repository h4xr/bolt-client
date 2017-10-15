'''
File: socket_handler.py
Description: Socket handling mechanism for the bolt client
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 13/10/2017
'''
import os
import socket
import threading

class SocketHandler(object):
    """Socket handling mechanism for the bolt client

    Socket Handler is responsible for handling the connection to the bolt server
    and bolt data sink. The socket client runs two threads, one for listening
    to the messages being sent by the bolt server and one thread for handling
    the sending of the data from the client to the bolt sink.
    """

    def __init__(self):
        """Initialize the socket handler for use with the bolt client"""

        self.bolt_server_host = os.getenv('BOLT_SERVER_HOST', '127.0.0.1')
        self.bolt_server_port = os.getenv('BOLT_SERVER_PORT', 5200)
        self.bolt_subscribe_topics = os.getenv('BOLT_SUBSCRIBE_TOPICS', 'Test')
        self.bolt_sink_host = os.getenv('BOLT_SINK_HOST', '127.0.0.1')
        self.bolt_sink_port = os.getenv('BOLT_SINK_PORT', 5201)
        self.bolt_client_host = str(socket.gethostname())

        #Setup the always listen flag to true
        self.listen = True

        #Register the generic message handler
        self.register_handler(self.__generic_message_handler)

    def register_handler(self, handler):
        """Regsiter a new message handler to handle the incoming messages

        Keyword arguments:
        handler -- Message handling object
        """

        self.message_handler = handler

    def start_client(self, publisher=False):
        """Start the bolt execution client

        Keyword arguments:
        publisher -- Flag to enable or disable the publisher
        """

        self.listener_thread = threading.Thread(target=self.__start_bolt_listener)
        self.listener_thread.daemon = True
        self.listener_thread.start()

        self.publisher_thread = None

        if publisher:
            self.publisher_thread = threading.Thread(target=self.__start_bolt_publisher)
            self.publisher_thread.daemon = True
            self.publisher_thread.start()

    def stop_listening(self):
        """Stop listening to the incoming messages"""

        self.listen = False
        self.listener_thread.join()
        if self.publisher_thread != None:
            self.publisher_thread.join()

    def __start_bolt_listener(self):
        """Start the listener service

        Connect to the bolt server and start listening to the messages
        """

        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.connect((self.bolt_server_host, self.bolt_server_port))
        self.__subscribe_topics()

        #We have subscribed to topics now, let's enter a listening loop
        while self.listen:
            message = self.listener.recv(32000)
            if not message:
                continue
            self.message_handler(message)

    def __start_bolt_publisher(self):
        """Start the bolt publishing service

        Connect to the bolt sink and start publishing results as they arrive
        TODO: Implement our packet reporting mechanism
        """

        self.publisher = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.publisher.connect((self.bolt_sink_host, self.bolt_sink_port))

    def __subscribe_topics(self):
        """Send the handshake message to the bolt server and subscribe to topics
        """

        self.listener.sendall(self.bolt_subscribe_topics + ':' + self.bolt_client_host)

    def __generic_message_handler(self, message):
        """A generic message handler which just prints the incoming data

        Keyword arguments:
        message -- The incoming message
        """

        print message
