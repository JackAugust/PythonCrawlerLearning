'''
目的：设计爬虫用于获取网站txt
网页：https://www.xbookcn.net/
小说：资源存于：/uploadfile/202109/1/D5201016929.jpg
图片获取：https://pic.xrmn5.com/Uploadfile/202109/1/D5201016929.jpg
已实现：获取当前网页的图片——即封面
'''

'''
第一步：请求网页
'''
import requests

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'
}

TheUrl='http://www.niglas.cas.cn/yjsjy_165790/dsjs/bshshdsh/';
Get_url = requests.get(TheUrl,headers=headers)
Get_url.encoding = 'utf-8'
# print(Get_url)
# print(Get_url.text)
# print(Get_url.request.headers)
Get_html = Get_url.text

'''
如果打印显示：forbidden，说明被禁止爬虫
print(Get_url.request.headers)
会显示：
{'User-Agent': 'python-requests/2.25.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
所以需要进行修改：
去想爬的网页进行F12，获取对应的headers：
添加headers
headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'
}
这个时候再访问就可以绕过去了
Get_url = requests.get('https://www.xrmn5.com/',headers=headers)
'''


'''
第二步：解析网页
'''

import re
# 正则表达式对应的为：
# (.*?):获取（）内的所有
# \"(.*?)\" 用于匹配网页
# re.findall 用于获取（）内的数据并每存为元组
'''
urls = re.findall('<li class="i_list list_n2"><a  href=\"(.*?)\" alt=(.*?) title=.*?><img src=\"(.*?)\"',Get_html)
patren1 = '<div class="postlist-imagenum"><span>(.*?)</span></div></a><div class="case_info"><div class="meta-title">\[.*?\](.*?)</a></div>'
patren2 = '<div class="meta-post"><i class="fa fa-clock-o"></i>(.*?)<span class="cx_like"><i class="fa fa-eye"></i>(.*?)</span>'
inforName = re.compile(patren1,re.S).findall(Get_html)
likeNum = re.compile(patren2,re.S).findall(Get_html)
'''
patrenForTeacher = '<a href=".(.*?)" target="_blank" title="(.*?)">'
getTeacherUrl = re.compile(patrenForTeacher,re.S).findall(Get_html)
getTeacherUrl=getTeacherUrl[-22:]
# print(getTeacherUrl)

patrenTeacherInfo1 = '<p><span>(.*?)<br />'
patrenTeacherInfo2 = '电话：(.*?)<br />'
patrenTeacherInfo3 = 'E-mail：(.*?)<br />'
patrenTeacherInfo4 = '简历： <br />\n\u3000&nbsp; (.*?)<br />'

InfoDir = 'TeacherInfo/'
for i in range(len(getTeacherUrl)):
	file = open(InfoDir+getTeacherUrl[i][1]+'.txt','a')
	url=TheUrl+getTeacherUrl[i][0];
	print(url)
	Get_TeacherInfo = requests.get(url, headers=headers)
	Get_TeacherInfo.encoding = 'utf-8'
	Get_html = Get_TeacherInfo.text
	#print(Get_html)
	getTeacherInfo1 = re.compile(patrenTeacherInfo1, re.S).findall(Get_html)
	getTeacherInfo2 = re.compile(patrenTeacherInfo2, re.S).findall(Get_html)
	getTeacherInfo3 = re.compile(patrenTeacherInfo3, re.S).findall(Get_html)
	getTeacherInfo4 = re.compile(patrenTeacherInfo4, re.S).findall(Get_html)
	file.write(str(getTeacherInfo1))
	file.write('\n电话：\n'+str(getTeacherInfo2))
	file.write('\nE-mail：\n' + str(getTeacherInfo3))
	file.write('\n简历：\n' + str(getTeacherInfo4))
	file.close()
	print(getTeacherInfo1,getTeacherInfo2,getTeacherInfo3,getTeacherInfo4)
	#break









# 封面图片：规则为：
# https://pic.xrmn5.com/Uploadfile/pic/9023.jpg
# 即https://pic.xrmn5.com 作为前缀，后面拼接/UploadFile/pic/9023.jpg即可获取

'''
第三步：存储封面
'''
import os
import time
'''
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
'''
'''
第四步 批量获取
'''
# 从https://www.xrmn5.com/UploadFile/pic/9013.jpg 中对应的网页为：https://www.xrmn5.com/XiuRen/2021/20219013.html