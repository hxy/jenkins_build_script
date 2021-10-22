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
from Util import Properties
import Pluginbuild
from Data import YIDIAN, UNSIGNED, SERVER_A1, SERVER_A3, SERVER_PRE
# from Data import archive_path_dst as apk_dst
# from Data import archive_path_unsigned_dst as unsigned_apk_dst
# from Data import archive_path_unsigned_src as unsigned_apk_src
# from Data import archive_patch_log

from Data import cur_path, src_path, archive_path, short_flavor, short_buildtype, \
    module_gradle_path, proj_gradle_path, gradle_properties_path, application_gradle_path, \
    library_gradle_path, mapping_dst, mapping_src, apk_path, metadata_path, web_root_dir
from Util import shell


def config():
    branch, flavor, buildtype, patch, sign, baseApkDir, lint, gitSource, product, tag = Util.arrangeArguments(
        sys.argv)
    return branch, baseApkDir, lint, tag, Command.CompileCommand(flavor, buildtype, patch, sign,
                                                            gitSource, product)


def checkout(branch,tag, cc):
    print('---Current directory----')
    print(shell('pwd'))

    print('Start syncing git repository...')
    needClone = True
    if os.path.isdir(src_path):
        print('Folder %s exits. Check whether it is a git repository' % src_path)
        # Check if this is a valid git repository
        # shell('cd %s' % src_path)
        # if os.path.isdir(src_path + '/.git') and shell('git reset --hard', output=False) == 0:
        #     print('It is a valid git respository. Update it')
        #     shell('git clean -d -x -f')
        #     shell('git checkout %s' % branch)
        #     shell('git pull')
        #     shell("cd ..")
        #     needClone = True
        # else:
        print('Not a valid git repository. Delete folder ' + src_path)
        # shell("cd ..")
        FileUtil.delete(src_path)

    if needClone:
        # https://git.yidian-inc.com:8021/android/ydnews.git 原地址 这个地址一直拉不下代码，测试建议换成 https://umeng-dev@git.yidian-inc.com:8021/android/ydnews.git就可以拉下代码，原因不明
        if tag == "None":
            shell(
                'git clone ' + cc.gitsource + ' ' + src_path + ' --recursive')
            shell('cd %s' % src_path)
            shell('git checkout %s' % branch)
        else:
            shell(
                'git clone -b ' + tag +' ' + cc.gitsource + ' ' + src_path + ' --recursive')
            shell('cd %s' % src_path)
        shell('cd ..')

    shell('cd %s' % src_path)
    shell('chmod 777 gradlew')

    # 增加下面两行命令是发现checkout下来的项目中， protco、www 子项目没有代码，所以重新获取子项目代码
    shell('git submodule update --init --recursive ')
    shell('git submodule update --recursive')
    shell('git submodule update --recursive ')
    sub_modules_checkout(src_path)

    # copy properties and keystore NOT FOR OPPO
    if cc.sign == UNSIGNED:
        print("unsigned")
        # FileUtil.delete('%s/signing.properties' % src_path)
        FileUtil.delete('%s/cutt.android.keystore' % src_path)
        # shell(
        #     "perl -p -i -e '{s/signingConfig signingConfigs\.debug//g}' " + application_gradle_path)
        # shell(
        #     "perl -p -i -e '{s/signingConfig signingConfigs\.release//g}' " + application_gradle_path)
    else:
        # FileUtil.copy('../signing.properties', '%s/signing.properties' % src_path)
        FileUtil.copy('../cutt.android.keystore',
                      '%s/cutt.android.keystore' % src_path)


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

