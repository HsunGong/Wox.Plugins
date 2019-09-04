# # -*- coding: utf-8 -*-

from wox import Wox, WoxAPI

# from web import search
from searcher import bookmark, history
from index.build import index

k='b '
keys = ['bookmark', 'history', 'search', 'index']


class ChromeSearcher(Wox):
    # def __init__(self):
    #     super().__init__()

    def openUrl(self, url):
        # open the browser
        import webbrowser
        webbrowser.open(url)
        # todo:doesn't work when move this line up
        WoxAPI.change_query(url)

    @staticmethod
    def hint(input):
        import re
        res = [k for k in keys if re.search(input, k)]
        return res

    @staticmethod
    def get_detail(method, argv):
        method = eval(method)
        return method().query(argv)

    def query(self, query):
        results = []
        argv = query.strip(' ').split(' ')
        hints = ChromeSearcher.hint(argv[0])

        for h in hints:
            if h == argv[0]:
                return ChromeSearcher.get_detail(h, argv[1:])

            results.append({
                "Title": h,
                "SubTitle": "Config it",
                "JsonRPCAction": {
                    # 这里除了自已定义的方法，还可以调用Wox的API。调用格式如下：Wox.xxxx方法名
                    # 方法名字可以从这里查阅https://github.com/qianlifeng/Wox/blob/master/Wox.Plugin/IPublicAPI.cs 直接同名方法即可
                    "method": "Wox.ChangeQueryText",
                    # 参数必须以数组的形式传过去
                    "parameters": [k + h, True],
                    # 是否隐藏窗口
                    "dontHideAfterAction": True
                }
            })

        return results


def test():
    # x = ChromeSearcher()
    # print(x.hint('s'))
    s='bookmark csdn'
    # print(ChromeSearcher.query(None, s))
    ChromeSearcher.query(None, s)


if __name__ == "__main__":
    ChromeSearcher()
    # test()
