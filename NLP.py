# encoding=utf-8

# 引入结巴分词库
import jieba
import jieba.analyse
import jieba.posseg as pseg

# 引入数学函数库
import math

# 所问的问题
q_question = input("你还想了解什么？？？")
# wordss = pseg.cut(q_question)
# for word, flag in wordss:
#     print(word, flag)
print(jieba.analyse.textrank(q_question, topK=3, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v')))

# 问题集的单字节列表
word_qs = []

# 问题集的分词列表
participle_qs = []

# 为了方便加入问题所创建的列表，加入问题向l中加入即可
l = []
l.append("南京天气怎么样")
l.append("周口天气")
l.append("项城天气怎么样")
l.append("南京近年来发生过哪些灾难")
l.append("今年来南京发生过哪些灾难")
l.append("南京的特大灾难今年来有哪些")



# 将l中的问题放入问题集
for i in range(len(l)):
    word_qs.append(list(l[i]))
    participle_qs.append(list(jieba.cut(l[i], cut_all=False)))

# 单字节所问的问题和分词后所问的问题
participle_ql = list(jieba.cut(q_question, cut_all=False))
word_ql = list(q_question)


def LCS(a, b):
    """
    字符串公共子串求解函数
    :param a: 字符串a对应问题集中的问题
    :param b: 字符串b对应所问的问题
    :return: 返回字符串a和字符串b的公共子串数列表
    """
    c = [0] * len(b)
    al = []
    for i in range(len(a)):
        tmp = a[i]
        for j in range(len(b)):
            js = len(b) - 1 - j
            if tmp == b[js]:
                if js == 0:
                    c[js] = 1
                else:
                    c[js] = c[js - 1] + 1
            else:
                if js != 0 and c[js - 1] != 0:
                    al.append(c[js - 1])
                c[js] = 0

    for i in range(len(b)):
        if c[i] != 0:
            al.append(c[i])
    return al


def LD(qs, ql):
    """
    字符串文本编辑距离求解函数
    :param qs: 字符串qs对应问题集的问题
    :param ql: 字符串ql对应所问的问题
    :return: 返回两个字符串的文本编辑距离
    """
    m, n = len(qs) + 1, len(ql) + 1

    ted_matrix = [[0]*n for i in range(m)]
    for i in range(m):
        ted_matrix[i][0] = i

    for j in range(n):
        ted_matrix[0][j] = j

    for i in range(1, m):
        for j in range(1, n):
            if qs[i - 1] == ql[j - 1]:
                cost = 0
            else:
                cost = 1

            ted_matrix[i][j] = min(ted_matrix[i-1][j] + 1, ted_matrix[i-1][j-1] + cost, ted_matrix[i][j-1] + 1)

    return ted_matrix[m - 1][n - 1]

def key_words(qs, ql):
    qs_theme = jieba.analyse.textrank(qs, topK=3, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    ql_theme = jieba.analyse.textrank(ql, topK=3, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    kwRel = 0
    sum = 0
    for i in ql_theme:
        for j in qs_theme:
            if i[0] == j[0]:
                kwRel += j[1]
    for m in qs_theme:
        sum += m[1]
    return [kwRel, sum]

def getLCSRel(a, b):
    """
    求字符串公共子串相关度
    :param a:
    :param b:
    :return:
    """
    return sum((x*x for x in LCS(a, b))) / (len(a) * len(b))

def getLDRel(qs, ql):
    """
    求字符串文本编辑距离相关度
    :param qs:
    :param ql:
    :return:
    """
    return pow(1 - LD(qs, ql) / max(len(qs), len(ql)), 2)

def getKWRel(qs, ql):
    if key_words(qs, ql)[0] == 0 or key_words(qs, ql) == 0:
        return 0
    return key_words(qs, ql)[0] / key_words(qs, ql)[1]

def getAllRel(a):
    """
    求最后的总相关度合成
    :param a: 四个相关度组成的列表
    :return: 返回总合成相关度
    """
    return math.sqrt(sum((x*x for x in a)) / len(a))

def strToList(l):
    """
    将列表变成字符串
    :param l: 列表
    :return: 返回列表对应的字符串
    """
    str = ""
    for i in range(len(l)):
        str += l[i]
    return str

# 全部问题集对应所问问题的总合成相关度字典
ll = {}

# 将全部的总合成相关度加入到ll字典中，并将问题集中所有问题对应的四类相关度打印出来
for i in range(len(word_qs)):

    qstr = strToList(word_qs[i])
    print(qstr + " 问题相似度:")
    print(qstr + " 问题的分词结果：", participle_qs[i])
    # print("问题的主题词：", jieba.analyse.extract_tags(qstr, topK=3, withWeight=True))
    print("问题的主题词：", jieba.analyse.textrank(qstr, topK=3, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v')))

    print("分词文本编辑距离相似度  --->  " , getLDRel(participle_qs[i], participle_ql))
    print("单字文本编辑距离相似度  --->  " , getLDRel(word_qs[i], word_ql))

    print("分词文本公共子串相似度  --->  " , getLCSRel(participle_qs[i], participle_ql))
    print("单字文本公共子串相似度  --->  " , getLCSRel(word_qs[i], word_ql))

    print("分词公共主题词相似度  --->  ", getKWRel(strToList(participle_ql), qstr))

    a = [getLDRel(participle_qs[i], participle_ql), getLDRel(word_qs[i], word_ql), getLCSRel(participle_qs[i], participle_ql), getLCSRel(word_qs[i], word_ql), getKWRel(strToList(participle_ql), qstr)]

    ll[qstr] = getAllRel(a)

    print("合成相似度  --->  ", getAllRel(a))
    print("\n\n")

print("合成相似度：", ll)
# 对问题集相关度字典进行排序，求出总合成相关度最高的那个对应的问题
lsort = sorted(ll.items(), key=lambda ll:ll[1])[-1]
print("你要问的问题是这个吗？ --->  ", lsort[0])

# jieba.analyse.set_stop_words("jieba-master/extra_dict/stop_words.txt")
# print(jieba.analyse.extract_tags(q_question,topK=10,withWeight=True))

"""
当前只是写出了大概的框架，还未对总合成相关度加以分析改进
问题：
    应该给予分词公共子串和分词文本编辑距离的相关度权重大一些
    分词是不是和主题词一样了，需要进一步的测试
    还有停止词还要不要去除
    对比王天使的代码结果加以改进..._(:з)∠)_
    先就这样（逃...
"""
ls = [1, 2, 3, 4]
for i in range(len(ls)-3):
    print(i)