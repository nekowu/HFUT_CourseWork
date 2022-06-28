# -*- coding: utf-8 -*-
import warnings

import numpy as np
import pandas as pd
import string
from sklearn.preprocessing import LabelEncoder
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.metrics import roc_curve, classification_report, auc
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV

warnings.filterwarnings("ignore")
stemmer = PorterStemmer()
PUNCT_TO_REMOVE = string.punctuation
STOPWORDS = set(stopwords.words("english"))


def text_processing(text):
    text = text.lower()
    text = re.compile(r'https?://\S+|www\.\S+').sub(r'', text)
    text = text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))
    text = " ".join([word for word in str(text).split() if word not in STOPWORDS])
    text = " ".join([stemmer.stem(word) for word in text.split()])
    return text


def ROC_plot(fpr, tpr):  # 画出函数图像
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    plt.xlabel('假正例率(FPR)', fontproperties=font)
    plt.ylabel('真正例率(TPR)', fontproperties=font)
    x = np.arange(0, 1.1, 0.2)
    y = np.arange(0, 1.1, 0.2)
    auc1 = auc(fpr, tpr)
    plt.xticks(x)
    plt.yticks(y)
    plt.plot(fpr, tpr)
    x1 = np.arange(0, 1.0, 0.1)
    plt.plot(x1, x1, color='blue', linewidth=2, linestyle='--', label='AUC=%.4f' % auc1)
    plt.legend(loc='lower right')
    plt.show()


if __name__ == '__main__':
    # 读邮件数据CSV
    train_email = pd.read_csv("data/train.csv", usecols=[2], encoding='utf-8')
    train_label = pd.read_csv("data/train.csv", usecols=[1], encoding='utf-8')
    # 数据中ham有3866条，总数4458，属于不平衡数据集

# 数据预处理
train_email['Email'] = train_email['Email'].apply(text_processing)
# 将内容转为list类型
train_email = np.array(train_email).reshape((1, len(train_email)))[0].tolist()
train_label = np.array(train_label).reshape((1, len(train_email)))[0].tolist()

# 构造训练集和验证集
train_num = int(len(train_email) * 0.7)
data_train = train_email[:train_num]
data_test = train_email[train_num:]
label_train = train_label[:train_num]
label_test = train_label[train_num:]

# 使用词袋模型
vectorizer = CountVectorizer()
# CountVectorizer类把文本全部转换为小写，进行文本的词频统计与向量化。
data_train_cnt = vectorizer.fit_transform(data_train)
data_test_cnt = vectorizer.transform(data_test)

# 变成TF-IDF矩阵
transformer = TfidfTransformer()
data_train_tfidf = transformer.fit_transform(data_train_cnt)
data_test_tfidf = transformer.transform(data_test_cnt)

# 以上两步可用下面替代，TfidfVectorizer 相当于 CountVectorizer 和 TfidfTransformer 的结合使用
# vectorizer_tfidf = TfidfVectorizer(sublinear_tf=True)
# data_train_tfidf = vectorizer_tfidf.fit_transform(data_train)
# data_test_tfidf = vectorizer_tfidf.transform(data_test)


# 利用贝叶斯的方法
clf = MultinomialNB(alpha=0.2)
clf.fit(data_train_tfidf, label_train)
score = clf.score(data_test_tfidf, label_test)
print("NB score: ", score)

# 利用SVM的方法
svm = LinearSVC(C=4, random_state=0)
svm.fit(data_train_tfidf, label_train)
score = svm.score(data_test_tfidf, label_test)
print("SVM score: ", score)

# # 利用随机森林的方法，n_estimators是森林中树木的数量，即基评估器的数量，越大，模型的效果往往越好。
# random_state固定时，随机森林中生成是一组固定的树，但每棵树依然是不一致的。max_depth如果为None，则将节点展开，直到所有叶子都是纯净的
rf = RandomForestClassifier(random_state=0, n_estimators=161, max_depth=None, verbose=0, n_jobs=-1)
rf.fit(data_train_tfidf, label_train)
score = rf.score(data_test_tfidf, label_test)
print("RF score: ", score)

# [0.001, 0.01, 0.1, 1, 10, 100]
# clf1 = MultinomialNB()
# param_grid = {'alpha': np.arange(0, 10, 0.1)}
# grid = GridSearchCV(clf1, param_grid, cv=5)
# grid.fit(data_train_tfidf, label_train)
# print("最佳参数为:")
# print(grid.best_params_)
# print("最佳分数为:")
# print(grid.best_score_)


