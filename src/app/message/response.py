# -*- coding: utf-8 -*-

"""
.. module:: response
   :synopsis: A module for embracing the templates of response messages.

.. moduleauthor:: George T. C. Lai
"""

import abc
import psutil


class ABCMessage(metaclass=abc.ABCMeta):
    """The abstract class of messages.

    :param metaclass: declare a metaclass by means of Python abc module, defaults to abc.ABCMeta
    :type metaclass: [type], optional
    :return: [description]
    :rtype: [type]
    """
    @property
    @abc.abstractmethod
    def message(self):
        """The method implementation to get the corresponding message.

        :return: `dict` This function returns the corresponding message result..
        :rtype: dict
        """
        return NotImplemented

class HealthCheckResponse(ABCMessage):
    """The response message with respect to health check.
    
    :param ABCMessage: [description]
    :type ABCMessage: [type]
    :return: [description]
    :rtype: [type]
    """


    def __init__(self):
        self.cpu_info = psutil.cpu_times_percent()
        self.cpu_count = psutil.cpu_count()
        self.mem_info = psutil.virtual_memory()
        self.swap_info = psutil.swap_memory()
        self.disk_info = psutil.disk_usage('/')

    @property
    def message(self):
        msg = {
            "cpu": {
                "count": self.cpu_count,
                "user": self.cpu_info.user,
                "system": self.cpu_info.system,
                "idle": self.cpu_info.idle,
            },
            "memory": {
                "total": self.mem_info.total,
                "used": self.mem_info.used,
                "free": self.mem_info.free,
                "available": self.mem_info.available,
                "percent": self.mem_info.percent
            },
            "swap": {
                "total": self.swap_info.total,
                "used": self.swap_info.used,
                "free": self.swap_info.free,
                "percent": self.swap_info.percent
            },
            "disk": {
                "total": self.disk_info.total,
                "used": self.disk_info.used,
                "free": self.disk_info.free,
                "percent": self.disk_info.percent
            }
        }
        return msg
