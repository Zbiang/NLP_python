# encoding=utf-8
import jieba
import jieba.analyse
import cmath
import math

q_question = input("你还想了解什么？？？")

word_qs = list("分词文本编辑距离相似度")
participle_qs = list(jieba.cut("分词文本编辑距离相似度", cut_all=False))

participle_ql = list(jieba.cut(q_question, cut_all=False))
word_ql = list(q_question)

def LCS(a, b):
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

def getLCSRel(a, b):
    return sum((x*x for x in LCS(a, b))) / (len(a) * len(b))

def getLDRel(qs, ql):
    return pow(1 - LD(qs, ql) / max(len(qs), len(ql)), 2)

def getAllRel(a):
    return math.sqrt(sum((x*x for x in a)) / len(a))


print("分词文本编辑距离相似度--->" , getLDRel(participle_qs, participle_ql))
print("单字文本编辑距离相似度--->" , getLDRel(word_qs, word_ql))

print("分词文本公共子串相似度--->" , getLCSRel(participle_qs, participle_ql))
print("单字文本公共子串相似度--->" , getLCSRel(word_qs, word_ql))

a = [getLDRel(participle_qs, participle_ql), getLDRel(word_qs, word_ql), getLCSRel(participle_qs, participle_ql), getLCSRel(word_qs, word_ql)]
print("合成相似度--->", getAllRel(a))

jieba.analyse.set_stop_words("jieba-master/extra_dict/stop_words.txt")
print(jieba.analyse.extract_tags(q_question,topK=10,withWeight=True))
