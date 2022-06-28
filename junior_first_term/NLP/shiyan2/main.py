# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 Double Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import random
from random import randint


def wordListSum(wordList):
    num = 0
    for word, value in wordList.items():
        num += value
    return num


def RandomWord(wordList):
    rand_index = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        rand_index -= value
        if rand_index <= 0:
            return word


def read_gram_dict():
    with open(r"C:\Users\yuanhuanfa\Desktop\nlp\2-gram.txt", 'r', encoding="utf-8") as f:
        f = f.read().splitlines()
        result_dict = {}
        text = []
        for line in f:
            word = line.split(':')
            text.append(word)
        result_dict = dict(text)
    return result_dict


def predict_text():
    result_dict = read_gram_dict()
    words = []
    for i in result_dict.keys():
        words.append(i)
    word_dict = {}
    for i in range(1, len(words)):  # 获得一个二维字典
        if words[i - 1] not in word_dict:
            word_dict[words[i - 1]] = {}
        if words[i] not in word_dict[words[i - 1]]:
            word_dict[words[i - 1]][words[i]] = 0
        word_dict[words[i - 1]][words[i]] += 1
    #print(word_dict)
    length = 100
    chain = ''
    current_word = random.choice(words)
    for i in range(0, length):
        temp = current_word
        current_word = RandomWord(word_dict[current_word])
        cut_word1 = temp.split(' ')[1]
        # chain = chain+temp.split(' ')[0]
        cut_word2 = current_word.split(' ')[0]
        if cut_word1 == cut_word2:
            chain = chain + temp.split(' ')[0]
            temp = current_word
    print("随机生成"+str(length)+"个词的句子："+chain)


if __name__ == '__main__':
    # read_dic_two()
    predict_text()
