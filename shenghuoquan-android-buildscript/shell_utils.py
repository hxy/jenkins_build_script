#!/usr/bin/env python
import os
import subprocess
import signal
import pwd
import sys
 

class Shell:
    def __init__(self, cmd):
        self.cmd = cmd 
        self.ret_code = None
        self.ret_info = None
        self.err_info = None
         
    def run_background(self):
        self._process = subprocess.Popen(self.cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         
    def run(self):
        self.run_background()
        self.wait()

    def wait(self):
        self.ret_info, self.err_info = self._process.communicate()
        self.ret_code = self._process.returncode
        
if __name__ == '__main__':
    shell = Shell("echo $ANDROID_HOME")
    shell.run()
    print shell.err_info, shell.ret_code, shell.ret_info
    
    shell2 = Shell("adb devices")
    shell2.run()
    print shell2.err_info, shell2.ret_code, shell2.ret_info
