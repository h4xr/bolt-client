'''
File: collectors.py
Description: System metric collectors
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 18/10/2017
'''
from structures import Metric
import psutil
import time

class CpuCollector(Metric):
    """CPU Metrics collector

    Collects the CPU metrics such as percent utilization, IOwait, nice and IRQ
    """

    def __init__(self, sampling_rate=5):
        """Initialize the CpuCollector instance

        Keyword arguments:
        sampling_rate -- The time interval between successive data collection
        """

        super(CpuCollector, self).__init__('cpu', sampling_rate)

    def start_sampling(self):
        """Start sampling the data"""

        cpu_times = psutil.cpu_times()
        timestamp = time.time()
        user = cpu_times.user
        system = cpu_times.system
        nice = cpu_times.nice
        idle = cpu_times.idle
        iowait = cpu_times.iowait
        irq = cpu_times.irq
        softirq = cpu_times.softirq

        self.record_data('user', timestamp, user)
        self.record_data('system', timestamp, system)
        self.record_data('nice', timestamp, nice)
        self.record_data('idle', timestamp, idle)
        self.record_data('iowait', timestamp, iowait)
        self.record_data('irq', timestamp, irq)
        self.record_data('softirq', timestamp, softirq)

class MemoryCollector(Metric):
    """Memory metrics collector

    Collects the memory metrics such as total memory, available and used memory,
    etc.
    """

    def __init__(self, sampling_rate=5):
        """Initialize the Memory collector instance

        Keyword arguments:
        sampling_rate -- The time interval between successive data collections
        """

        super(MemoryCollector, self).__init__('memory', sampling_rate)

    def start_sampling(self):
        """Start the data collection and recording of the data"""

        virtual_memory = psutil.virtual_memory()
        timestamp = time.time()

        used_mem = virtual_memory.used
        free_mem = virtual_memory.free
        cached_mem = virtual_memory.cached
        shared_mem = virtual_memory.shared

        self.record_data('used', timestamp, used_mem)
        self.record_data('free', timestamp, free_mem)
        self.record_data('cached', timestamp, cached_mem)
        self.record_data('shared', timestamp, shared_mem)
