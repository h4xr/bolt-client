'''
File: structures.py
Description: Metric collection structures
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 18/10/2017
'''

class Metric(object):
    """Hold the details about the metric"""

    def __init__(self, metric_name, sampling_rate=5):
        """Initialize the metric object

        Keyword arguments:
        metric_name -- The name of the metric
        sampling_rate -- The sampling interval at which metric should be collected
        """

        self.metric_name = metric_name
        self.sampling_rate = sampling_rate
        self.metric_data = []

    def change_sampling_rate(self, sampling_rate):
        """Change the sampling rate

        Keyword arguments:
        sampling_rate -- The new rate of sampling
        """

        self.sampling_rate = sampling_rate

    def record_data(self, metric):
        """Record the new set of data

        Keyword arguments:
        metric -- Tuple signifying current timestamp and metric value
        """

        self.metric_data.append(metric)

    def get_data(self):
        """Retrieve the data stored for the metric

        Returns:
            List
        """

        return self.metric_data
