import json
import os
import time
from django.shortcuts import render
import pymysql
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse
import random
import hashlib
import requests


# Create your views here.

def index(request):
    return render(request, 'index.html')


def wordlist(request):
    # 导入Word类
    global word
    from english.models import Word
    # 实例化一个word对象
    # Words = Word.objects.all()
    Words = Word.objects.order_by('word')
    # 将数据按照规定每页显示 20 条, 进行分割
    paginator = Paginator(Words, 20)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            words = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            words = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            words = paginator.page(paginator.num_pages)
    # 建立空字典存储wordlist
    # dict_word = {'wordlist': words}
    # 向bookList.html页面传入数据dict_book
    return render(request, 'wordList.html', {'words': words})


def wordsearch(request):
    return render(request, 'wordSearch.html')


def word_search(request):
    from english.models import Word
    if request.method == 'GET':
        search_word = request.GET.get('word_name', '')
        word_list_search = Word.objects.filter(word__icontains=search_word)
        print(word_list_search)
        if word_list_search.count() == 0:
            return render(request, 'wordNotsearch.html')
        dict_word = {'word_list_search': word_list_search}
        return render(request, 'wordSearch.html', dict_word)


# 短文搜索
def parasearch(request):
    return render(request, 'paraSearch.html')


def para_search(request):
    from english.models import Sentence
    # return render(request, 'paraNotsearch.html')
    if request.method == 'GET':
        search_para = request.GET.get('para_name', '')
        para_list_search = Sentence.objects.filter(sentence__icontains=search_para)
        if para_list_search.count() == 0:
            return render(request, 'paraNotsearch.html')
        dict_para = {'para_list_search': para_list_search}
        #dict_para = {'para_list_search': '123'}

        return render(request, 'paraSearch.html', dict_para)


def paratranslate(request):
    return render(request, 'paragraphs.html')


def para_translate(request):
    if request.method == 'GET':
        q = str(request.GET.get('para_translate_info', ''))
        pd = str(request.GET.get('select_tran', ''))
        if pd == "en_zh":
            fromm = "en"
            too = "zh"
        else:
            fromm = "zh"
            too = "en"
        appid = "20210602000850930"
        salt = str(random.randint(0, 100000000))
        key = "n38aAVszmMRNNBN2kl0y"
        strr = appid + q + salt + key
        # print(str)
        hash_md5 = hashlib.md5(strr.encode(encoding='UTF-8'))
        retstr = hash_md5.hexdigest()
        # print(retstr)
        poststr = "https://fanyi-api.baidu.com/api/trans/vip/translate?q=" + q + "&from=" + fromm + \
                  "&to=" + too + "&appid=" + appid + "&salt=" + salt + "&sign=" + retstr
        r = requests.get(poststr)
        result = r.json()['trans_result'][0]['dst']
        # print(result)
        return render(request, 'paragraphs.html', {"result": result})


def wordinfo(request, id):
    # 导入
    from english.models import Word
    # 实例化一个对象，使用id查询该数据
    word = Word.objects.get(word_id=id)

    # 建立空字典存储wordlist
    dict_word = {'word': word.word, 'word_id': word.word_id, 'word_levels': word.levels}
    # 存储单词名称

    # 从数据库获取数据
    db = pymysql.connect(host="localhost", user="root", password="Qq114514", database="en")

    # SQL 查询单词词性以及翻译
    cursor1 = db.cursor()

    sql1 = "SELECT DISTINCT property,translation \
        FROM word natural join translate natural join translation \
        where word_id='%s';" % id

    try:
        # 执行SQL语句
        cursor1.execute(sql1)
        # 获取所有记录列表
        results_Translation = cursor1.fetchall()
        for row in results_Translation:
            # print(type(row))
            property = row[0]
            translation = row[1]
            # 打印结果
            print("property=%s,translation=%s" % \
                  (property, translation))

    except:
        print("Error: unable to fetch data")

    dict_word['word_tran'] = results_Translation

    # SQL 查询单词词性以及翻译
    cursor2 = db.cursor()

    sql2 = "SELECT DISTINCT sentence,translation \
            from sentence natural join instance natural join word \
            where word_id='%s';" % (id)

    try:
        # 执行SQL语句
        cursor2.execute(sql2)
        # 获取所有记录列表
        results_Sentence = cursor2.fetchall()
        for row in results_Sentence:
            # print(type(row))
            sentence = row[0]
            translation = row[1]
            # 打印结果
            print("sentence=%s,translation=%s" % \
                  (sentence, translation))

    except:
        print("Error: unable to fetch data")

    dict_word['word_sent'] = results_Sentence

    return render(request, 'wordInfo.html', dict_word)


