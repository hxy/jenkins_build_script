# -*- coding: utf-8 -*-

import Data
import time
import functools
import subprocess
import os
import re
import FileUtil


def cost(f):
    @functools.wraps(f)
    def wrapper(*args, **kw):
        t1 = time.time()
        res = f(*args, **kw)
        t2 = time.time()
        print ('call %s() cost %s second(s)' % (f.__name__, t2 - t1))
        return res

    return wrapper


def command(f):
    @functools.wraps(f)
    def wrapper(*args, **kw):
        print ('****Compile Command******')
        if len(args) > 0:
            print ('*', args[0], '*')
        print ('*************************')
        return f(*args, **kw)

    return wrapper


# 参数output 表示返回输出结果，还是返回状态码；True for output while False for status code
def shell(cmd, output=True):
    if cmd.startswith('cd '):
        path = cmd[3:]
        os.chdir(path)
        return

    if output:
        try:
            return subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            pass
    else:
        return subprocess.call(cmd, shell=True)

# 获取版本号
def cat_version(flavor):
    path = Data.manifest_path % (Data.src_path, flavor.lower())
    version_name_reg = re.compile('(?<=versionName).*')
    number_reg = re.compile('(\d+\.){3}\d+')
    lines = FileUtil.readcontent(path)
    for line in lines:
        if version_name_reg.search(line) is not None:
            remain_text = version_name_reg.search(line).group()
            return number_reg.search(remain_text).group()
    return ''
    # return shell(r'''cat %s |  perl -e 'while(<STDIN>) { if($_ =~ /android:versionName="([^"]+)"/) { print $old; last; }}' ''' % path )


def arrangeArguments(*args):
    args = args[0]
    if len(args) < 3:
        raise ValueError('lack of parameters!')
    push = ''
    flavor =''
    buildtype = ''
    patch = False
    baseApkDir = ''
    branch = args[1]
    sign = Data.SIGNED
    lint = False
    gitSource = ''
    product = ''
    tag = ''
    # 第0个参数为模块名
    for var in args[2:]:
        if var in Data.DEBUG_TYPE_MATCH:
            buildtype = Data.SERVER_A3
        elif var in Data.RELEASE_TYPE_MATCH:
            buildtype = Data.SERVER_A1
        elif var in Data.PRE_TYPE_MATCH:
            buildtype = Data.SERVER_PRE
        elif var in Data.PATCH_OPTION_MATCH:
            patch = True
            baseApkDir = args[6]
            break
        elif var in Data.LINT_OPTION_MATCH:
            lint = True
        elif var == Data.UNSIGNED:
            sign = Data.UNSIGNED
        elif var == Data.SIGNED:
            sign = Data.SIGNED
        elif var.endswith("git"):
            gitSource = var
        elif var == 'Dev':
            product = "Dev"
        elif var == 'Beta':
            product = 'Beta'
        elif var == 'Prod':
            product = 'Prod'
        elif var.startswith("B"):
            tag = var
        else:
            raise ValueError('Invalid Parameter %s!' % var)
    if buildtype != '':
        return branch, flavor, buildtype, patch, sign, baseApkDir, lint, gitSource, product, tag

# 读入Java property 文件
def readProperties(filePath):
    separator = "="
    keys = {}

    # I named your file conf and stored it 
    # in the same directory as the script

    with open(filePath) as f:

        for line in f:
            if separator in line:
                # Find the name and value by splitting the string
                name, value = line.split(separator, 1)

                # Assign key value pair to dict
                # strip() removes white space from the ends of strings
                keys[name.strip()] = value.strip()

    return keys


class Properties(object):
  def __init__(self, fileName):
    self.fileName = fileName
    self.properties = {}
  def __getDict(self,strName,dictName,value):
    if(strName.find('.')>0):
      k = strName.split('.')[0]
      dictName.setdefault(k,{})
      return self.__getDict(strName[len(k)+1:],dictName[k],value)
    else:
      dictName[strName] = value
      return
  def getProperties(self):
    try:
      pro_file = open(self.fileName, 'Ur')
      for line in pro_file.readlines():
        line = line.strip().replace('\n', '')
        if line.find("#")!=-1:
          line=line[0:line.find('#')]
        if line.find('=') > 0:
          strs = line.split('=')
          strs[1]= line[len(strs[0])+1:]
          self.__getDict(strs[0].strip(),self.properties,strs[1].strip())
    except Exception, e:
      raise e
    else:
      pro_file.close()
    return self.properties


# 测试
if __name__ == '__main__':
    l = [y * y for y in range(2, 20) if y % 2 == 0]


    @cost
    def calc(l):
        newlist = map(lambda y: y + 3, l)
        return newlist


    print (calc(l))


    @command
    def command(s):
        print (s)


    #     command('AssembleYidianDebug')
    #
    #     shell('git status')
    #     shell('cd ..')
    #     shell('cd yidian_docs/pylon')
    #     shell('ls')
    #     print shell('pwd')

    print shell('git rev-list HEAD --count')[:-1], 'test'

def get_code_appid(flavor):
    path =  Data.appid_path % (flavor.lower())
    # applicationId "com.yidian.news.huaweiplug"
    #print 'path==',path
    p = re.compile(r'.*OEM_APPID\s*=\s*"(\w+)".*')
    lines = FileUtil.readcontent(path)
    for line in lines:
        m = p.match(line)
        if m:
            #print m.group(1)
            return m.group(1)
    raise ValueError('not find appid ! cannot compare plugin code!!!')