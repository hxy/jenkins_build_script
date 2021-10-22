#!/usr/bin/env python
import os
import sys
import unittest
import argparse
import re
from appium import webdriver
from shell_utils import Shell
from UiWaitUtils import WaitUtils
from selenium.common.exceptions import NoSuchElementException

device_serial_num = '35379805'
webdriver_addr = 'http://0.0.0.0:4723/wd/hub'
inject_num = 30000
interval = 100

def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('-apk', '--APK File', dest = 'apk', help = 'Please input the location of APK file')
        parser.add_argument('-pkg', '--Package Name', dest = 'pkg_name', help = 'Please input the package name of the target app')
        parser.add_argument('-activity', '--Launch Activity', dest = 'launch_activity', help = 'Please input the launch activity of the target app')
        parser.add_argument('-output', '--Output File', dest = 'output_file', help = 'Please input the output file which Monkey result will redirect to')
        args = parser.parse_args()
        return args.apk, args.pkg_name, args.launch_activity, args.output_file

def check_device_state():
        cmd = 'adb devices'
        shell = Shell(cmd)
        shell.run()
        if not shell.ret_code == 0:
                print "Can't check device state with adb devices command"
                sys.exit()
        it = re.compile('([0-9A-Za-z])+\s+([A-Za-z])+').finditer(shell.ret_info)
        for m in it:
                line = m.group()
                if line.find(device_serial_num) > -1 and line.find('device') > -1:
                        return
        print "Can't find device %s"%device_serial_num
        sys.exit()
        
        
class MonkeyAutomation:
    def validation(self):
        if not os.path.isfile(self.apk) or self.apk.split('.')[-1] not in ['apk', 'APK']:
            print 'The source APK file you provided is invalid !'
            sys.exit()
        
        output = self.output_file
        if os.path.exists(output):
                if os.path.isfile(output):
                        os.remove(output)
                elif os.path.isdir(output):
                        print "Please provide output FILE name, not dir name!"
                        sys.exit()
        else:
                dirname = os.path.dirname(output)
                if not os.path.exists(dirname):
                        os.makedirs(dirname)
                if not os.path.exists(dirname):
                        print "Can't create dir"
                        sys.exit()                    
    
    def init_appium_session(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = device_serial_num
        desired_caps['app'] = self.apk
        desired_caps['appPackage'] = self.pkg_name
        desired_caps['appActivity'] = self.launch_activity
        self.driver = webdriver.Remote(webdriver_addr, desired_caps)
        
    def close_appium_session(self):
        self.driver.close()
    
    def ensure_yidian_installed(self):
        print 'ensure_yidian_installed'
        print self.driver.is_app_installed(self.pkg_name)
        if not self.driver.is_app_installed(self.pkg_name):
            print 'Can\'t find target package'
            sys.exit()
    
    def close_permission_request_popups(self):
        print 'close_permission_request_popups'
        if self.wait_for_grant_permission():
                wait_for_element = WaitUtils(self.driver)
                while True:
                    ele = wait_for_element.wait_for_element('new UiSelector().resourceId("android:id/button1")', 1)
                    print ele
                    if ele:
                        ele.click()
                    else:
                        break
    def wait_for_grant_permission(self):
        wait_for_activity = WaitUtils(self.driver)
        return wait_for_activity.wait_for_activity('GrantPermissionsActivity', 5)

    def close_interest_choose_dialog(self):
        if self.wait_for_navibar():
               wait_for_element = WaitUtils(self.driver)
               ele = wait_for_element.wait_for_element('new UiSelector().resourceId("%s:id/ivClose")'%self.pkg_name, 1)
               print ele
               if ele:
                ele.click()
    
    def wait_for_navibar(self):
        wait_for_activity = WaitUtils(self.driver)
        return wait_for_activity.wait_for_activity('NavibarHomeActivity', 5)
        
    def start_appium(self):
        shell = Shell("appium &")
        shell.run_background()

    def run_monkey(self):
        cmd = 'adb shell monkey -p {0} {1} -v 100 --throttle {2} --ignore-crashes --ignore-timeouts --monitor-native-crashes >> {3}'.format(self.pkg_name,inject_num,interval,self.output_file)
        print cmd
        shell = Shell(cmd)
        shell.run()

if __name__ == '__main__':
    check_device_state()
    
    monkey = MonkeyAutomation()
    monkey.apk, monkey.pkg_name, monkey.launch_activity, monkey.output_file = parse_args()
    monkey.validation() 
    monkey.start_appium()
    monkey.init_appium_session()
    monkey.ensure_yidian_installed()
    monkey.close_permission_request_popups()
    monkey.close_interest_choose_dialog()
    monkey.run_monkey()
    monkey.close_appium_session()