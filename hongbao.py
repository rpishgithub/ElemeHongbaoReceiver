import requests
import re
import time


class mtdhb(object):
    def __init__(self):
        self.header={
            'accept':'application/json, text/plain, */*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh - CN, zh;q = 0.9, en;q = 0.8',
            'content-length':'54',
            'content-type':'application/x-www-form-urlencoded',
            'origin':'https://www.mtdhb.com',
            'referer':'https://www.mtdhb.com/login',
            'save-data':'on',
            'user-agent':'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 62.0.3202.62 Safari / 537.36',
            'x-user-token':'null'
        }
        self.login_url='https://api.mtdhb.com/user/login'
        self.receiving_url='https://api.mtdhb.com/user/receiving'
        self.session=requests.Session()

    def login(self,account,password):
        post_data={}
        post_data['account']=account
        post_data['password']=password

        response=self.session.post(self.login_url,data=post_data,headers=self.header)
        if response.status_code==200:
            text=response.text
            list=text.split(",")
            token=list[7]
            self.header['x-user-token']=token.split(":")[1][1:-1]
            self.header['content-length']='18'
            self.header['referer']='https://www.mtdhb.com/'


    def receiving(self,phone,hongbao_url):
        post_data={}
        post_data['phone']=phone
        post_data['url']=hongbao_url
        response=self.session.post(self.receiving_url,data=post_data,headers=self.header)
        print (response.text.split(",")[1].split(":")[1])

class hongbao(object):
    def __init__(self):
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.pinghongbao.com',
            'Save-Data': 'on',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
        }
        self.menu_url="https://www.pinghongbao.com/eleme"
        self.new_id=0
        self.old_id=0
        self.redirect_url="https://www.pinghongbao.com/go/"
        self.hongbao_url=""

    def find_empty_hongbao_id(self):
        response = requests.get(self.menu_url, headers=self.header)
        html = response.content.decode("utf-8")
        pattern = re.compile(r'<span style="color: #d44950;font-weight: 600;" id="(.*?)">(\d)', re.S)
        result = re.findall(pattern, html)
        for item in result:
            if (int(item[1]) < 4):
                return item[0]
        return 0

    def get_id(self):
        self.new_id = self.find_empty_hongbao_id()
        while (self.new_id == 0 or self.new_id==self.old_id):
            self.new_id = self.find_empty_hongbao_id()
        self.old_id=self.new_id
        return self.new_id;

    def get_URL(self):
        response = requests.get(self.redirect_url+self.get_id())
        return response.url



if __name__=='__main__':
    phone=input("Phone:")
    account=input("Account:")
    passowrd=input("Password:")
    user=mtdhb()
    Hongbao=hongbao()
    user.login(account,passowrd)
    while(True):
        user.receiving(phone,Hongbao.get_URL())
        time.sleep(5)