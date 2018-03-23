#!/usr/bin/python3
'''
功能：对华为云常用API接口进行封装
版权信息:华为技术有限公司，版权所有(C)2018-2019
作者：qshujun
修改记录：2018/02/28v1.0
'''

importos
importtime
importjson
fromHttpRequestimportHttpRequests


classHWCloud():

def__init__(self,domain_name,username,password,region_id):
self.domain_name=domain_name
self.username=username
self.password=password
self.region_id=region_id
self.token_file="token"
self.iam_endpoint="https://iam.{region_id}.myhuaweicloud.com"
self.iam_token_uri="/v3/auth/tokens"
self.smn_endpoint="https://smn.{region_id}.myhuaweicloud.com"
self.sms_publish_uri="/v2/{project_id}/notifications/sms"
self.headers={"content-type":"application/json"}
self.project_id=""
self.proxies=None
self.get_iam_token()


defget_iam_token(self):
'''
以用户名、密码从IAN换取token并加入headers
:return:
'''
#先尝试从本地文件读取尚在有效期内的token
ifos.path.isfile(self.token_file):
try:
f=open(self.token_file)
token_str=f.read()
f.close()
token_info=json.loads(token_str)
iftoken_info["expires_at"]>time.time():
self.headers["X-Auth-Token"]=token_info["token"]
self.project_id=token_info["project_id"]
returnTrue
except:
pass

iam_token_url=self.iam_endpoint.format(region_id=self.region_id)+self.iam_token_uri
data={
"auth":{
"identity":{
"methods":[
"password"
],
"password":{
"user":{
"name":self.username,
"password":self.password,
"domain":{
"name":self.domain_name
}
}
}
},
"scope":{
"project":{
"name":self.region_id
}
}
}
}
auth_timestamp=time.time()
req=HttpRequests(iam_token_url,data=json.dumps(data),type="POST",headers=self.headers,proxies=self.proxies)
print(req.get_text())
ifreq.get_code()==201and"X-Subject-Token"inreq.get_headers():
self.headers["X-Auth-Token"]=req.get_headers()["X-Subject-Token"]
req_text=json.loads(req.get_text())
self.project_id=req_text["token"]["project"]["id"]
issued_at=req_text["token"]["issued_at"]
expires_at=req_text["token"]["expires_at"]
expires_timestamp=auth_timestamp+time.mktime(time.strptime(expires_at,"%Y-%m-%dT%H:%M:%S.%fZ"))-time.mktime(time.strptime(issued_at,"%Y-%m-%dT%H:%M:%S.%fZ"))
token_info={
"token":req.get_headers()["X-Subject-Token"],
"project_id":self.project_id,
"expires_at":expires_timestamp
}
f=open(self.token_file,'w')
f.write(json.dumps(token_info))
f.close()
returnTrue
else:
print("GetIAMtokenfailed,httpcode:%s,%s"%(str(req.get_code()),req.get_text()))
returnFalse

defsendSms(self,sign_id,endpoint,message):
'''
:paramsign_id:短信签名
:paramendpoint:手机号码
:parammessage:短信消息
:return:
'''
sms_publish_url=self.smn_endpoint.format(region_id=self.region_id)+self.sms_publish_uri.format(project_id=self.project_id)
data={
"endpoint":endpoint,
"message":message,
"sign_id":sign_id
}
req=HttpRequests(sms_publish_url,data=json.dumps(data),type="POST",headers=self.headers,proxies=self.proxies)
ifreq.get_code()==200:
returnTrue
else:
print("SendSMSfailed,httpcode:%s,%s"%(str(req.get_code()),req.get_text()))
returnFalse

if__name__=='__main__':
client=HWCloud('domain_name','username','Password','cn-north-1')
client.sendSms('dddabcde*********************66','181xxxxx110','hello')
依赖的外部HttpRequests类

#!/usr/bin/python
#coding:utf-8

importrequests

classHttpRequests():
'''
对requests库封装的GET、POST、PUT等方法调用类
'''

def__init__(self,url,data=None,type='GET',cookie=None,headers=None,proxies=None):
self.url=url
self.data=data
self.type=type
self.cookie=cookie
self.headers=headers
self.proxies=proxies
self.send_request()

defsend_request(self):
'''
setuparequest
'''

ifself.url==Noneorself.url=='':
raise'Theurlshouldnotempty!'
ifself.type=='POST':
self.req=requests.post(self.url,data=self.data,headers=self.headers,proxies=self.proxies)
elifself.type=='GET':
ifself.data==None:
self.req=requests.get(self.url,headers=self.headers,proxies=self.proxies)
else:
self.req=requests.get(self.url,params=self.data,headers=self.headers,proxies=self.proxies)
elifself.type=='PUT':
self.req=requests.put(self.url,data=self.data,headers=self.headers,proxies=self.proxies)
else:
self.req=None
raise'ThehttprequesttypeNOTsupportnow!'

defget_code(self):
try:
returnself.req.status_code
except:
raise'getcodefail'

defget_url(self):
try:
returnself.req.url
except:
raise'geturlfail'

defget_text(self):
try:
returnself.req.text
except:
raise'gettextfail'

defget_headers(self):
try:
returnself.req.headers
except:
raise'getheadersfail'

defget_cookie(self):
headers=self.get_headers()
if'set-cookie'inheaders:
returnheaders['set-cookie']
else:
returnNone
