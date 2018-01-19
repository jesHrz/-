# -*- coding: utf-8 -*-


import hashlib
import http.cookiejar
import urllib.error
import urllib.parse
import urllib.request
import json

'''     用于向山东大学本科生院递交登录查询用的表单       '''


class SDULogin:
    def __init__(self, username, password):
        #   MD5加密密码
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        self.__password = md5.hexdigest()

        self.__username = urllib.parse.quote(username, 'utf-8')

        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.108 Safari/537.36 '
        }
        #   存储登录过已保存的opener 一个baseURL对应一个opener
        self.__baseURLList = []

    #   登录  成功后会在post中使用保存的opener   结果返回是否登录成功
    def login(self, url):
        result = {}
        login_form = {
            'j_username': self.__username,
            'j_password': self.__password
        }
        login_data = bytes(urllib.parse.urlencode(login_form), encoding='utf8')

        try:
            request = urllib.request.Request(url, headers=self.__headers, data=login_data)
            cookie = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
            login_respond = opener.open(request)
        except urllib.error.URLError:
            return False, result
        else:
            result = login_respond.read().decode('utf8')
            if 'success' in result:
                base_url = self.__getbaseURL(url)

                #   检查是否重复登陆    重复登陆则覆盖
                for eachURL in self.__baseURLList:
                    if base_url in eachURL.keys():
                        self.__baseURLList.remove(eachURL)
                        break

                url_list = {base_url: opener}
                self.__baseURLList.append(url_list)

                return True, result
            else:
                return False, result

    def emit(self, url, method="post", post_form=None):
        content = {}
        opener = None

        #   检查是否登陆过
        base_url = self.__getbaseURL(url)
        has_url = False
        for eachURL in self.__baseURLList:
            if base_url in eachURL.keys():
                has_url = True
                opener = eachURL[base_url]
                break

        if method == "post":
            if post_form is None:
                return
            if has_url:
                post_data = bytes(urllib.parse.urlencode(post_form), encoding='utf8')
                try:
                    request = urllib.request.Request(url, headers=self.__headers, data=post_data)
                    response = opener.open(request)
                except urllib.error.URLError:
                    pass
                else:
                    result = response.read().decode('utf-8')
                    content = json.loads(result)
        if method == "get":
            if has_url:
                try:
                    request = urllib.request.Request(url, headers=self.__headers)
                    response = opener.open(request)
                except urllib.error.URLError:
                    pass
                else:
                    result = response.read().decode('utf-8')
                    return result

        return content

    @staticmethod
    #   处理url获得baseURL以判断是否登陆过
    def __getbaseURL(url):
        index = url.find("/") + 1
        index = url.find("/", index) + 1
        index = url.find("/", index) + 1
        return url[:index]
