'''
目的：设计爬虫用于获取网站图片
网页：https://www.xrmn5.com/
图片：资源存于：/uploadfile/202109/1/D5201016929.jpg
图片获取：https://pic.xrmn5.com/Uploadfile/202109/1/D5201016929.jpg
已实现：1.获取当前网页的图片——即封面；2.获取当前网页的具体链接并进入获取专辑所有图片
'''

'''
第一步：请求网页
'''
import requests

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'
}

WebURL = "https://www.xrmn5.com/"

Get_url = requests.get(WebURL,headers=headers)
# print(Get_url.text)
# print(Get_url.request.headers)
Get_html = Get_url.text

'''
第二步：解析网页
'''

import re
# 正则表达式对应的为：
# (.*?):获取（）内的所有
# \"(.*?)\" 用于匹配网页
# re.findall 用于获取（）内的数据并每存为元组
urls = re.findall('<li class="i_list list_n2"><a  href=\"(.*?)\" alt=(.*?) title=.*?><img src=\"(.*?)\"',Get_html)
patren1 = '<div class="postlist-imagenum"><span>(.*?)</span></div></a><div class="case_info"><div class="meta-title">\[.*?\](.*?)</a></div>'
patren2 = '<div class="meta-post"><i class="fa fa-clock-o"></i>(.*?)<span class="cx_like"><i class="fa fa-eye"></i>(.*?)</span>'
inforName = re.compile(patren1,re.S).findall(Get_html)
likeNum = re.compile(patren2,re.S).findall(Get_html)



# <img onload="size(this)" alt=.*? title=.*? src="/uploadfile/202109/1/07201045631.jpg" />
patren3 = '<img onload=.*? alt=.*? title=.*? src=\"(.*?)\" />'

'''
第三步：进一步解析网页
'''
'''
第三步：存储封面
'''
import os
import time

dir = r"D:/Let'sFunning/Picture/PythonGet/"
url = "https://pic.xrmn5.com"

# 创建目录：人名+时间+专辑名
num = len(likeNum)
for i in range(num):
	if (int(likeNum[i][1]) > 500):
		getImgDir=dir+str(inforName[i][0])+'/'+str(likeNum[i][0])+'/'+str(inforName[i][1]+'/')
		# 创建对应目录
		if not os.path.exists(getImgDir):
			os.makedirs(getImgDir)
		imgUrl = url+urls[i][2]
		imgName = getImgDir+urls[i][2].split('/')[-1]
		print(imgName)
		time.sleep(1)
		# 获取封面图片
		Get_Img = requests.get(imgUrl, headers=headers)
		with open(imgName,'wb') as f:
			f.write(Get_Img.content)
		# 进入具体网页
		IntoPageUrl = WebURL + urls[i][0]
		Get_InPage = requests.get(IntoPageUrl, headers=headers)
		Get_InPage.encoding = 'utf-8'
		Get_InPagehtml = Get_InPage.text

		AllPage = re.findall('</a><a href=\"(.*?)\">([0-9]*)', Get_InPagehtml)

		for k in range(len(AllPage)):
			if k == len(AllPage) - 1:
				break
			else:
				imgPageUrl = re.compile(patren3, re.S).findall(Get_InPagehtml)
				PageNum = len(imgPageUrl)
				# 循环获取并保存图片
				for l in range(PageNum):
					GetPageImg = url+imgPageUrl[l]
					print(GetPageImg)
					PageImgeName = getImgDir+imgPageUrl[l].split('/')[-1]
					print(PageImgeName)
					time.sleep(1)
					# 获取封面图片
					Get_PImg = requests.get(GetPageImg, headers=headers)
					with open(PageImgeName, 'wb') as f:
						f.write(Get_PImg.content)


				# 继续下一页获取图片
				NewPaperUrl = WebURL + AllPage[k][0]
				time.sleep(1)
				Get_InPage = requests.get(NewPaperUrl, headers=headers)
				Get_InPage.encoding = 'utf-8'
				Get_InPagehtml = Get_InPage.text


