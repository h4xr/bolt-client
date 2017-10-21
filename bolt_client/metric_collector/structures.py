'''
File: structures.py
Description: Metric collection structures
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 18/10/2017
'''

class Metric(object):
    """Hold the details about the metric"""

    def __init__(self, collector_name, sampling_rate=5):
        """Initialize the metric object

        Keyword arguments:
        metric_name -- The name of the metric
        sampling_rate -- The sampling interval at which metric should be collected
        """

        self.collector_name = collector_name
        self.sampling_rate = sampling_rate
        self.metric_data = {}

    def change_sampling_rate(self, sampling_rate):
        """Change the sampling rate

        Keyword arguments:
        sampling_rate -- The new rate of sampling
        """

        self.sampling_rate = sampling_rate

    def record_data(self, metric_name, metric_time, metric_value):
        """Record the new set of data

        Keyword arguments:
        metric_name -- The name of the metric
        metric_time -- The timestamp for the metric
        metric_value -- The value for the metric
        """

        if metric_name not in self.metric_data.keys():
            self.metric_data[metric_name] = []

        metric = (metric_time, metric_value)
        self.metric_data[metric_name].append(metric)

    def get_sampling_rate(self):
        """Get the sampling rate for the metric

        Returns:
            Int
        """

        return self.sampling_rate

    def get_collector_name(self):
        """Return the name of the collector

        Returns:
            String
        """

        return self.collector_name

    def get_data(self):
        """Retrieve the data stored for the metric

        Returns:
            List
        """

        return self.metric_data
