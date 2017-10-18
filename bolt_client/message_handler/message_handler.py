'''
File: message_handler.py
Description: Handle the incoming message request by calling in the required
             plugin method calls.
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 17/10/2017
'''
import json

class MessageHandler(object):
    """Handle the incoming messages as they arrive

    Message Handler is responsible for taking action on incoming messages by
    calling the necessary actions by the plugins. During this time, the message
    handler also initiates the system statistics collection daemon so as to
    monitor the system statistics and gather the system data.
    """

    def __init__(self, socket_handler, plugin_loader):
        """Initialize the message handler

        Keyword arguments:
        socket_handler -- The socket handler object
        """

        self.socket_handler = socket_handler
        self.message_register = {}

        #Setup the plugin loader
        self.plugin_loader = plugin_loader

        self.socket_handler.register_handler(self.message_handler)

    def message_handler(self, message):
        """Handle the incoming message

        Keyword arguments:
        message -- The incoming message object
        """

        message_data = self.__message_decoder(message)
        message_id = message_data[0]
        plugin_name = message_data[1]
        plugin_payload = message_data[2]

        #Get the plugin executor
        plugin_executor = self.__get_plugin_handler(plugin_name)

        if plugin_executor!= False:
            self.__handover_payload(plugin_executor, plugin_payload)


    def __get_plugin_handler(self, plugin_name):
        """Retrieve the plugin handler responsible for handling the execution

        Keyword arguments:
        plugin_name -- The name of the plugin

        Returns:
            Object on success
            False on failure
        """

        try:
            plugin_executor = self.plugin_loader.get_plugin_executor(plugin_name)
        except KeyError:
            return False

        return plugin_executor

    def __message_decoder(self, message):
        """Decode the message and retrieve the actual data from it

        Our message comes in a special format which contains the server
        generated message id and the plugin payload. Message decoder is
        responsible for decoding the message packet and segragating the plugin
        and the payload

        Keyword arguments:
        message -- The incoming message packet

        Returns:
            List
        """

        message_json = json.loads(message)
        message_id = message_json['id']
        message_payload = message_json['payload']
        plugin_name = message_payload['plugin_name']

        return [message_id, plugin_name, message_payload]

    def __handover_payload(self, plugin_executor, payload):
        """Handover the payload to the plugin executor

        Once we have processed the payload, we should hand it over to the plugin
        that deals with it. The method should block until the call from the
        handover returns.

        Keyword arguments:
        plugin_executor -- The plugin object
        payload -- The payload that needs to be handed over to the plugin

        Returns:
            Bool
        """

        #Initialize the executor class of the plugin
        executor = plugin_executor()

        #Check if the plugin has a valid payload handler or not and then handover
        #the payload to the handler
        plugin_methods = dir(executor)

        if 'handle_payload' not in plugin_methods:
            return False

        executor.handle_payload(payload)
        return True
