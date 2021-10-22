# -*- coding: utf-8 -*-

import os
import FileUtil
import PluginUtils
from Util import shell
from PluginUtils import cur_path, plugin_src_path,plugin_gradle_path,plugin_path,NOT_PLUGINS,TOOLS_TEST_URL,TOOLS_ONLINE_URL


def pullCode( ):
    needClone = True
    if os.path.isdir(plugin_src_path):
        shell('cd %s' % plugin_src_path)
        if os.path.isdir(plugin_src_path + '/.git') and shell('git reset --hard', output=False) == 0:
            #print('It is a valid git respository. Update it')
            shell('git clean -d -x -f')
            shell('git checkout master')
            shell('git pull')
            shell("cd ..")
            needClone = False
        else:
            print('Not a valid git repository. Delete folder ' + plugin_src_path)
            shell("cd ..")
            FileUtil.delete(plugin_src_path)

    if needClone:
        shell('git clone https://umeng-dev@git.yidian-inc.com:8021/android/yd-replugins.git ' + plugin_src_path + ' --recursive')
        shell('cd %s' % plugin_src_path)
        shell('git checkout master')
        shell('cd ..')

    shell('cd %s' % plugin_src_path)

def get_code_version():
    files = os.listdir(plugin_path)
    dict = {}
    for f in files:
        if(os.path.isdir(plugin_path + '/' + f) and not (f in NOT_PLUGINS)):
            #print ('current plugin is ',f)
            version = PluginUtils.get_version(f)
            #print version
            name = PluginUtils.get_page_name(f)
            #print name
            if(version!='' and name!=''):
                dict[name] = version
    #print 'code version = ',dict
    return dict


def check_plugin_verison(code_appid):
    FileUtil.mkdirs(plugin_src_path)
    pullCode()
    code_plugin_verison = get_code_version()
    testlist = PluginUtils.get_url_content(TOOLS_TEST_URL,code_appid)
    onlinelist = PluginUtils.get_url_content(TOOLS_ONLINE_URL,code_appid)
    PluginUtils.compare("testConifg",code_plugin_verison,testlist)
    PluginUtils.compare("onlineConfig",code_plugin_verison,onlinelist)


if __name__ == '__main__':
    FileUtil.mkdirs(plugin_src_path)
    pullCode()
    code_plugin_verison = get_code_version()
    testlist = PluginUtils.get_url_content(TOOLS_TEST_URL,"local")
    onlinelist = PluginUtils.get_url_content(TOOLS_ONLINE_URL,"local")
    PluginUtils.compare("testConifg",code_plugin_verison,testlist)
    PluginUtils.compare("onlineConfig",code_plugin_verison,onlinelist)




