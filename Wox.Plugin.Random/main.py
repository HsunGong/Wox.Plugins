# # -*- coding: utf-8 -*-

from wox import Wox, WoxAPI

# from web import search

keys = ['password', 'uuid-guid', 'uuid-32']

import uuid
import random

# defaults
B32_SPACE = '[^ABCDEFGHIJKLMNOPQRSTUVWXYZ234567]+'
B32_LEN = 26


class Random(Wox):
    # def __init__(self):
    #     super().__init__()

    def gen_uuid(self, name=''):
        """ uuid3:md5 uuid5:sha-1"""
        from time import gmtime, strftime
        return uuid.uuid5(namespace=uuid.NAMESPACE_DNS,
                          name=strftime("%Y-%m-%d-%H:%M:%S", gmtime()) + name).__str__()

    def gen_uuid_base(self, name='wox', length=B32_LEN, name_len=24):
        """
        youd import from https://github.com/t-mart/youd/blob/master/youd.py\n
        Generate a random base32-encoded uuid (A-Z,2-7) with an optional readable word in the beginning.\n
        If you provide a string as the first argument to this script, it will replace the first characters of this otherwise random uuid.
        Only characters of the word that are in the (A-Z, 2-7) space will be placed. Lower cased letters that are provided are
        converted to upper case.
        Why? Sometimes, you're writing tests or documentation and you need a uuid, but also want it to be readable and meaningful. What's
        going to convey more to users? RPRKIRYJSVMWSOY64XS3CIL3OO or SPECIALUUID6JIHP5RKUQBPDQI ?
        The second uuid there was created by running the script like this:
        $ youd "special uuid"
        """
        import re
        u = re.sub(B32_SPACE, '', name.upper())[:name_len]  # max name len
        import base64
        real_uuid = base64.b32encode(uuid.uuid4().bytes)[:length]
        return u + str(real_uuid[:(length - len(u))], encoding="utf-8")

    def gen_passwd(self, size=12, sign=True):
        """
        import from https://github.com/sectool/Python-Random-Password-Generator/blob/master/source/rpg.py
        """
        import string
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        if sign:
            chars += chars + string.punctuation
        chars += string.digits
        return ''.join(random.choice(chars) for x in range(0, size))

    def copy_to_clipboard(self, text):
        cmd = 'echo ' + text.strip() + '| clip'
        import os
        os.system(cmd)
        # WoxAPI.hide_app()

    @staticmethod
    def hint(input):
        import re
        res = [k for k in keys if re.search(input, k)]
        return res

    def get_detail(self, method, argv):
        if method == keys[0]:
            if len(argv) == 1:
                try:
                    ans = self.gen_passwd(size=int(argv[0]))
                except:
                    ans = 'Please Input a number after `password`'
            else:
                ans = self.gen_passwd()
        elif method == keys[1]:
            if len(argv) == 1:
                ans = self.gen_uuid(name=argv[0])
            elif len(argv) == 0:
                ans = self.gen_uuid()
            else:
                ans = 'Please Input a Special Name after `uuid`'
        else:
            if len(argv) == 1:
                ans = self.gen_uuid_base(name=argv[0])
            elif len(argv) == 0:
                ans = self.gen_uuid_base()
            else:
                ans = 'Please Input  a Special Name after `uuid`'

        results = []
        results.append({
            "Title": ans,
            "SubTitle": "Copy it",
            "JsonRPCAction": {
                "method": "copy_to_clipboard",
                "parameters": [ans],
                "dontHideAfterAction": True
            }
        })
        results.append({
            "Title": ans + ' Regen it needs change query',
            "SubTitle": "Regen it??",
            "JsonRPCAction": {
                "method": "Wox.ChangeQuery",
                "parameters": ["gen " + method, True],
                "dontHideAfterAction": True
            }
        })
        return results

    def query(self, query):
        results = []
        argv = query.strip(' ').split(' ')
        hints = Random.hint(argv[0])

        for h in hints:
            if h == argv[0]:
                return self.get_detail(h, argv[1:])

            results.append({
                "Title": h,
                "SubTitle": "Config it",
                "JsonRPCAction": {
                    # 这里除了自已定义的方法，还可以调用Wox的API。调用格式如下：Wox.xxxx方法名
                    # 方法名字可以从这里查阅https://github.com/qianlifeng/Wox/blob/master/Wox.Plugin/IPublicAPI.cs 直接同名方法即可
                    "method": "Wox.ChangeQueryText",
                    # 参数必须以数组的形式传过去
                    "parameters": ['gen ' + h, True],
                    # 是否隐藏窗口
                    "dontHideAfterAction": True
                }
            })

        return results


def test():
    print(Random().query(None, 'password'))
    # print(Random.get_detail(None, 'password', []))


if __name__ == "__main__":
    Random()
    # test()
