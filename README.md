# PythonCrawlerLearning

这是一个以学习爬虫为目的的自用无商业化的github项目，不针对任何网站，仅用于爬虫学习
若爬取网站过程涉及到您的财产损失，请及时告知以便停止操作

## 1. 美女图片爬取
### - 结构说明：
目前主要代码有：
main.py 用于第一步：从一个网页中获取到当前网页图片
AllImgGet.py 用于第二步，从一个网页深入到具体图片网页来获取网页对应所有图片
AllImgGet-WebAll.py 用于第三步，从一个网站上获取到对应网页的具体图片，即爬网站
### - 存储地址：
存储地址设置为 D盘 Let'sFunning 文件夹中的 Picture 文件夹中的 PythonGet 文件夹中，以人名+时间+专辑的方式存储爬取到的图片
`dir = r"D:/Let'sFunning/Picture/PythonGet/"`
修改此处即可
### - 图片判断机制
针对的网站为：[https://www.xrmn5.com/](https://www.xrmn5.com/)
其网站图片拥有参数为 `查看次数`，设置为超过500次观看即将其爬取

可修改 WebURL 即可更换网站，但下面解析出需重新修改（较为简单）
`WebURL = "https://www.xrmn5.com/"`
### - 结果展示