def pre_compile_settings(cc, baseApkDir):
    # 如果是打补丁包，创建 bugly_config.properties 文件，保存配置项中的基准包目录，格式为 BASE_APK_DIR=''
    if cc.patch:
        FileUtil.delete('%s/bugly_config.properties' % src_path)
        fo = open('%s/bugly_config.properties' % src_path, 'wb')
        fo.write('BASE_APK_DIR=%s' % baseApkDir)
        fo.close
    # disable jumboMode
    shell('perl -p -i -e "{s/jumboMode = true/jumboMode = false/g}" ' + library_gradle_path)
    shell('perl -p -i -e "{s/jumboMode = true/jumboMode = false/g}" ' + application_gradle_path)
    if cc.buildtype == SERVER_A3:
        print('Going to build a3 test release version')
        shell(
            "perl -p -i -e '{s/signingConfigs\.debug/signingConfigs\.release/g}' " + application_gradle_path)  # 这句代码只是为了以防万一
        shell("perl -p -i -e '{s/\.debug//g}' " + application_gradle_path)  # 这句代码只是为了以防万一
        shell(
            "perl -p -i -e '{s/minifyEnabled false/minifyEnabled true/g}' " + application_gradle_path)  # 这句代码只是为了以防万一
        shell(
            "perl -p -i -e '{s/shrinkResources false/shrinkResources true/g}' " + application_gradle_path)  # 这句代码只是为了以防万一
        shell("perl -p -i -e '{s/a1.go2yd.com/a3.go2yd.com/g}' " + module_gradle_path)  # 这句有用~~~

    if cc.buildtype == SERVER_PRE:
        print('Going to build pre a1 release version')
        shell(
            "perl -p -i -e '{s/signingConfigs\.debug/signingConfigs\.release/g}' " + application_gradle_path)  # 这句代码只是为了以防万一
        shell("perl -p -i -e '{s/\.debug//g}' " + application_gradle_path)  # 这句代码只是为了以防万一
        shell(
            "perl -p -i -e '{s/minifyEnabled false/minifyEnabled true/g}' " + application_gradle_path)  # 这句代码只是为了以防万一
        shell(
            "perl -p -i -e '{s/shrinkResources false/shrinkResources true/g}' " + application_gradle_path)  # 这句代码只是为了以防万一
        shell("perl -p -i -e '{s/a1.go2yd.com/pre.go2yd.com/g}' " + module_gradle_path)  # 这句有用~~~

    # tingyun sdk
    print('------ open tingyun compile options ------')
    if cc.flavor == YIDIAN:
        shell(
            "perl -p -i -e '{s/\/\/apply plugin: \"newlens\"/apply plugin: \"newlens\"/g}' " + module_gradle_path)
        shell("perl -p -i -e '{s/\/\/tycompile/compile/g}' " + module_gradle_path)
        shell(
            "perl -p -i -e '{s/\/\/classpath \"com.networkbench/classpath \"com.networkbench/g}' " + proj_gradle_path)
        # delete the faked lib
        FileUtil.delete('%s/yidian/libs/main/tingyunsdk.jar' % src_path)
        # shell('rm %s/yidian/libs/main/tingyunsdk.jar' % src_path)
    # elif cc.flavor == PRELOAD:
    #     print("Enable network warning dialog")
    #     shell('perl -p -i -e "{s/SHOW_NETWORK_CONNECTION_WARNING = false/SHOW_NETWORK_CONNECTION_WARNING = true/g}" %s/yidian/src/zixun/java/com/yidian/news/HipuConstants.java' % src_path)
    #     properties = Util.readProperties(gradle_properties_path)
    #     minVersion = properties['VERSION_PATCH']
    #     newMiniVersion = int(minVersion) + 1
    #     print("Update apk miniVersion: oldVersion=" + minVersion + ", newVersion=" + str(newMiniVersion))
    #     cmd = "perl -p -i -e '{s/VERSION_PATCH=([0-9]?)/VERSION_PATCH=%s/}' %s" % (newMiniVersion, gradle_properties_path)
    #     shell(cmd)
    # copy files
    for dest in Data.property_paths:
        FileUtil.copy('local.properties', dest)


def build(cc, lint):
    shell('./gradlew clean')
    # shell('./gradlew cleanBuildCache')

    if lint:
        shell('./gradlew lintRelease')
        shell('./gradlew ' + 'lint' + 'Release')

    errorcode = cc();
    if errorcode == 0:
        print 'Build Success'
    else:
        print 'Build Failed: error code is', errorcode
        shell('cd %s' % cur_path)
        exit(1)


