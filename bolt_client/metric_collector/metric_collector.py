'''
File: metric_collector.py
Description: Metric collection daemon
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 17/10/2017
'''
from collector_loader import CollectorLoader
import time
import threading

class MetricCollector(object):
    """Metric collection orchestrator

    Figures out the various collectors that are present and loads them for
    collection of metrics. The collected metrics are then retrieved and send as
    a single package.
    """

    def __init__(self):
        """Initialize the metric collector

        Setups the metric collector for the collection of the metrics
        """

        self.collector_loader = CollectorLoader()

        #Load the collectors
        self.collector_loader.load_collectors()
        self.metric_collectors = self.collector_loader.get_collectors()

    def start_sampling(self):
        """Start the metric sampling"""

        self.__collector_initializer()
        self.__thread_preparer()

        self.sampler = True

        for thread in self.collector_threads:
            thread.start()

    def stop_sampling(self):
        """Stop the sampling and gather the collected results

        Returns:
            Dict
        """

        self.sampler = False

        for thread in self.collector_threads:
            thread.join()

        results = self.__get_results()
        return results

    def __get_results(self):
        """Gather the results of the metric collection and return them

        Returns:
            Dict
        """

        data = {}
        for collector in self.collector_instances:
            collector_name = collector.get_collector_name()
            collector_data = collector.get_data()
            for metric in collector_data.keys():
                metric_name = collector_name + '.' + metric
                data[metric_name] = collector_data[metric]

        return data

    def __metric_collector(self, target_method, sampling_rate):
        """Launch the metric collector method

        Keyword arguments:
        target_method -- The method to be called for the data collection
        sampling_rate -- The rate at which samples should be collected
        """

        while self.sampler:
            target_method()
            time.sleep(sampling_rate)

    def __collector_initializer(self):
        """Initialize the collectors"""

        self.collector_instances = []
        for collector in self.metric_collectors:
            self.collector_instances.append(collector())

    def __thread_preparer(self):
        """Prepares the threads for the execution

        Prepares and keeps a track of threads for metric collection purpose
        """

        self.collector_threads = []

        for collector_instance in self.collector_instances:
            sampling_rate = collector_instance.get_sampling_rate()
            t = threading.Thread(target=self.__metric_collector, args=(collector_instance.get_sample, sampling_rate,))
            t.daemon = True
            self.collector_threads.append(t)
