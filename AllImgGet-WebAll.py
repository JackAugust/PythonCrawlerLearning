import os
import time
import urllib3
urllib3.disable_warnings()
import socket

dir = r"D:/Let'sFunning/Picture/PythonGet/"
url = "https://www.xrmn5.com/"
# 目前网站没了。。。
# https://xrhub.cc/image_type/XiuRen

# 解决ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。
# 链接：
# https://blog.csdn.net/IllegalName/article/details/77164521?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task

# 设置超时时间
time_out = 60
socket.setdefaulttimeout(20*time_out)

import requests

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84',
	'Connection':'close'
}

URL = "https://www.xrmn5.com/XiuRen/"
WebURL = "https://www.xrmn5.com/"

time.sleep(1)

# 去除添加ssh无认证下的红色警告
# https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
requests.packages.urllib3.disable_warnings()

Get_url = requests.get(URL,headers=headers,timeout=time_out,verify=False)
Get_url.encoding = 'utf-8'
Get_html = Get_url.text
# 关闭当前链接
Get_url.close()
# print(Get_html)

import re
patrenForPageNum = '</a><a href=\"(.*?)\">'
Get_PageNum = re.compile(patrenForPageNum,re.S).findall(Get_html)
temp = str(Get_PageNum[len(Get_PageNum)-1])
PageNum = "".join(list(filter(str.isdigit, temp)))

# 获取所有网页，存入AllPage中
AllPageTemp = []
GetAllPage = ()
for i in range(int(PageNum)):
	if i > 0:
		AllPageTemp.append(WebURL+"/XiuRen/index"+str(i+1)+".html")
GetAllPage += tuple(AllPageTemp)

