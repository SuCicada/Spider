import urllib.request
import urllib.parse
import chardet
import re
import os
import threading
import lxml.etree
import json
import sys
import threading
from queue import Queue

# https://www.jianshu.com/p/02cc7442fb99
# about Queue
# https://blog.csdn.net/sjyttkl/article/details/79887720

head = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
}
'''
我们为了获得服务器的json回复,第三行必须要,前两个没有也行
https://blog.csdn.net/heatdeath/article/details/79168614
如果 requestedWith 为 null，则为同步请求。
如果 requestedWith 为 XMLHttpRequest 则为 Ajax 请求。
'''
head_json = {
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest',
}

IMG_CONUT = 0
DOWN_COUNT = 0
myqueue = Queue()


def getHTML(url, savepage=False, accept=None):
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
    # print(url)
    request = urllib.request.Request(url)
    # 添加头部
    opener.addheaders = [a for a in head.items()]
    if accept == "json":
        opener.addheaders += [a for a in head_json.items()]
    # print(opener.addheaders)
    print("访问网页...", end="")
    response = opener.open(request)
    print("访问成功")
    html = response.read()
    charset = chardet.detect(html)  # 获取网页编码
    # print(charset)
    html = html.decode(charset["encoding"])
    if savepage:
        with open('html.html', 'wb') as f:
            f.write(html)
        print("保存网页成功")
    # print(html)
    return html

# 下载不全


def downloadURL(download, save, flag=3):
    if not flag:
        print("failed")
        return
    try:
        a, b = urllib.request.urlretrieve(download, save)
        print(IMG_CONUT, " success")
    except urllib.error.ContentTooShortError:
        download(download, save, flag - 1)


def saveIMG(root, savepath):
    global DOWN_COUNT, IMG_CONUT
    while not myqueue.empty():
        # 得到图片编号
        i = myqueue.get()
        download = root + i
        save = savepath + '' + i + ".jpeg"
        # 如果存在文件,就不下载
        IMG_CONUT += 1
        print("[%d] " % IMG_CONUT, download, "->", save, "...")
        if not os.path.exists(save):
            downloadURL(download, save)
            DOWN_COUNT += 1
        myqueue.task_done()  # 同步queue


def getIMG(search, page=3, rejson=False):
    """
    https://blog.csdn.net/cquptcmj/article/details/53526137
    https://www.cnblogs.com/zhouxuchen/p/4341034.html
    """

    # 注意要编码
    ori_url = "http://huaban.com/search/?q=%s&type=pinspage" % urllib.parse.quote(
        search)
    print("寻找图片")
    root = "http://hbimg.b0.upaiyun.com/"
    savepath = "./" + search + "/"

    try:
        os.listdir(savepath)
    except FileNotFoundError as e:
        os.mkdir(savepath)

    imgs = []
    # if os.path.exists("imgs.json") and not rejson:
    if 1 == 2:
        with open("imgs.json", "r") as f:
            # a = json.load(f)
            # print(a)
            imgs = json.load(f)["imgs"]
    else:
        for i in range(1, int(page) + 1):
            url = ori_url + "&page=%d&per_page=20" % i
            html = getHTML(url, accept="json")
            res_dict = json.loads(html)
            # 得到图片编号
            imgs += [i['file']['key'] for i in res_dict["pins"]]
        imgs = list(set(imgs))
        with open("imgs.json", "w") as f:
            json.dump({"imgs": imgs}, f)

    print(len(imgs))
    for i in imgs:
        myqueue.put(i)

    thread_num = 5
    for i in range(thread_num):
        threading.Thread(target=saveIMG, args=(root, savepath)).start()
        # saveIMG(url, root, savepath)
    myqueue.join()  # 等到队列为空，再执行别的操作

    print("共计%d张,下载%d张" % (IMG_CONUT, DOWN_COUNT))


if __name__ == "__main__":
    man = """
        -q    search the name of your picture
        -p    the number of pages that you want to search,default one page
        """
    # -re   clear the cache of search results
    man_zn = """
        -q    搜索你的图片
        -p    搜索的页数,每页20张,默认1页
        """
    # -re   是否清除缓存,重新搜索
    argv = sys.argv
    rejson = False
    search = ''
    page = 3
    for i in argv:
        if "-re" == i:
            rejson = True
        if "-p" == i:
            page = argv[argv.index(i) + 1]
        if "-q" == i:
            search = argv[argv.index(i) + 1]
    if not "-q" in argv:
        print(man)
        print(man_zn)
        quit()
    getIMG(search, rejson=rejson, page=page)
