import json
import time
from usdt import *
class group:
    def make(groupid,bookname,score):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        huilv=float(user_dict['order'][str(bookname)]['汇率'])
        return huilv*score
    def new(groupid,adminlist):
        with open("group.json",'r',encoding='utf-8') as load_f:
            user_dict_ = json.load(load_f)
            load_f.close()
        user_dict=user_dict_['data']
        if groupid in user_dict:
            pass
        else:
            userdict={
                "adminlist":adminlist,
                "order":{}
            }
            with open("{}.json".format(groupid),'w',encoding='utf-8') as du:
                json.dump(userdict,du)
                du.close()
            user_dict_['data'].append(groupid)
            with open("group.json",'w') as du:
                json.dump(user_dict_,du,ensure_ascii=False)
                du.close()
    def change(adminid,groupid):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
            if adminid in user_dict['adminlist']:
                user_dict['adminlist'].remove(adminid)
            else:
                user_dict['adminlist'].append(adminid)
        with open("{}.json".format(groupid),'w') as du:
                json.dump(user_dict,du,ensure_ascii=False)
                du.close()
    def userinadmin(adminid,groupid):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        if str(adminid) in user_dict['adminlist']:
            return True
        else:
            return False
    def newbook(bookname,groupid):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        user_dict['order'][str(bookname)]={
            "汇率": 7,
            "费率":0,
            "累计入款":0,
            "累计放款":0,
            "流水":[]
        }
        with open("{}.json".format(groupid),'w',encoding='utf-8') as du:
                json.dump(user_dict,du,ensure_ascii=False)
                du.close()
    def load(groupid,bookname):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        book=user_dict['order'][str(bookname)]
        data=book['流水']
        paylist=[]
        getlist=[]
        pay_text=''
        get_text=''
        while len(data) > 0:
            if data[-1]['type']=='入款':
                getlist.append(data[-1])
                get_text+='{}  {}\n'.format(data[-1]['time'],data[-1]['score'])
            else:
                paylist.append(data[-1])
                pay_text+='{}  {}\n'.format(data[-1]['time'],data[-1]['score'])
            data.remove(data[-1])
        return {
            "paylist":paylist,
            "getlist":getlist,
            "pay_text":pay_text,
            "get_text":get_text
        }
    def write(type,score,groupid,bookname):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        user_dict['order'][str(bookname)]["流水"].append({"type":type,"score":score,"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
        user_dict['order'][str(bookname)]['累计{}'.format(type)]+=float(score)
        with open("{}.json".format(groupid),'w',encoding='utf-8') as du:
                json.dump(user_dict,du,ensure_ascii=False)
                du.close()
    def isbookin(groupid,bookname):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        if bookname in user_dict['order']:
            return True
        else:
            return False
    def more(groupid,bookname):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        if user_dict['order'][str(bookname)]['汇率']=='timer':
            user_dict['order'][str(bookname)]['汇率']==usdt.huilv()
        return user_dict['order'][str(bookname)]
    def sethuilv(groupid,bookname,huilv):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        user_dict['order'][str(bookname)]['汇率']=huilv
        with open("{}.json".format(groupid),'w',encoding='utf-8') as du:
                json.dump(user_dict,du,ensure_ascii=False)
                du.close()
    def setfeelv(groupid,bookname,feelv):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        user_dict['order'][str(bookname)]['费率']=feelv
        with open("{}.json".format(groupid),'w',encoding='utf-8') as du:
                json.dump(user_dict,du,ensure_ascii=False)
                du.close()
    def getfeelv(groupid,bookname):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        return user_dict['order'][str(bookname)]['费率']
    def gethuilv(groupid,bookname):
        with open("{}.json".format(groupid),'r',encoding='utf-8') as du:
            user_dict = json.load(du)
            du.close()
        if user_dict['order'][str(bookname)]['汇率'] == 'timer':
            user_dict['order'][str(bookname)]['汇率']=usdt.huilv()
        return user_dict['order'][str(bookname)]['汇率']
    
    