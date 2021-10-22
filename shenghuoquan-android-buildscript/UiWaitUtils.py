#!/usr/bin/env python
import time
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

class WaitUtils:
    def __init__(self, driver):
        self.driver = driver
        self.default_interval = 1
    
    def wait_for_element(self, condition, retry_count):
        i = 0
        while i < retry_count :
            try:
                i = i + 1
                ele = self.driver.find_element_by_android_uiautomator(condition)
                if ele.is_displayed():
                    return ele
            except NoSuchElementException, e:
                time.sleep(self.default_interval)
        return None
    
    def wait_for_activity(self, name, retry_count):
        i = 0
        while i < retry_count :  
            i = i + 1
            print self.driver.current_activity, self.driver.current_activity.find(name)
            if self.driver.current_activity.find(name) > -1:
                return True
            else :
                time.sleep(self.default_interval)
        return False
    