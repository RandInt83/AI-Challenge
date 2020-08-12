# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:46:26 2020

@author: chris
"""
class TimeOutException(Exception):
    def __init__(self, message, errors):
        super(TimeOutException, self).__init__(message)
        self.errors = errors

def timeouthandler(signum, frame):
    raise TimeOutException