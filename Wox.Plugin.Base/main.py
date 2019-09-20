# encoding=utf-8

import re, os
from wox import Wox, WoxAPI

k = 'base '  # keyword

import psutil, platform


class naive():

    @classmethod
    def host(cls, id):
        import socket
        for proc in [socket.gethostbyname_ex, socket.gethostbyaddr]:
            try:
                s = str(proc(id))
                break
            except Exception as e:
                s = e.__str__()
                continue
        return s, "Get Hostname for IP; Get IP for Hostname"

    # import wmi
    @classmethod
    def info(cls):
        return '{} {}'.format(platform.platform(),
                              platform.machine()), 'Users ' + str(
                                  [u.name for u in psutil.users()])

    @classmethod
    def cpu(cls):
        info = '{} {}/{}'.format(platform.processor(),
                                 psutil.cpu_count(logical=False),
                                 psutil.cpu_count())
        usage = 'Usage: {}%,  Freq: {}MHz'.format(psutil.cpu_percent(),
                                    psutil.cpu_freq())  #psutil.getloadavg())
        return info, usage

    @classmethod
    def mem(cls):
        # data >> 20 # means byte -> mb; 30 -> gb
        info = psutil.virtual_memory()
        swap = psutil.swap_memory()
        s1 = 'Mem Used: {}G/{}G'.format(info.used >> 30, info.total >> 30)
        s2 = 'Swap-Mem Used: {}G/{}G'.format(swap.used >> 30, swap.total >> 30)
        return s1, s2

    @classmethod
    def disk(cls):
        info = psutil.disk_usage('/')
        s1 = 'Disk Used: {}G/{}G'.format(info.used >> 30, info.total >> 30)
        s2 = psutil.disk_partitions()
        return s1, str([s.mountpoint for s in s2])

    @classmethod
    def secs2hours(cls, secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%dh-%02dm-%02ds" % (hh, mm, ss)

    @classmethod
    def battery(cls):
        # info=psutil.sensors_temperatures['coretemp'] <- Linux
        # psutil.sensors_fans()
        info = psutil.sensors_battery()

        return 'Battery: {}%'.format(
            info.percent), 'Remain ' + ('infinite time' if info.power_plugged
                                        else cls.secs2hours(info.secsleft))

    @classmethod
    def net(cls):
        import socket
        name = platform.node()
        try:
            ip = socket.gethostbyname(name)
        except:
            ip = 'No Network'
            
        return ip, 'Hostname:{},\t{}'.format(
            name, [k for k in psutil.net_if_addrs().keys()])


class ssr(object):
    import json

    @classmethod
    def get_pac_path(cls):
        with open(os.path.join(os.path.dirname(__file__), "plugin.json"),
                  "r") as content_file:
            config = json.loads(content_file.read())
            return config["pacPath"]

    @classmethod
    def add_new_domain(cls, domain):
        if not domain:
            WoxAPI.show_msg("Warning", "You can't add empty domain")
            return

        r = re.compile(r"domains = {([\s\S]*)};")
        with open(cls().get_pac_path(), "r+") as pac:
            pactxt = pac.read()
            existing_domains = r.search(pactxt).group(1)
            domains = json.loads("{" + existing_domains + "}")
            domains[domain] = 1
            newpactxt = r.sub(
                r"domains = " + json.dumps(domains, indent=4) + ";", pactxt)
            pac.seek(0)
            pac.write(newpactxt)
            pac.truncate()
            WoxAPI.show_msg("Success", "{} is now in PAC file".format(domain))


keys = ['ssr', 'hostname-address-access', 'platform-info']


class Base(Wox):

    @staticmethod
    def hint(input, value_list=keys):
        import re
        res = [k for k in value_list if re.search(input, k)]
        return res

    @staticmethod
    def get_detail(method, argv=['']):
        results = []
        # no need to copy-clip actions
        if method == keys[0]:
            results.append({
                "Title": "add {} to Shadowsocks PAC list".format(argv[0]),
                "IcoPath": "images/ss.png",
                "JsonRPCAction": {
                    "method": "ssr",
                    "parameters": [argv[0]],
                    "dontHideAfterAction": True
                }
            })
            return results

        # copy-clip actions
        s = []
        if method in keys[1]:
            s.append(naive.host(argv[0]))
        elif method == keys[2]:
            s.append(naive.net())
            s.append(naive.cpu())
            s.append(naive.mem())
            s.append(naive.disk())
            s.append(naive.battery())
            s.append(naive.info())

        for i in range(len(s)):
            results.append({
                "Title": s[i][0],
                "Subtitle": s[i][1],
                "JsonRPCAction": {
                    "method": "copy_to_clipboard",
                    "parameters": [s[i][0]],
                    "dontHideAfterAction": True
                }
            })

        return results

    def ssr(self, argv):
        ssr.add_new_domain(argv)

    def copy_to_clipboard(self, text):
        cmd = 'echo ' + text.strip() + '| clip'
        import os
        os.system(cmd)
        # WoxAPI.hide_app()

    def query(self, query):
        results = []
        argv = query.strip(' ').split(' ')
        hints = Base.hint(argv[0])

        for h in hints:
            if h == argv[0]:
                return Base.get_detail(h, argv[1:])

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
    print(Base.query(None, 'hostname-address www.baidu.com'))


if __name__ == "__main__":
    Base()
    # test()