# 随机森林调n_estimators
# scorel = []
# for i in range(0, 200, 10):
#     rfc = RandomForestClassifier(n_estimators=i + 1, n_jobs=-1, random_state=0)
#     score = cross_val_score(rfc, data_train_tfidf, label_train, cv=10).mean()
#     scorel.append(score)
# print(max(scorel), '使分数最高的n_estimators值为：', scorel.index(max(scorel)) * 10 + 1)
# plt.figure()
# plt.plot(range(1, 201, 10), scorel)
# plt.show()

# # 调整max_depth
# param_grid = {'max_depth': np.arange(1, 20, 1)}  # 字典这里也可以输入多个参数
# rfc = RandomForestClassifier(n_estimators=161, random_state=0)  # 这里使用上面得到的最佳n_estimators值
# GS = GridSearchCV(rfc, param_grid, cv=5)  # cv为交叉验证的个数
# GS.fit(data_train_tfidf, label_train)
# print("最佳参数为:")
# print(GS.best_params_)
# print("最佳分数为:")
# print(GS.best_score_)

# param_grid = {'C': np.arange(1, 20, 1),
#               'random_state': [0]}
# grid = GridSearchCV(svm, param_grid, cv=5)
# grid.fit(data_train_tfidf, label_train)
# print(grid.best_params_)
# print(grid.best_score_)

# 预测结果混淆矩阵
result_svm = svm.predict(data_test_cnt)
result_nb = clf.predict(data_test_cnt)
result_rf = rf.predict(data_test_tfidf)
print("贝叶斯混淆矩阵\n", confusion_matrix(label_test, result_nb))
print("随机森林混淆矩阵\n", confusion_matrix(label_test, result_rf))
print("SVM混淆矩阵\n", confusion_matrix(label_test, result_svm))

# 预测结果的分类报告
print('贝叶斯分类报告\n' + classification_report(label_test, result_nb, target_names=['ham', 'spam']))
print('随机森林分类报告\n' + classification_report(label_test, result_rf, target_names=['ham', 'spam']))
print('SVM分类报告\n' + classification_report(label_test, result_svm, target_names=['ham', 'spam']))
# macro avg表示宏平均，表示所有类别对应指标的平均值（（precision.ham+precision.spam）/2）
# weighted avg表示带权重平均，表示类别样本占总样本的比重与对应指标的乘积的累加和
# （（precision.ham * support.ham /support +precision.spam * support.spam /support））
# 验证模型的性能
# 交叉验证用于评估模型的预测性能，尤其是训练好的模型在新数据上的表现，可以在一定程度上减小过拟合。cv：交叉验证生成器或可迭代的次数
# 进行交叉验证数据评估, 数据分为5部分, 每次用一部分作为测试集，输出5次交叉验证的准确率
accuracy = cross_val_score(clf, data_train_tfidf, label_train, cv=5, scoring='accuracy')
print('朴素贝叶斯交叉验证准确率：')
print(accuracy.mean())
accuracy = cross_val_score(rf, data_train_cnt, label_train, cv=5, scoring='accuracy')
print('随机森林交叉验证准确率：')
print(accuracy.mean())
accuracy = cross_val_score(svm, data_train_cnt, label_train, cv=5, scoring='accuracy')
print('SVM交叉验证准确率：')
print(accuracy.mean())

# 将标签转为数值
class_le = LabelEncoder()
y_train_n = class_le.fit_transform(label_train)
y_test_n = class_le.fit_transform(label_test)
# 预测的概率
pred_nb = clf.predict_proba(data_test_tfidf)
pred_svm = svm._predict_proba_lr(data_test_tfidf)
pred_rf = rf.predict_proba(data_test_tfidf)
# pred[:, 1]每一步切片
fpr, tpr, thresholds = roc_curve(y_test_n, pred_nb[:, 1])  # tpr真阳性率=召回率
plt.title('NB_ROC')
ROC_plot(fpr, tpr)

plt.title('RandomForest_ROC')
fpr, tpr, thresholds = roc_curve(y_test_n, pred_rf[:, 1])  # tpr真阳性率=召回率
ROC_plot(fpr, tpr)

plt.title('SVM_ROC')
fpr, tpr, thresholds = roc_curve(y_test_n, pred_svm[:, 1])  # tpr真阳性率=召回率
ROC_plot(fpr, tpr)