def parainfo(request, para):
    # 导入
    from english.models import Sentence

    # 建立空字典存储wordlist
    # dict_para = {'para': sentence.sentence, 'word_id': word.word_id, 'word_levels': word.levels}
    # 存储单词名称

    # 从数据库获取数据
    db = pymysql.connect(host="localhost", user="root", password="Qq114514", database="en")

    cursor1 = db.cursor()

    sql1 = "SELECT translation from sentence where sentence=para;"

    try:
        # 执行SQL语句
        cursor1.execute(sql1)
        # 获取所有记录列表
        results_Translation = cursor1.fetchall()
        for row in results_Translation:
            # print(type(row))
            translation = row[0]
            # 打印结果
            print("translation=%s" % \
                  (translation))

    except:
        print("Error: unable to fetch data")

    return render(request, 'paraSearch.html', translation)


def wordtest(request):
    return render(request, 'wordTest.html')


def word_test_getinfo(request):
    dict_word_ret = {}

    if request.method == 'POST':

        level = str(request.GET.get('level_choose', ''))

        print(level)

        # 从数据库获取数据
        db = pymysql.connect(host="localhost", user="root", password="Qq114514", database="en")

        # SQL 查询单词,词性以及翻译
        cursor1 = db.cursor()

        sql1 = "SELECT word,property,translation FROM word " \
               "natural join translate natural join translation " \
               "WHERE levels='%s' ORDER BY RAND() LIMIT 10;" % level

        try:
            # 执行SQL语句
            cursor1.execute(sql1)
            # 获取所有记录列表
            results_Translation = cursor1.fetchall()
            for row in results_Translation:
                # print(type(row))
                word = row[0]
                property = row[1]
                translation = row[2]
                # 打印结果
                print("word=%s,property=%s,translation=%s" % \
                      (word, property, translation))
        except:
            print("Error: unable to fetch data")

        dict_word_ret['words'] = results_Translation

        return HttpResponse(json.dumps(dict_word_ret, ensure_ascii=False), content_type="application/json")


def mysqldumpbackup(request):
    dbHost = "localhost"
    dbUser = "root"
    dbPasswd = "Qq114514"
    dbName = "en"
    backupDir = ".\\files\\"
    dbCharset = 'utf8'
    dumppath = "D:\\MySQL\\bin\\mysqldump.exe"  # mysqldump的路径
    os.system(dumppath + " -h%s -u%s -p%s %s --default_character-set=%s > %s/%s.sql" % (
        dbHost, dbUser, dbPasswd, dbName, dbCharset, backupDir, 'backup'))
    return HttpResponse("备份完成")

def mysqlrecovery(request):
    dbHost = "localhost"
    dbUser = "root"
    dbPasswd = "Qq114514"
    dbName = "rec"
    recDir = ".\\files\\"
    dbCharset = 'utf8'
    recpath = "D:\\MySQL\\bin\\mysql.exe"  # mysqldump的路径
    os.system(recpath + " -h%s -u%s -p%s %s --default_character-set=%s < %s/%s.sql" % (
        dbHost, dbUser, dbPasswd, dbName, dbCharset, recDir, 'backup'))
    return HttpResponse("恢复完成")