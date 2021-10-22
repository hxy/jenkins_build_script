# -*- coding: utf-8 -*-
from Data import YIDIAN, ZIXUN, OPPO, DK, GLORY, FOXCONN, SERVER_A1, SERVER_A3, SIGNED, UNSIGNED
from Util import command as cmdLog
from Util import shell
import sys
import Util
from Data import SERVER_A1, SERVER_A3, SERVER_PRE, SIGNED, UNSIGNED


class CompileCommand(object):
    __slots__ = ('_flavor', '_gitandroid', '_androidbranch', '_gitflutter', '_flutterbranch','_product')

    def __init__(self, flavor, gitandroid, androidbranch, gitflutter, flutterbranch, product):
        self.flavor = flavor
        self.gitandroid = gitandroid
        self.androidbranch = androidbranch
        self.gitflutter = gitflutter
        self.flutterbranch = flutterbranch
        self.product = product

    def __str__(self):
        prefix = ''
        # if self._patch:
        #     prefix = 'buildTinkerPatch'
        # else:
        prefix = 'assemble'

        return prefix +self.product

    __repr__ = __str__

    @cmdLog
    def __call__(self):
        print "__call__"
        return shell('./gradlew --no-build-cache ' + self.__str__(), False)
        # return shell('./gradlew --debug --stacktrace --no-build-cache ' + self._str_(), False)

    @property
    def flavor(self):
        return self._flavor

    @flavor.setter
    def flavor(self, flavor):
        self._flavor = flavor

    @property
    def gitandroid(self):
        return self._gitandroid

    @gitandroid.setter
    def gitandroid(self, gitandroid):
        self._gitandroid = gitandroid

    @property
    def androidbranch(self):
        return self._androidbranch

    @androidbranch.setter
    def androidbranch(self, androidbranch):
        self._androidbranch = androidbranch

    @property
    def gitflutter(self):
        return self._gitflutter

    @gitflutter.setter
    def gitflutter(self, gitflutter):
        self._gitflutter = gitflutter

    @property
    def flutterbranch(self):
        return self._flutterbranch

    @flutterbranch.setter
    def flutterbranch(self, flutterbranch):
        self._flutterbranch = flutterbranch

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, product):
        self._product = product


# test
# if _name_ == '_main_':
#     c = CompileCommand('Yidian', 'Debug', True, 'signed', "/test.git")
#     print
#     c
#     print
#     "start c()"
#     c()