def post_compile_operations(cc, branch, lint):
    # 去除结尾的换行
    # git_ver = shell('git rev-parse --short HEAD')[:-1]
    # git_num = shell('git rev-list HEAD --count')[:-1]

    # terminal = Data.web_terminal

    # filelist = os.listdir(Data.src_floder)
    # filelist.sort()
    # print
    # 'post_compile_operations : src_floder len=', len(filelist)
    #
    # if len(filelist) != 0:
    #     apkfoldername = filelist[-1]
    #     print
    #     'post_compile_operations : apkfoldername is', apkfoldername

    # print
    # 'post_compile_operations : signed is', cc.sign
    # print
    # 'post_compile_operations : patch is', cc.patch
    # 去除结尾的换行
    git_ver = shell('git rev-parse --short HEAD')[:-1]
    git_num = shell('git rev-list HEAD --count')[:-1]
    project_name = cc.gitsource[cc.gitsource.rfind('/'):cc.gitsource.rfind('.')]

    FileUtil.mkdirs(archive_path)
    # shell('mkdir -p %s' % archive_path)
    products = []
    if cc.product == '':
        products = ['Dev', 'Beta', 'Prod']
    else:
        products = [cc.product]
    for product in products:
        # # 获取版本号
        # version = Util.cat_version(cc.flavor)
        # print 'Version:', version
        meta_data = FileUtil.readjson(metadata_path % (src_path, "/"+product))
        apk_file_name = "app-release.apk"
        version_name = ''
        if None != meta_data:
            apk_file_name = meta_data["elements"][0]["outputFile"]
            version_name = meta_data["elements"][0]["versionName"]

        # 存档
        tmp_version = '%s_%s_%s' % (version_name, git_num, git_ver)

        src = apk_path % (src_path, "/"+product, apk_file_name)

        # 保存到服务器
        target_dir = Data.web_target_dir_unsigned % (project_name,
                                                     tmp_version, short_buildtype.get(cc.buildtype))
        location_dir = Data.web_location_dir_unsigned % (project_name,
                                                         tmp_version, short_buildtype.get(cc.buildtype))
        terminal = Data.web_terminal

        # FileUtil.mkdirs(target_dir)
        shell("ssh %s 'mkdir -p %s'" % (terminal, target_dir))

        # 因为永远打Release包，所以src最后一个参数为release，而非 cc.buildtype.lower()
        # res = FileUtil.copy(src % (src_path,lower_flavor,'release'), dst % (target_dir,cc.flavor,short_buildtype.get(cc.buildtype),formalVersion))
        final_src = src
        res = shell('scp %s %s:%s' % (final_src, terminal, target_dir), False) == 0
        print 'apk_download_url:%s/%s' % (location_dir, apk_file_name)

        if cc.sign != UNSIGNED:
            if product == "Prod":
                src_mapping = mapping_src % (src_path, product)
                res_mapping = shell('scp %s %s:%s' % (src_mapping, terminal, target_dir), False) == 0
                if res_mapping:
                    print 'mapping_download_url:%s/mapping.txt' % location_dir

        if res:
            server = 'a3'
            if cc.buildtype == SERVER_A1:
                server = 'a1'
            print 'Location --- ', location_dir
            url = location_dir + '/' + FileUtil.getfilename(target_dir)
            # write_id_and_url(url)
            item = location_dir + ",Version:" + version_name + ",Server:" + server + ",Flavor:" + cc.flavor + ",Branch:" + branch + ",Patch:" + str(
                cc.patch)
            shell(
                'ssh %s "cd %s ; python %s %s"' % (
                    terminal, Data.web_record_pythonpath, Data.web_record_pythonfile, item))
            print 'Upload to server succeed!'
        else:
            raise ValueError("Upload to server Failed!")




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
    FileUtil.mkdirs(archive_path)
    branch, baseApkDir, lint, tag, cc = config()
    checkout(branch, tag, cc)
    # pre_compile_settings(cc, baseApkDir)
    build(cc, lint)
    post_compile_operations(cc, branch, lint)
    # print "***************start check plugin*******"
    # Pluginbuild.check_plugin_verison(Util.get_code_appid(cc.flavor))
