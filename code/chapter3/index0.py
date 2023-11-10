import re
import sys
import collections

# 用法示例
# import sys # 导入sys模块
# name = sys.argv[1] # 获取第一个参数，即用户输入的名字
# print ("Hello, " + name + "!") # 打印问候语

WORD_RE = re.compile(r'\w+')

# index = {}
index = collections.defaultdict(list)

with open(sys.argv[1],encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1): # 指定索引为1，即从第一行开始
        for match in WORD_RE.finditer(line):
            word = match.group() # 获取匹配的单词
            column_no = match.start() + 1 # 获取单词在行中的起始位置，因为match.start()返回的是起始索引（从0开始）
            location = (line_no, column_no)
            
            # 优化前
            # occurrences = index.get(word, [])
            # occurrences.append(location)
            # index[word] = occurrences

            # 优化后
            # index.setdefault(word, []).append(location)
            index[word].append(location)
for word in sorted(index, key=str.upper):
    print(word, index[word])
