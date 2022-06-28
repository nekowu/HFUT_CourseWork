# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 Double Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

def read_gram_dict(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        f = f.read().splitlines()
        result_dict = {}
        text = []
        for line in f:
            word = line.split(':')
            text.append(word)
        result_dict = dict(text)
    return result_dict


dic = []


# 实现正向最大匹配法
def front_cut_words(raw_sentence, word_dic):
    # 统计词典最长的词
    max_length = max(len(word) for word in dic)
    sentence = raw_sentence.strip()
    words_length = len(sentence)
    cut_word = []
    while words_length > 0:
        max_cut_length = min(max_length, words_length)
        sub = sentence[0: max_cut_length]
        # 进行一轮分词，在左侧切出一个词
        while max_cut_length > 0:
            if sub in dic:
                cut_word.append(sub)
                break
                #只剩一个字
            elif max_cut_length == 1:
                cut_word.append(sub)
                break
            else:
                max_cut_length = max_cut_length - 1
                sub = sub[0: max_cut_length]
        # 将切掉的单词删去
        sentence = sentence[max_cut_length:]
        words_length = words_length - max_cut_length

    words = "/".join(cut_word)
    print(words)
    fw = open(r"C:\Users\yuanhuanfa\Desktop\nlp\front_cut.txt", "w", encoding='UTF-8')
    for i in words:
        fw.write(i)
    fw.close()
    print('正向最大匹配切分完成！')
    # return words


# 逆向最大匹配
def back_cut_words(raw_sentence, words_dic):
    # 找到最大词的长度
    max_length = max(len(word) for word in words_dic)
    sentence = raw_sentence.strip()
    words_length = len(sentence)
    cut_words = []
    while words_length > 0:
        max_cut_length = min(words_length, max_length)
        sub_sentence = sentence[-max_cut_length:]
        while max_cut_length > 0:
            if sub_sentence in words_dic:
                cut_words.append(sub_sentence)
                break
            # 只剩下一个字
            elif max_cut_length == 1:
                cut_words.append(sub_sentence)
                break
            # 都不符合，从左侧去掉一个词，长度减一，继续循环
            else:
                max_cut_length -= 1
                sub_sentence = sub_sentence[-max_cut_length:]
        # 将切掉的单词删去，将切掉的长度减去
        sentence = sentence[0:-max_cut_length]
        words_length -= max_cut_length
    cut_words.reverse()
    words = '/'.join(cut_words)
    print(words)
    fw = open(r"C:\Users\yuanhuanfa\Desktop\nlp\back_cut.txt", "w", encoding='UTF-8')
    for i in words:
        fw.write(i)

    fw.close()
    print('逆向最大匹配切分完成！')
    # return words


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    file_name = r"C:\Users\yuanhuanfa\Desktop\nlp\1-gram.txt"
    read_dict = read_gram_dict(file_name)

    for i in read_dict.keys():
        dic.append(i)
    # print(dic)
    input_str = input('请输入待分词句子:')  # 提示用户输入名字
    # input_str = '在这一年中中国的改革开放和现代化建设继续向前迈进国民经济保持了高增长低通胀的良好发展态势了解开'
    front_cut_words(input_str, dic)
    back_cut_words(input_str, dic)
