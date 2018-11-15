import urllib.request
import urllib.parse
import chardet
import re
import os
import threading


class Spider:
    def __init__(self, url):
        self.head = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            # 'Host': 'httpbin.org'
        }
        self.html = ''
        self.url = url
        self.getHTML(self.url)
        self.getIMG()

    def getHTML(self, url):
        url1 = "http://127.0.0.1:880/post"
        url2 = "http://httpbin.org/get"
        url3 = "https://duckduckgo.com/"

        dict = {"q": "peng"}
        data = bytes(urllib.parse.urlencode(dict), encoding="utf8")
        isproxy = 0
        if isproxy:
            print("使用代理")
            proxy_handler = urllib.request.ProxyHandler({
                "http": "127.0.0.1:12333",
                # "http": "61.128.208.94:3128",
                # "http": "119.3.20.128:80",
                # "http": "117.191.11.108:80",
                # "https": "119.3.20.128:80",
                "https": "127.0.0.1:12333",
            })
        else:
            print("不使用代理")
            proxy_handler = urllib.request.ProxyHandler()
        opener = urllib.request.build_opener(proxy_handler)
        # opener.add_handler(head)

        url = url + "?" + urllib.parse.urlencode(dict)
        print(url)
        request = urllib.request.Request(url)
        # 添加头部
        opener.addheaders = [a for a in self.head.items()]
        print("访问网页")
        response = opener.open(request)
        print("访问成功")
        html = response.read()
        charset = chardet.detect(html)  # 获取网页编码
        self.html = html.decode(charset["encoding"])
        # print(html)
        return html

    def saveIMG(self, download, save):
        # 直接用urlretrieve 405错误,所以直接写文件
        if os.path.exists(save):
            return
        with open(save, 'wb') as f:
            # 如果存在文件,就不下载
            # 包装头部,否则无法访问
            request = urllib.request.Request(download, headers=self.head)
            a = (urllib.request.urlopen(request)).read()
            f.write(a)

    def getIMG(self):
        """
        https://blog.csdn.net/cquptcmj/article/details/53526137
        https://www.cnblogs.com/zhouxuchen/p/4341034.html
        """
        regular = '''<img src="[\w/]*.\w+" data-src="([/\w]*.\w+)"'''
        root = "https://wallhalla.com"
        imgs = re.findall(regular, self.html)
        savepath = "imgs/"
        try:
            os.listdir(savepath)
        except FileNotFoundError as e:
            os.mkdir(savepath)
        print(imgs)
        for i in imgs:
            download = root + i
            save = savepath + '' + i.split('/')[-1]
            print(download, "->", save)
            # 使用线程,快
            threading.Thread(target=self.saveIMG,
                             args=(download, save)).start()


url = "https://wallhalla.com/search?q=misaki&color=ffffff&image=&purity=safe&luminosity=0_100&reso=&reso_atleast=0&ratio=&order=relevance"
Spider(url)
