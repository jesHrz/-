# -*- coding: utf-8 -*-

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
            'kch': search_kch,
            'jsh': search_jsh,
            'skxq': search_xq,
            'skjc': search_jc,
            'kkxsh': search_kkxsh
        }
        #   提交post表单获取json信息
        json = searcher.post(search_url, search_form)

        #   从返回的json信息中筛选要显示的课程信息以及总页数
        total_page = json['object']['totalPages']
        classes = json['object']['resultList']

        for clas in classes:
            if search_dd in clas['SJDD']:
                search_result.append(clas)

        current_page += 1

        if current_page > total_page:
            break

    return search_result
