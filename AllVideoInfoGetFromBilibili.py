'''
目的：设计爬虫用于获取B站机器学习视频
网页：https://search.bilibili.com/all?keyword=%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97&from_source=webtop_search&spm_id_from=333.851

'''

Url = 'https://search.bilibili.com/all?keyword=%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97&from_source=webtop_search&spm_id_from=333.851'

'''
第一步：请求网页
'''
import requests

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'
}

Get_url = requests.get(Url,headers=headers)
# print(Get_url.text)
# print(Get_url.request.headers)
Get_html = Get_url.text
Get_url.close()
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
urls = re.findall('<li class="i_list list_n2"><a  href=\"(.*?)\" alt=(.*?) title=.*?><img src=\"(.*?)\"',Get_html)
#patren_get_Videoinfo = '</span><a title=\"(.*?)\" href=\"//(.*?)\?from=search\" target=.*? class=.*?><em class=.*?>'
patren_get_keyword = '</span><a title=\"(.*?)\" href=\"//(.*?)\?from=search\" target=.*? class=.*?>.*?<em class="keyword">(.*?)</em>(.*?)<.*?<div class="des hide">(.*?)</div><div class=.*?><span title=\"(.*?)\" class=.*?><i class=.*?></i>\n(.*?)</span>'
patren_get_pageNum = '<li class="page-item last"><button class="pagination-btn">(.*?)</button>'

#get_Videoinfo = re.compile(patren_get_Videoinfo,re.S).findall(Get_html)
#print(get_Videoinfo)
get_Keyword = re.compile(patren_get_keyword,re.S).findall(Get_html)
print(get_Keyword)
get_pageNum = re.compile(patren_get_pageNum,re.S).findall(Get_html)

pageNum = list(filter(str.isdigit, str(get_pageNum)))



'''

# 用于将数据存入excle中
'''
import xlwt
import xlrd
from xlutils.copy import copy
# 创建excel
def crteateExcel():
	create = xlwt.Workbook(encoding='utf-8')
	sheet1 = create.add_sheet(u'video',cell_overwrite_ok=True)
	create.save('test.xls')


Prev_Url = "https://"
crteateExcel()
for page in range(8):

	num = len(get_Keyword)
	# print(get_Keyword[0])
	for i in range(num):
		title = get_Keyword[i][0]
	# print(title)
		video_url = Prev_Url + get_Keyword[i][1]
		video_keword = get_Keyword[i][2]+get_Keyword[i][3]
		video_info = get_Keyword[i][4]
		video_WatchNum = get_Keyword[i][5]+get_Keyword[i][6]
		print(title,':',video_url,video_keword,video_info,video_WatchNum)

		# 存入excel
		excel_file = xlrd.open_workbook('test.xls', formatting_info=True)
		create = copy(wb=excel_file)
		video_sheel = create.get_sheet(0)

		video_sheel.write(i+page*num,0,title)
		video_sheel.write(i+page*num, 1, video_keword)
		video_sheel.write(i+page*num, 2, video_info)
		video_sheel.write(i+page*num, 3, video_WatchNum)
		create.save('test.xls')
	next_Page = Url + '&page=' +str(page+1)
	Get_url = requests.get(next_Page, headers=headers)
	# print(Get_url.text)
	# print(Get_url.request.headers)
	Get_html = Get_url.text
	Get_url.close()
	get_Keyword = re.compile(patren_get_keyword, re.S).findall(Get_html)


'''
第四步 批量获取
'''
# 从https://www.xrmn5.com/UploadFile/pic/9013.jpg 中对应的网页为：https://www.xrmn5.com/XiuRen/2021/20219013.html