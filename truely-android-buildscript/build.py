# -*- coding: utf-8 -*-

import os
import sys
import shutil
import json
import subprocess
import Command
import Data
import FileUtil
import Util
import datetime
from Util import Properties
import requests
from Data import YIDIAN, UNSIGNED, SERVER_A1, SERVER_A3, SERVER_PRE
# from Data import archive_path_dst as apk_dst
# from Data import archive_path_unsigned_dst as unsigned_apk_dst
# from Data import archive_path_unsigned_src as unsigned_apk_src
# from Data import archive_patch_log

from Data import cur_path, src_path, flutter_src_path, archive_path, short_flavor, short_buildtype, \
    module_gradle_path, proj_gradle_path, gradle_properties_path, application_gradle_path, \
    library_gradle_path, mapping_dst, mapping_src, apk_path, metadata_path, web_root_dir, web_target_dir_unsigned, web_location_dir_unsigned, web_terminal
from Util import shell

timestamp = ""
version_name = ""

def config():
    gitandroid, androidbranch, gitflutter, flutterbranch, product, is_debug_as_release = Util.arrangeArguments(
        sys.argv)
    return Command.CompileCommand('None', gitandroid, androidbranch, gitflutter, flutterbranch, product)


def checkout(path, branch, gitsource, isflutter):
    print('---Current directory----')
    print(shell('pwd'))

    print('Start syncing git repository...')
    needClone = True
    if os.path.isdir(path):
        print('Folder %s exits. Check whether it is a git repository' % path)
        # Check if this is a valid git repository
        shell('cd %s' % path)
        if os.path.isdir(path + '/.git') and shell('git reset --hard', output=False) == 0:
            print('It is a valid git respository. Update it')
            # 如果flutter module没有.android或者是Android主工程则执行clean
            if os.path.isdir(path + '/.android')==False:
                shell('git clean -d -x -f')
            shell('git checkout %s' % branch)
            shell('git pull')
            print('-------last commit log:------')
            print('%s' % shell('git log --oneline -1'))
            if isflutter==True:
                if os.path.isdir(path + '/.android')==True:
                    shell('flutter pub get')
                else:
                    shell('flutter build aar')
            else:
                create_local_properties()
                shell('gradle wrapper')
            shell("cd ..")
            needClone = False
        else:
            print('Not a valid git repository. Delete folder ' + path)
            shell("cd ..")
            FileUtil.delete(path)

    if needClone:
        # https://git.yidian-inc.com:8021/android/ydnews.git 原地址 这个地址一直拉不下代码，测试建议换成 https://umeng-dev@git.yidian-inc.com:8021/android/ydnews.git就可以拉下代码，原因不明
        shell('git clone ' + gitsource + ' ' + path + ' --recursive')
        shell('cd %s' % path)
        shell('git checkout %s' % branch)
        print('-------last commit log:------')
        print('%s' % shell('git log --oneline -1'))
        if isflutter:
            shell('flutter build aar')
        else:
            create_local_properties()
            shell('gradle wrapper')
        shell('cd ..')

    # 增加下面两行命令是发现checkout下来的项目中， protco、www 子项目没有代码，所以重新获取子项目代码
    shell('git submodule update --init --recursive ')
    shell('git submodule update --recursive')
    shell('git submodule update --recursive ')
    if isflutter == False:
        shell('cd %s' % path)
        shell('chmod 777 gradlew')
        sub_modules_checkout(path)

    # copy properties and keystore NOT FOR OPPO
    # if cc.sign == UNSIGNED:
    #     print("unsigned")
    #     # FileUtil.delete('%s/signing.properties' % src_path)
    #     FileUtil.delete('%s/cutt.android.keystore' % src_path)
        # shell(
        #     "perl -p -i -e '{s/signingConfig signingConfigs\.debug//g}' " + application_gradle_path)
        # shell(
        #     "perl -p -i -e '{s/signingConfig signingConfigs\.release//g}' " + application_gradle_path)
    # else:
        # FileUtil.copy('../signing.properties', '%s/signing.properties' % src_path)
        # FileUtil.copy('../cutt.android.keystore',
        #               '%s/cutt.android.keystore' % src_path)


def sub_modules_checkout(path):
    properties = Properties(path + '/gradle.properties').getProperties()
    if 'submodule' in properties.keys():
        submodule = properties['submodule']
        for key in  submodule:
            module = submodule[key]
            module_path = path + module['path']
            get_sub_module(module['branch'], module['tag'], module_path)


def get_sub_module(branch,tag,module_path):
    cmd = 'git checkout %s \n git pull \n git checkout %s' % (branch,tag)
    print 'submodule：' + cmd
    print 'module_path：' + module_path
    subprocess.call(cmd, shell=True,
                    cwd=module_path)

