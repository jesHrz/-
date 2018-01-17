# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

#   按照要求筛选所得到的信息
def search_classes(searcher, search_kch='', search_jsh='', search_xq='', search_jc='', search_kkxsh='', search_dd=''):
    # 提交表单的地址和header
    search_url = "http://bkjwxk.sdu.edu.cn/b/xk/xs/kcsearch"

    # 存放用于返回的筛选后的结果
    search_result = []
    current_page = 1
    while True:
        #   表单内容
        search_form = {
            'type': 'kc',
            'currentPage': current_page,
            'kch': '',
            'jsh': '',
            'skxq': search_xq,
            'skjc': search_jc,
            'kkxsh': ''
        }
        #   提交post表单获取json信息
        json = searcher.emit(search_url, "post", search_form)

        #   从返回的json信息中筛选要显示的课程信息以及总页数
        total_page = json['object']['totalPages']
        classes = json['object']['resultList']
        for clas in classes:
            if (search_dd in clas['SJDD'] if clas['SJDD'] is not None else True) and \
                    (search_jsh in clas['JSM'] if clas['JSM'] is not None else True) and \
                    ((search_kch in clas['KCM'] if clas['KCM'] is not None else True) or (search_kch in clas['KCLBMC'] if clas['KCLBMC'] is not None else True)) and \
                    (search_kkxsh in clas['KKXSH'] if clas['KKXSH'] is not None else True):
                search_result.append(clas)

        current_page += 1

        if current_page > total_page:
            break

    return search_result


def check_classes(seacher):
    response = seacher.emit("http://bkjwxk.sdu.edu.cn/f/xk/xs/yxkc", "get")
    soup = BeautifulSoup(response, "lxml")

    tag = ["KCH", "KCM", "KXH", "SJDD", "JSM", "SX"]
    res = []
    for each in soup.find_all('tr'):
        st = BeautifulSoup(str(each), "lxml")
        i = 0
        content = []
        for t in st.find_all('td'):
            i += 1
            if i == 1 or i == 5 or i > 8:
                continue
            else:
                if t.string is None:
                    content.append('')
                else:
                    content.append(t.string)

        if len(content) > 0:
            dict = {
                tag[0]: content[0],
                tag[1]: content[1],
                tag[2]: content[2],
                tag[3]: content[3],
                tag[4]: content[4],
                tag[5]: content[5]
            }
            res.append(dict)

    return res