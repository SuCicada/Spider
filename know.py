"""
响应状态码

200：代表成功

301：代表跳转

404：文件不存在

403：无权限访问

502：服务器错误

请求头需要注意的参数：

（1）Referrer：访问源至哪里来（一些大型网站，会通过Referrer 做防盗链策略；所有爬虫也要注意模拟）

（2）User-Agent:访问的浏览器（要加上否则会被当成爬虫程序）

（3）cookie：请求头注意携带
（1）Set-Cookie:BDSVRTM=0; path=/：可能有多个，是来告诉浏览器，把cookie保存下来

（2）Content-Location：服务端响应头中包含Location返回浏览器之后，浏览器就会重新访问另一个页面

https://blog.csdn.net/c406495762/article/details/58716886
https://www.cnblogs.com/zhaof/p/6910871.html
https://blog.csdn.net/bo_mask/article/details/76067790
"""


import urllib.request
import urllib.parse
import chardet
import re
import socks
import socket
import http.cookiejar


def fun1():
    url1 = "http://tieba.baidu.com/p/1753935195"
    url2 = "https://www.cnblogs.com/sss4/p/7809821.html"
    response = urllib.request.urlopen(url2)
    html = response.read()  # 读取页面源码
    # print(type(html))
    charset = chardet.detect(html)  # 获取网页编码
    print(charset)
    # you can use the regular, but the type of html is bytes
    # a = re.findall('''<meta charset="([\w-]*)"\/>''', html, re.MULTILINE)
    html = html.decode(charset["encoding"])  # 将网页源码进行解码,能整理格式
    # print(html)


def fun2():
    """
    https://www.cnblogs.com/zhaof/p/6910871.html
    data timeout参数使用
    """
    url = "http://httpbin.org/post"
    data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')
    print(data, type(data))
    try:
        response = urllib.request.urlopen(url, data=data, timeout=0.5)
        print(response.read().decode("utf8"))
        # 关于头部
        url = "http://httpbin.org/get"
        response = urllib.request.urlopen(url)
        print(type(response), response)
        response.getheaders()
        print(response.read().decode())

    except urllib.error.URLError as e:
        print('TIME OUT')


def fun3():
    """
    request
    """
    request = urllib.request.Request('https://python.org')
    response = urllib.request.urlopen(request)
    # print(response.read().decode('utf-8'))

    url = 'http://httpbin.org/post'
    dict = {
        'name': 'zhaofan'
    }
    data = bytes(urllib.parse.urlencode(dict), encoding='utf8')
    # 添加头部信息.方法1
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Host': 'httpbin.org'
    }
    req = urllib.request.Request(
        url=url, data=data, headers=headers, method='POST')  # must be upper
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))

    # 添加头部信息.方法2
    req = urllib.request.Request(url=url, data=data, method='POST')
    req.add_header(
        'User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))


class fun4():
    """
    代理,ProxyHandler
    https://blog.csdn.net/qq_42330464/article/details/80553718
    https://www.cnblogs.com/jackyspy/p/6027385.html
    http://www.xicidaili.com/
    """

    def __init__(self):
        self.url = "http://httpbin.org/ip"
        # self.url = "http://172.17.0.1:880/ip"
        self.fun4_1()
        print(self.response.read().decode("utf8"))

    def fun4_1(self):
        # http代理
        proxy_handler = urllib.request.ProxyHandler({
            # "http": "163.125.248.217:8118",
            "http": "127.0.0.1:12333",
            # "https": "https://127.0.0.1:1080"
        })
        opener = urllib.request.build_opener(proxy_handler)
        # 给该对象添加请求头
        # opener.addheaders = [header]
        self.response = opener.open(self.url)

    def fun4_2(self):
        # socks代理 (import socks, socket)
        socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1080)
        socket.socket = socks.socksocket
        self.response = urllib.request.urlopen(self.url)


def fun5():
    """
    cookie,HTTPCookiProcessor
    import http.cookiejar
    """
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    for item in cookie:
        print(item.name + "=" + item.value)

    # i want to save the cookie into a file
    filename = "cookie"
    # http.cookiejar.MozillaCookieJar()方式
    cookie = http.cookiejar.MozillaCookieJar(filename)
    # http.cookiejar.LWPCookieJar()方式
    # cookie = http.cookiejar.LWPCookieJar(filename)
    # Load the cookie file
    cookie.load('cookie', ignore_discard=True, ignore_expires=True)

    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open("http://www.baidu.com")
    for i in cookie:
        print(i.name, '', i.value)
    cookie.save(ignore_discard=True, ignore_expires=True)


def fun6():
    """
    error
    """
    try:
        response = urllib.request.urlopen("http://pythonsite.com/1111.html")
    except urllib.error.HTTPError as e:
        print(e.reason)
        print(e.code)
        print(e.headers)
    except error.URLError as e:
        print(e.reason)

    else:
        print("reqeust successfully")


def fun7():
    """
    URL解析
    """
    result = urllib.parse.urlparse(
        "http://www.baidu.com/index.html;user?id=5#comment")
    print(result)

    data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=123', 'commit']
    print(urllib.parse.urlunparse(data))

    params = {
        "name": "zhaofan",
        "age": 23,
    }
    base_url = "http://www.baidu.com?"
    url = base_url + urllib.parse.urlencode(params)
    print(url)


def myfun():
    data = urllib.parse.urlencode({'wd': '佐仓杏子'})
    base_url = "http://www.baidu.com"
    url = base_url + '/s?' + data
    print(url)
    response = urllib.request.urlopen(url)
    print(response.read().decode("utf-8"))


# fun4()
myfun()
