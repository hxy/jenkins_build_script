# -*- coding: utf-8 -*-
import sys
import FileUtil
import re
import requests
import json
# 路径
cur_path = sys.path[0]  # 脚本目录
plugin_src_path = cur_path + '/ydplugin'  # 代码路径
plugin_path = plugin_src_path + '/replugin' # replugin code
plugin_gradle_path = plugin_path+'/%s/build.gradle' #gradle文件路径

NOT_PLUGINS = ['Host','Module','Plugin1','replugin-host-lib','replugin-plugin-lib']

TOOLS_TEST_URL = 'http://a4-1.go2yd.com/Website/config/shared-data?key=520aa5fe37ffcb3cd40fa5e6b871a085&id=TEST_YIDIAN_ANDROID_PLUGIN_V2&opt=read' # 工具测试环境
TOOLS_ONLINE_URL ='http://a4.go2yd.com/Website/config/shared-data?key=520aa5fe37ffcb3cd40fa5e6b871a085&id=YIDIAN_ANDROID_PLUGIN_V2&opt=read' # 工具正式环境


def get_version(plugin_name):
    path = plugin_gradle_path % plugin_name
    #versionCode 104
    p = re.compile(r'\s*versionCode\s*(\d+).*')
    lines = FileUtil.readcontent(path)
    for line in lines:
      m = p.match(line)
      if m:
        return m.group(1)
    return ''

  #获取版本号
def get_version1(plugin_name):
    path = plugin_gradle_path % plugin_name
    version_name_reg = re.compile('(?<=versionCode).*')
    number_reg = re.compile('(\d+)')
    lines = FileUtil.readcontent(path)
    for line in lines:
        if version_name_reg.search(line.strip()) is not None:
            remain_text = version_name_reg.search(line).group()
            return number_reg.search(remain_text).group()
    return ''

def get_name(plugin_name):
    path = plugin_gradle_path % plugin_name
    # def app_name = "huaweiplug"
    p = re.compile(r'\s*def\s*app_name\s*=\s*"(\w+)".*')
    lines = FileUtil.readcontent(path)
    for line in lines:
        m = p.match(line)
        if m:
            return m.group(1) # 第一个括号内的字符串
    return ''

def get_page_name(plugin_name):
    path = plugin_gradle_path % plugin_name
    # applicationId "com.yidian.news.huaweiplug"
    p = re.compile(r'\s*applicationId\s*"([\w|\.]+)".*')
    lines = FileUtil.readcontent(path)
    for line in lines:
        m = p.match(line)
        if m:
            return m.group(1)
    return ''

def get_url_content(url,code_appid):
    res=requests.get(url)
    res.encoding='utf-8'
    s = res.json()
    dict = {}
    #print s
    #print s.keys()
    list =  s[u'data'] #
    list = json.loads(list) #
    for i in list:  #
        appid = i['appid']
        #print code_appid
        if(code_appid in appid.split('|')):
           # print i
            package = i['package_name']
            version = i['version']
            if(package in dict.iterkeys()):
                dict[package] = max(version,dict[package])
            else:
                dict[package] = version
   # print 'url=',url,dict
    return dict

def compare(tag,code,tools):
    diff = code.keys() and tools.keys()
    isPluginOK = True
    for k in diff:
       # print k
        if k in code.keys() and k in tools.keys() and code[k] != tools[k]:
            isPluginOK = False
            print 'package name =',k,'codeVersion=',code[k],tag,'viersion=',tools[k]
    if isPluginOK:
        print 'code plugin version is matching ',tag