def build(cc):
    shell('cd %s' % src_path)
    shell('./gradlew clean')
    # shell('./gradlew cleanBuildCache')
    # if lint:
    #     shell('./gradlew lintRelease')
    #     shell('./gradlew ' + 'lint' + 'Release')

    errorcode = cc()
    if errorcode == 0:
        print 'Build Success'
    else:
        print 'Build Failed: error code is', errorcode
        shell('cd %s' % cur_path)
        exit(1)

def uploadFile(filePath, appInfo):
    upload_files = {'file': open(filePath, 'rb')}
    r = requests.post('http://app-pack.go2yd.com/uploadfile', data = appInfo, files=upload_files)
    # print(r.status_code)
    if r.status_code == 200:
        # print(r.json())
        return r.json()
    else:
        # print('request error:', r.status_code, r.text)
        return False

def post_compile_operations(cc, branch):
    git_ver = shell('git rev-parse --short HEAD')[:-1]
    project_name = "truely"
    meta_data = FileUtil.readjson(metadata_path % (src_path, cc.product))
    apk_file_name = "app-release.apk"
    if None != meta_data:
        apk_file_name = meta_data["elements"][0]["outputFile"]
        version_name = meta_data["elements"][0]["versionName"]
    src = apk_path % (src_path, cc.product, apk_file_name)
    type = "online"
    if cc.product  == "Debug":
        type = 'alpha'
    appInfo = {
        'appid': 'localside',
        'platform': 'android',
        'version': version_name,
        'display_name': '啫喱',
        'bundleID': 'com.yidian.local',
        'type': type,
        'subType': 'release',
        'icon': ''
    }
    result = uploadFile(src,appInfo)
    print ("result:%s" % result)
    if result['code'] == 0:
        print ('apk_download_url:%s' % result['data'])
    else:
        print ('upload apk fail')

    # 保存mapping到服务器
    global target_dir
    time = timestamp
    target_dir = web_target_dir_unsigned % (project_name,cc.product,
                                            version_name, "_%s_%s"%(git_ver,time))
    global location_dir
    location_dir = web_location_dir_unsigned % (project_name,cc.product,
                                                version_name, "_%s_%s"%(git_ver,time))
    terminal = web_terminal
    shell("ssh %s 'mkdir -p %s'" % (terminal, target_dir))
    #copy mapping
    src_mapping = mapping_src % src_path
    res_mapping = shell('scp %s %s:%s' % (src_mapping, terminal, target_dir), False) == 0
    if res_mapping:
        print 'mapping_download_url:%s/mapping.txt' % location_dir
    print 'Upload to server succeed!'


def create_local_properties():
    flutter_sdk ="flutter.sdk=/Users/daqianduan/Downloads/flutter2.2.3"
    # ndk_sdk ="flutter.sdk=/Users/daqianduan/Documents/flutter_sdk"
    FileUtil.mkfile(src_path+"/local.properties",flutter_sdk)

def post_lint_files(f, target_dir):
    terminal = Data.web_terminal
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):
            index = tmp_path.find('/build/reports/lint-results-release.html')
            pos = -4

            if index == -1:
                index = tmp_path.find('/build/reports/lint/lint-result.html')
                pos = -5

            if index != -1:
                lint_dest = '%s/lint/%s_lint-results.html'
                final_r_dest = lint_dest % (
                    target_dir, tmp_path.split('/')[pos])

                # print 'lint文件:', tmp_path
                print 'lint_dest:', final_r_dest
                r_res = shell('scp %s %s:%s' % (tmp_path, terminal, final_r_dest), False) == 0

                # print '上传lint文件结果:', r_res
        else:
            # print('文件夹：%s'%tmp_path)
            post_lint_files(tmp_path, target_dir)


def write_id_and_url(url):
    print 'url=' + url
    path = archive_patch_log % archive_path
    if os.getenv('BUILD_ID') != None:
        FileUtil.write_content(path, 'BUILD_ID:' + os.getenv('BUILD_ID'))
        FileUtil.write_content(path, 'package_url:' + url)
    else:
        print
        "没有对应的buidid号。所以就不需要url 了啊,自行处理二维码信息"


if __name__ == '__main__':
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    FileUtil.mkdirs(archive_path)
    cc = config()
    checkout(flutter_src_path,cc.flutterbranch,cc.gitflutter,True)
    checkout(src_path,cc.androidbranch,cc.gitandroid,False)
    build(cc)
    post_compile_operations(cc, cc.androidbranch)
    # print "***************start check plugin*******"
    # Pluginbuild.check_plugin_verison(Util.get_code_appid(cc.flavor))
