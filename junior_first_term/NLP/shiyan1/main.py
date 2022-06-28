# 这是一个示例 Python 脚本。
import json

import nltk


def delete_punctuation(source, clean_over):
    with open(source, 'r', encoding="utf-8") as f:
        f = f.read()
        index = 0
        # 删除/w标注的词
        while f.find('w', index) != -1:
            index = f.find('w')
            f = f[:index - 4] + f[index + 1:]
            #print(f)
        f = (f.replace("{", " ").replace("}", " "))
        #f = (f.replace("[", "").replace("]", ""))
        file = open(clean_over, 'w')
        file.write(f)
        file.close()
        print("删除标点完成")


def clean_letter(in_put, out_put):
    stopwords = [line.strip() for line in
                 open(r'C:\Users\yuanhuanfa\Desktop\nlp\stopword.txt', encoding='UTF-8').readlines()]
    # print(stopwords)
    word_dict = nltk.defaultdict(int)
    words = []
    with open(in_put, 'rb') as f:
        for line in f:
            content = line.decode('gbk').strip().split()
            for word in content[1:]:
                words.append(word.split(u'/')[0])
        clean_words = []
        for i in words:
            if i not in stopwords and u'\u4e00' <= i <= u'\u9fa5':
                clean_words.append(i)
    fw = open(out_put, "w", encoding='UTF-8')
    for i in clean_words:
        fw.write(i + ' ')
    fw.close()
    print("去除字母完成")


def getNgrams(in_put, n, out_put):
    with open(in_put, 'r', encoding="utf-8") as f:
        f = f.read()
        clean_words = []
        clean_words = f.split(' ')
        out_data = {}
        #print(clean_words)
        for i in range(len(clean_words) - n + 1):
            ngram_temp = " ".join(clean_words[i:i + n])  # .encode('utf-8')
            if ngram_temp not in out_data:  # 词频统计
                out_data[ngram_temp] = 0  # 典型的字典操作
            out_data[ngram_temp] += 1
        keys = list(out_data.keys())
        fw = open(out_put, "w", encoding='UTF-8')
        for i in keys:
            fw.write(i + ":" + str(out_data[i]) + '\n')
            #print(i + ": " + str(out_data[i]))
        fw.close()
    print(str(n) + "-gram保存成功！")


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    source_txt = r"C:\Users\yuanhuanfa\Desktop\nlp\1998-01-2003.txt"
    clean_once_txt = r"C:\Users\yuanhuanfa\Desktop\nlp\cleanonce.txt"

    new_source = r"C:\Users\yuanhuanfa\Desktop\nlp\newsource.txt"
    clean_new = r"C:\Users\yuanhuanfa\Desktop\nlp\cleannew.txt"
    #delete_punctuation(new_source, clean_new)

    clean_finish_txt = r"C:\Users\yuanhuanfa\Desktop\nlp\cleanfinish.txt"
    new_txt = r"C:\Users\yuanhuanfa\Desktop\nlp\new.txt"
    #clean_letter(clean_new, new_txt)

    unigram = r"C:\Users\yuanhuanfa\Desktop\nlp\1-gram.txt"
    bigram = r"C:\Users\yuanhuanfa\Desktop\nlp\2-gram.txt"

    getNgrams(clean_finish_txt, 2, bigram)
    getNgrams(clean_finish_txt, 1, unigram)
