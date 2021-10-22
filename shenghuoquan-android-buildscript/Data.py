# -*- coding: utf-8 -*-
import sys

# 标准写法都是首字母大写，其余小写
YIDIAN_FLAVOR_MATCH = ('yd', 'YD', 'Yidian', 'YiDian', 'yidian', 'YIDIAN')
ZIXUN_FLAVOR_MATCH = ('zx', 'ZX', 'Zixun', 'ZiXun', 'zixun', 'ZIXUN')
DINGKAI_FLAVOR_MATCH = ('yddk', 'YDDK', 'dingkai', 'DingKai', 'Dingkai', 'DINGKAI')
GLORY_FLAVOR_MATCH = ('glory', 'GLORY', 'Glory')
HUAWEI_FLAVOR_MATCH = ('huawei', 'HUAWEI', 'HuaWei', 'Huawei')
OPPO_FLAVOR_MATCH = ('oppo', 'OPPO', 'Oppo')
ZIXUNHD_FLAVOR_MATCH = ('Zixun_hd', 'zixun_hd', 'ZIXUN_HD', 'zixunhd')
LOCAL_FLAVOR_MATCH = ('local', 'ydlocal', 'Ydlocal', 'YdLocal')
FOXCONN_FLAVOR_MATCH = ('foxconn', 'Foxconn', 'FoxConn', 'FOXCONN')
DEBUG_TYPE_MATCH = ('a3', 'A3', 'DEBUG', 'debug', 'd', 'deb', 'D', 'Deb', 'Debug')
RELEASE_TYPE_MATCH = ('a1', 'A1', 'Release', 'RELEASE', 'release', 'r', 'R', 'rele', 'Rele')
PRE_TYPE_MATCH = ('PRE', 'pre', 'p')
PATCH_OPTION_MATCH = ('p', 'P', 'patch', 'Patch', 'PATCH')
LINT_OPTION_MATCH = ('l', 'L', 'lint', 'Lint', 'LINT')

# 标准写法
YIDIAN = 'Yidian'
ZIXUN = 'Zixun'
DK = 'Yddk'
GLORY = 'Glory'
HUAWEI = 'HuaWei'
OPPO = 'Oppo'
ZIXUNHD = 'Zixun_hd'
FOXCONN = "foxconn"
LOCAL = 'Ydlocal'
SERVER_A1 = 'Release'
SERVER_A3 = 'Debug'
SERVER_PRE = 'Pre'
SIGNED = 'signed'
UNSIGNED = 'unsigned'

# 路径
cur_path = sys.path[0]  # 脚本目录
src_path = cur_path + '/shq_src_code'  # 代码路径
archive_path = cur_path + '/archives'  # 存档路径
# src_floder = '../archives/'  # bugly 输出目录
# archive_patch_path = src_floder + '/patch'  # 补丁存档路径

# 本地properties文件拷贝的目标位置
property_paths = (
    'yidian/local.properties', 'pulltorefreshlib/local.properties',
    'TencentWeiboSDKComponent/local.properties',
    'cropimage/simple-crop-image-lib/local.properties', 'dynamicgrid/', 'gif/')

module_gradle_path = src_path + '/app/build.gradle'
proj_gradle_path = src_path + '/build.gradle'
gradle_properties_path = src_path + '/gradle.properties'
application_gradle_path = src_path + '/config/application.gradle'
library_gradle_path = src_path + '/config/library.gradle'
# tinker_gradle_path = src_path + '/config/tinker.gradle'
# manifest_path = '%s/yidian/build/intermediates/manifests/full/%s/release/AndroidManifest.xml'
# archive_path_dst = '%s/%s_b_%s_%s.apk'
# archive_patch_log = '%s/log.txt'

# archive_path_unsigned_src = '%s/app/build/outputs/apk/yidian-%s-%s-unsigned.apk'
# archive_path_unsigned_dst = '%s/%s_%s_%s-unsigned.apk'
mapping_src = '%s/app/build/outputs/mapping/%srelease/mapping.txt'

mapping_dst = '%s/mapping.txt'
web_root_dir = '/var/wwwroot/android'  # 服务器存档路径
web_target_dir = '/var/wwwroot/android/release/%s/%s'  # 服务器存档路径
web_target_dir_unsigned = '/var/wwwroot/android/release/%s/%s%s'  # 服务器存档路径
web_record_pythonpath = '/var/wwwroot/android/release'  # 记录脚本路径
web_record_pythonfile = 'writelink.py'  # 记录脚本
web_location_dir = 'http://dailybuild.yidian-inc.com/android/release/%s/%s'
web_location_dir_unsigned = 'http://dailybuild.yidian-inc.com/android/release/%s/%s%s'
web_terminal = 'android-builder@dailybuild.yidian-inc.com'
apk_path = '%s/app/build/outputs/apk%s/release/%s'
metadata_path ='%s/app/build/outputs/apk%s/release/output-metadata.json'
# patch_path_in_server = '/var/wwwroot/android/release/%s/patch/'  # 服务器补丁文件存放地址
# bugly_apk_no_push = src_floder + '%s/%s/yidian-%s-release.apk'  # bugly 输出apk目录
# bugly_unsigned_apk_no_push = src_floder + '%s/%s/yidian-%s-release-unsigned.apk'  # bugly 输出apk目录
# bugly_mapping_file = src_floder + '%s/%s/yidian-%s-release-mapping.txt'  # bugly 输出mapping文件目录
# bugly_r_file = src_floder + '%s/%s/yidian-%s-release-R.txt'  # bugly 输出R文件目录
# bugly_patch_file = src_path + '/yidian/build/outputs/patch'  # bugly 输出补丁目录,由于文件权限问题，暂时从这一目录开始复制
# archive_patch_file = archive_patch_path + '/%s/release/patch_signed_7zip.apk'  # bugly 输出补丁文件
r_dest = '%s/%s_%s_R.txt'
# dest_floder = archive_path + '/%s%s/'
# appid_path = src_path + '/yidian/src/%s/java/com/yidian/news/HipuConstants.java'

# flavor 转换为 简称的dict
short_flavor = {YIDIAN: 'yd', ZIXUN: 'ydzx', DK: 'yddk', GLORY: 'ydglory', HUAWEI: 'ydhuawei',
                ZIXUNHD: 'ydzxhd', OPPO: 'ydoppo', LOCAL: 'ydlocal', FOXCONN: 'ydfoxconn'}
# buildtype 转换为 简称的dict
short_buildtype = {SERVER_A3: '_a3', SERVER_A1: '', SERVER_PRE: 'pre'}

if __name__ == '__main__':
    print
    application_gradle_path
    print
    library_gradle_path
