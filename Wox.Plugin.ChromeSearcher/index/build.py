import sys, os

import subprocess as sub


class index(object):

    def query(self, query):
        """
        reindex the ....
        """
        if not os.path.exists('index'):
            raise FileNotFoundError
        if os.path.exists('data/index.xlsx'):
            os.remove('data/index.xlsx')
        return index.index()

    @staticmethod
    def index():
        # has changed dir
        p = sub.run([
            'index/hindsight.exe', '-i',
            'C:/Users/xun/AppData/Local/Google/Chrome/User Data/Default', 
            '-o', '../data/index'
        ],timeout=600,check=False)

        results=[]
        if p.returncode != 0:
            results.append({
                    "Title": 'Error',
                    "SubTitle": p.stderr
            })
        else:
            results.append({
                    "Title": 'Success'
            })
        return results