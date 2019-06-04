from bs4 import BeautifulSoup

s=html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
<script></script>
"""
bs = BeautifulSoup(s,'html.parser')
# print(bs.text)  # 取出文本内容（去掉标签）
# print(bs.find_all('a'))  # 取出所有的a标签

# for tag in bs.find_all('a'):
#     print(tag.get('href'))    # 取出所有的a标签的href属性

# print(bs.find_all()) # 取出所有标签(深度优先)
for tag in bs.find_all():
        print(tag.name)
print('--'*50)

for tag in bs.find_all():
    if tag.name == 'script':
        tag.decompose()   # decompose() 方法删除标签
print('--'*50)
for tag in bs.find_all():
        print(tag.name)





