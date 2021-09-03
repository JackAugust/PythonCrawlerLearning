import os
import time

dir = r"D:/Let'sFunning/Picture/PythonGet/"
url = "https://pic.xrmn5.com"

import requests

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'
}

URL = "https://www.xrmn5.com/XiuRen/"
WebURL = "https://www.xrmn5.com/"
Get_url = requests.get(URL,headers=headers)
Get_url.encoding = 'utf-8'
Get_html = Get_url.text
print(Get_html)

import re
patrenForPageNum = '</a><a href=\"(.*?)\">'
Get_PageNum = re.compile(patrenForPageNum,re.S).findall(Get_html)
temp = str(Get_PageNum[len(Get_PageNum)-1])
PageNum = "".join(list(filter(str.isdigit, temp)))
print(temp)
print(PageNum)

# 获取所有网页，存入AllPage中
AllPageTemp = []
GetAllPage = ()
for i in range(int(PageNum)):
	if i > 0:
		AllPageTemp.append(WebURL+"/XiuRen/index"+str(i+1)+".html")
GetAllPage += tuple(AllPageTemp)

print(len(GetAllPage))
for pagenum in range(int(PageNum)):
	urls = re.findall('<li class="i_list list_n2"><a  href=\"(.*?)\" alt=(.*?) title=.*?><img class="waitpic" src=\"(.*?)\"', Get_html)
	patren1 = '<div class="postlist-imagenum"><span>(.*?)</span></div></a><div class="case_info"><div class="meta-title">\[.*?\](.*?)</a></div>'
	patren2 = '<div class="meta-post"><i class="fa fa-clock-o"></i>(.*?)<span class="cx_like"><i class="fa fa-eye"></i>(.*?)</span>'
	inforName = re.compile(patren1, re.S).findall(Get_html)
	likeNum = re.compile(patren2, re.S).findall(Get_html)
	print(urls)
	print(inforName)
	print(likeNum)
	num = len(likeNum)

	patren3 = '<img onload=.*? alt=.*? title=.*? src=\"(.*?)\" />'

	for i in range(num):
		if (int(likeNum[i][1]) > 500):
			getImgDir = dir + str(inforName[i][0]) + '/' + str(likeNum[i][0]) + '/' + str(inforName[i][1] + '/')
			# 创建对应目录
			if not os.path.exists(getImgDir):
				os.makedirs(getImgDir)
			imgUrl = url + urls[i][2]
			imgName = getImgDir + urls[i][2].split('/')[-1]
			print(imgName)
			time.sleep(1)
			# 获取封面图片
			Get_Img = requests.get(imgUrl, headers=headers)
			with open(imgName, 'wb') as f:
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
						GetPageImg = url + imgPageUrl[l]
						print(GetPageImg)
						PageImgeName = getImgDir + imgPageUrl[l].split('/')[-1]
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
	Get_url = requests.get(GetAllPage[pagenum],headers=headers)
	Get_url.encoding = 'utf-8'
	Get_html = Get_url.text