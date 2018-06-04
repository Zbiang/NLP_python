a = input()
b = input()

c = [0]*len(b)

for i in range(len(b)):
    c[i] = i + 1

print(c)

for i in range(len(a)):
    tmp = a[i]
    for j in range(len(b)):
        js = len(b) - 1 - j
        print(js)

        if js == 0:
            editD = i
        else:
            editD = c[js-1]

        if tmp != b[js]:
            editD += 1

        if editD < ++c[js]:
            c[js] = editD
            print(js,editD)
        print(i,c)

    for j in range(len(b)-1):
        if c[j+1] > (c[j] + 1):
            c[j+1] = c[j] + 1
print(c)
print(c[len(b)-1])

# 我的饭卡忘在了图书馆一楼了，我改怎么版   补办校园卡在学生服务大厅
# 你的饭卡丢了图书干，你不知道怎么        分词文本编辑距离相似度校园卡
# 杀马特啊图书，怎么了
