'''
File: collector_loader.py
Description: Common interface to load the different collectors
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 21/10/2017
'''

class CollectorLoader(object):
    """Common interface for loading the collectors"""

    def __init__(self):
        """Initialize the collector loader"""

        self.collectors = []

    def get_collectors(self):
        """Get the list of collectors

        Returns:
            List
        """

        return self.collectors

    def load_collectors(self):
        """Load the collectors

        We implement a number of collectors to collect the system metrics. Before
        we get them to function, we need to validate if the collectors are valid
        and then load them.
        """

        #Before we start loading the collectors, we need to get a list of available ones
        collector_list = self.__get_collector_list()

        #Start validating and loading the valid collectors
        for collector in collector_list:
            if self.__validate_collector(collector):
                self.__load_collector(collector)

    def __load_collector(self, collector_name):
        """Load the definition of the collector and store it

        Keyword arguments:
        collector_name -- The name of the collector to be loaded
        """

        collector = getattr(self.collector_module, collector_name)
        self.collectors.append(collector)

    def __load_collector_module(self):
        """Loads the collector module"""

        self.collector_module = __import__('bolt_client.metric_collector.collectors', fromlist=['*'])

    def __get_collector_list(self):
        """Retrieve the list of collectors from the collectors module

        Returns:
            List
        """

        return dir(collector_module)

    def __validate_collector(self, collector_name):
        """Validate if the provided collector name is a valid collector or not

        We have several rules which must be validated before a collector can be
        used to collect the metrics. The method checks the provided collector
        for the validation of these rules and returns a boolean indicating if
        the provided collector is a valid collector or not.

        Keyword arguments:
        collector_name -- The name of the collector to be validated

        Returns:
            Bool
        """

        collector = getattr(self.collector_module, collector_name)
        if 'start_sampling' not in dir(collector):
            return False
        return True
