# -*- coding: utf-8 -*-
from Data import YIDIAN, ZIXUN, OPPO, DK, GLORY, FOXCONN, SERVER_A1, SERVER_A3, SIGNED, UNSIGNED
from Util import command as cmdLog
from Util import shell
import sys
import Util
from Data import SERVER_A1, SERVER_A3, SERVER_PRE, SIGNED, UNSIGNED


class CompileCommand(object):
    __slots__ = ('__flavor', '__buildtype', '__patch', '__sign', '_gitsource','_product')

    def __init__(self, flavor, buildtype, patch, sign, gitsource, product):
        self.flavor = flavor
        self.buildtype = buildtype
        self.patch = patch
        self.sign = sign
        self.gitsource = gitsource
        self.product = product

    def __str__(self):
        prefix = ''
        if self.__patch:
            prefix = 'buildTinkerPatch'
        else:
            prefix = 'assemble'

        command_flavor = self.__flavor

        return prefix +self.product+ 'Release'  # 永远打Release包

    __repr__ = __str__

    @cmdLog
    def __call__(self):
        print "_call_"
        return shell('./gradlew --no-build-cache ' + self.__str__(), False)
        # return shell('./gradlew --debug --stacktrace --no-build-cache ' + self.__str__(), False)

    @property
    def flavor(self):
        return self.__flavor

    @flavor.setter
    def flavor(self, flavor):
        self.__flavor = flavor

    @property
    def buildtype(self):
        return self.__buildtype

    @buildtype.setter
    def buildtype(self, buildtype):
        if buildtype == SERVER_A3 or buildtype == SERVER_A1 or buildtype == SERVER_PRE:
            self.__buildtype = buildtype
            print
            'ComileCommand buildtype  %s' % buildtype
        else:
            raise ValueError('wrong BuildType parameter!')

    @property
    def patch(self):
        return self.__patch

    @patch.setter
    def patch(self, patch):
        if isinstance(patch, bool):
            self.__patch = patch
            print
            'ComileCommand patch  %s' % patch
        else:
            raise ValueError('wrong patch parameter!')

    @property
    def sign(self):
        return self.__sign

    @sign.setter
    def sign(self, sign):
        if sign == SIGNED or sign == UNSIGNED:
            self.__sign = sign
        else:
            raise ValueError('wrong sign type!')

    @property
    def gitsource(self):
        return self._gitsource

    @gitsource.setter
    def gitsource(self, gitsource):
        self._gitsource = gitsource

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, product):
        self._product = product


# test
if __name__ == '__main__':
    c = CompileCommand('Yidian', 'Debug', True, 'signed', "/test.git")
    print
    c
    print
    "start c()"
    c()
