# -*- coding: utf-8 -*-
"""
Wox支持使用Python进行插件的开发。Wox自带了一个打包的Python及其标准库，所以使用Python 插件的用户不必自己再安装Python环境。
同时，Wox还打包了requests和beautifulsoup4两个库， 方便用户进行网络访问与解析。
ref: http://doc.getwox.com/zh/plugin/python_plugin.html
"""

import webbrowser
import os, sys

from wox import Wox, WoxAPI

import pandas as pd

NULL='None'
class timeline(object):
    @staticmethod
    def readExcel(sheet_name):
        """
        Para:
        --
        sheet_name : string
        Return:
        --
        DataFrame of 1 sheet\n
        row-name: start with 0\n
        col-name: start with 1(No head)
        """
        datas = pd.read_excel('data/index.xlsx',
                              sheet_name=sheet_name,
                              header=None)
        return datas

    def query(self, label, query):
        results = []
        if not len(query) == 0:
            # bookmark_searcher().do_search(query)
            for _, item in self.search(label, query).iterrows():
                # print(item['path'])
                results.append({
                    "Title": item['title'],
                    "SubTitle": item['time'] if item['path'] == NULL else item['path'], # Done
                    "IcoPath": "images/app.ico",
                    "JsonRPCAction": {
                        "method": "openUrl",
                        "parameters": [item['url']],
                        "dontHideAfterAction": True
                    }
                })

        if len(results) == 0:
            results.append({
                "Title": NULL,
                "SubTitle": "Query: Not Found",
            })
        return results

    def search(self, label, keys):
        """
        col-index: `type`(deleted), time, url, title, folder/path, inter(delete), chrome_path(delete)
        """
        datas = self.readExcel('Timeline')
        datas = datas.loc[datas[0] == label]
        # or datas.drop(0, axis='columns', inplace=True)
        datas = datas[[0, 1, 2, 3, 4]]  # list(range(0,5))
        datas.fillna(NULL, inplace=True)
        datas.rename(columns={
            0: 'type',
            1: 'time',
            2: 'url',
            3: 'title',
            4: 'path'
        },
                     inplace=True)
        # datas.drop(columns=['type', 'useless'], inplace=True)

        sel = ~pd.Series(index=datas.index, dtype=bool)
        for key in keys:
            sel = sel & (datas['url'].str.contains(key) |
                         datas['title'].str.contains(key))
        datas = datas.loc[sel]

        # datas.reset_index(inplace=True)

        # print(datas[0:1].values)
        return datas


class bookmark(timeline):

    def query(self, query):
        return super().query('bookmark', query)


class history(timeline):

    def query(self, query):
        return super().query('url', query)


if __name__ == "__main__":
    bookmark()
