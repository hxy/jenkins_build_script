import os
import shutil
import json

def copy(src, dest):
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)

    if not os.path.exists(src):
        print src, 'not exist!!'
        return False

    if os.path.isfile(src):
        dest_dir = os.path.dirname(dest)
        if not os.path.exists(dest_dir):
            if not mkdirs(dest_dir):
                return False

        shutil.copy(src, dest)
        print 'copy file!!'
        return os.path.isfile(dest)
    else:
        if os.path.exists(dest):
            print '%s already exists!' % dest
            return False

        shutil.copytree(src, dest, True, None)
        return os.path.isdir(dest)


def mkdirs(dest):
    dest = os.path.abspath(dest)
    try:
        if not os.path.exists(dest):
            os.makedirs(dest)
    except OSError as e:
        print 'create folder %s failed!' % dest
    finally:
        return os.path.isdir(dest)


def delete(src):
    src = os.path.abspath(src)
    if not os.path.exists(src):
        print 'delete %s not exist' % src
        return False

    if os.path.isfile(src):
        os.remove(src)
    else:
        shutil.rmtree(src)
        print 'delete %s success' % src

    return not os.path.exists(src)


def readcontent(src):
    src = os.path.abspath(src)
    if not os.path.isfile(src):
        return []

    file_obj = open(src, "r")
    lines = []
    try:
        lines = file_obj.readlines()
    finally:
        file_obj.close()
        return lines

def readjson(src):
    src = os.path.abspath(src)
    if not os.path.isfile(src):
        return
    file_json =  open(src, "r")
    return json.load(file_json)


def copyfolder(src, dest):
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)

    if os.path.exists(dest):
        print dest, 'exist just delete'
        shutil.rmtree(dest)

    print 'copyfolder start...'
    shutil.copytree(src, dest)
    print 'copyfolder end...'

def write_content(filename,content):
    with open(filename, 'a') as apksrc:
        apksrc.write(content + "\n")




def getfilename(file_path):
    filepath,fullflname = os.path.split(file_path)
    return fullflname

if __name__ == '__main__':
    pass
