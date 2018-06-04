a = input()
b = input()

c = [0]*len(b)
al = []
for i in range(len(a)):
    tmp = a[i]
    for j in range(len(b)):
        js = len(b) - 1 - j
        if tmp == b[js]:
            if js == 0:
                c[js] = 1
            else:
                c[js] = c[js-1] + 1
        else:
            if js != 0 and c[js-1] != 0:
                al.append(c[js-1])
            c[js] = 0

for i in range(len(b)):
    if c[i] != 0:
        al.append(c[i])

print(al)

# 自己写的公共子串长度
def LCS(qs, ql):
    word_count = 0

    for a in ql:
        for b in qs:
            if a == b:
                word_count += 1

    return word_count

# 我的饭卡忘在了图书馆一楼了，我改怎么版      补办校园卡
# 你的饭卡丢了图书干，你不知道怎么           补办校园卡在学生服务大厅
# 图书馆开门关门时间
# 图书馆开门时间