print('GetAllPage:',len(GetAllPage))
print('PageNum:',PageNum)
for pagenum1 in range(int(len(GetAllPage))):
	urls = re.findall('<li class="i_list list_n2"><a  href=\"(.*?)\" alt=(.*?) title=.*?><img class="waitpic" src=\"(.*?)\"', Get_html)
	patren1 = '<div class="postlist-imagenum"><span>(.*?)</span></div></a><div class="case_info"><div class="meta-title">\[.*?\](.*?)</a></div>'
	patren2 = '<div class="meta-post"><i class="fa fa-clock-o"></i>(.*?)<span class="cx_like"><i class="fa fa-eye"></i>(.*?)</span>'
	inforName = re.compile(patren1, re.S).findall(Get_html)
	likeNum = re.compile(patren2, re.S).findall(Get_html)
	print(urls)
	print(inforName)
	print(len(likeNum),likeNum)
	num = len(likeNum)
	#pagenum = int(len(GetAllPage)) - pagenum1 - 67
	pagenum = int(len(GetAllPage))-pagenum1-1
	# pagenum = pagenum1;
	patren3 = '<img onload=.*? alt=.*? title=.*? src=\"(.*?)\" />'

	for i in range(num):
		if (int(likeNum[i][1]) > 800):
			getImgDir = dir + str(inforName[i][0]) + '/' + str(likeNum[i][0]) + '/' + str(inforName[i][1] + '/')
			file_num = re.findall('\d+',getImgDir)

			# 创建对应目录
			if not os.path.exists(getImgDir):
				os.makedirs(getImgDir)
			else:
				if (len(os.listdir(getImgDir)) >= (int(file_num[-1]))):
					print("此目录",getImgDir,"已存在：", len(os.listdir(getImgDir)),"个文件\n")
					continue
					#break
			imgUrl = url + urls[i][2]
			imgName = getImgDir + urls[i][2].split('/')[-1]
			print(imgUrl,imgName)

			# 获取封面图片
			if os.path.isfile(imgName):
				print("此封面已存在：", imgName)
			else:
				time.sleep(1)
				try:
					requests.packages.urllib3.disable_warnings()
					Get_Img = requests.get(imgUrl, headers=headers,timeout=time_out,verify=False)
					with open(imgName, 'wb') as f:
						f.write(Get_Img.content)
					Get_Img.close()
				except Exception as e:
					print('get the first img with the error:  %s ' % e)
					time.sleep(1)
					requests.packages.urllib3.disable_warnings()
					Get_Img = requests.get(imgUrl, headers=headers, timeout=time_out, verify=False)
					with open(imgName, 'wb') as f:
						f.write(Get_Img.content)
					Get_Img.close()
			# 进入具体网页
			IntoPageUrl = WebURL + urls[i][0]
			print("当前写真网页为：",IntoPageUrl)
			time.sleep(1)
			try:
				requests.packages.urllib3.disable_warnings()
				Get_InPage = requests.get(IntoPageUrl, headers=headers,timeout=time_out,verify=False)
				Get_InPage.encoding = 'utf-8'
				Get_InPagehtml = Get_InPage.text
				Get_InPage.close()
			except Exception as e:
				print('get the img page with the error:  %s ' % e)
				time.sleep(1)
				requests.packages.urllib3.disable_warnings()
				Get_InPage = requests.get(IntoPageUrl, headers=headers, timeout=time_out, verify=False)
				Get_InPage.encoding = 'utf-8'
				Get_InPagehtml = Get_InPage.text
				Get_InPage.close()

			AllPage = re.findall('</a><a href=\"(.*?)\">([0-9]*)', Get_InPagehtml)

			for k in range(len(AllPage)):
				imgPageUrl = re.compile(patren3, re.S).findall(Get_InPagehtml)
				PageNum = len(imgPageUrl)
				# 循环获取并保存图片
				for l in range(PageNum):
					GetPageImg = url + imgPageUrl[l]
					print(GetPageImg)
					PageImgeName = getImgDir + imgPageUrl[l].split('/')[-1]
					print(PageImgeName)

					# 获取内部图片
					if os.path.isfile(PageImgeName):
						print("此图片已存在：",PageImgeName)
						continue

					else:
						try:
							time.sleep(1)
							requests.packages.urllib3.disable_warnings()
							Get_PImg = requests.get(GetPageImg, headers=headers,timeout=time_out,verify=False)
							with open(PageImgeName, 'wb') as f:
								f.write(Get_PImg.content)
							Get_PImg.close()
						except Exception as e:
							time.sleep(1)
							requests.packages.urllib3.disable_warnings()
							Get_PImg = requests.get(GetPageImg, headers=headers, timeout=time_out,verify=False)
							print('get the next img with the error:  %s ' % e)
							with open(PageImgeName, 'wb') as f:
								f.write(Get_PImg.content)
							Get_PImg.close()
				if k == len(AllPage) - 1:
					print("当前信息：",AllPage[k])
					continue

				# 继续下一页获取图片
				NewPaperUrl = WebURL + AllPage[k][0]
				print("开始下一页：",NewPaperUrl)
				time.sleep(1)
				requests.packages.urllib3.disable_warnings()
				Get_InPage = requests.get(NewPaperUrl, headers=headers,timeout=time_out)
				Get_InPage.encoding = 'utf-8'
				Get_InPagehtml = Get_InPage.text
				Get_InPage.close()
	print("开始下一轮：",GetAllPage[pagenum])
	try:
		time.sleep(1)
		requests.packages.urllib3.disable_warnings()
		Get_url = requests.get(GetAllPage[pagenum],headers=headers,timeout=time_out)
		Get_url.encoding = 'utf-8'
		Get_html = Get_url.text
		Get_url.close()
	except Exception as e:
		print('get the next info page with the error:  %s ' % e)
		requests.packages.urllib3.disable_warnings()
		Get_url = requests.get(GetAllPage[pagenum],headers=headers,timeout=time_out)
		Get_url.encoding = 'utf-8'
		Get_html = Get_url.text
		Get_url.close()