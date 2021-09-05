'''
实现校园网自动登录
未实现

'''
import requests

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'
}

# <meta http-equiv="Content-Type" content="text/html" charset="GBK">

url = 'http://10.10.1.96/eportal/index.jsp?wlanuserip=5cf5203796ae86c77764bc6155920e41&wlanacname=41b15a45cb2b73db&ssid=56869b60ef8e26b8&nasip=413da7e798b5ff3a938123ae62686639&mac=e9dc34e120f7a31138992b6336e5d903&t=wireless-v2&url=1c8aaf9da2c033d1072be8e29c46c695229ab1c8b1319b6e'
#url = 'http://10.10.1.96/eportal/success.jsp?userIndex=34313364613765373938623566663361393338313233616536323638363633395f31302e31302e31392e3135315f31383234313030303039&keepaliveInterval=0'

# 这里会出现：document.getElementById("username")
# 和 document.getElementById("pwd") 用于获取用户名和密码

# password cookie :1148b233cda419b89e74e376b79943223a85e7531236eac4ac626778a7411a8d943a01a49423b2000af5f4844e1336e4cbf8379939777413d11f06bb234e75fca67650d484aaaa223016cb3189bbea789f1b83ef56b9baa545f9bdc147fd7c1e304504cbd3742f8e82539bfa21ec6163bd076df81a7b05d365e8caf3e2d2d484
import urllib.request,urllib.parse

user_infor = {
	"username":"1824100009",
	"pwd":"0151449"
}
user_data = bytes(urllib.parse.urlencode(user_infor),encoding='GBK')
url_req = urllib.request.Request(url=url,data=user_data,headers=headers)
url_res = urllib.request.urlopen(url_req)

print(url_res.read().decode('GBK'))

'''
# urllib 用法测试

import urllib.parse
dict = {"word":"hello"}
URL = "http://httpbin.org/post"
data_test = bytes(urllib.parse.urlencode(dict),encoding='utf-8')
req = urllib.request.Request(url=URL,data=data_test,headers=headers)
res = urllib.request.urlopen(req)
print(res.read().decode('utf-8'))

'''
