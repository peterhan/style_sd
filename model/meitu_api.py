#!coding:utf8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
from tornado.options import define, options
import logging

import traceback
import base64
import json
import time
import pdb


from jsonpath_ng import jsonpath, parse
import requests

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    
from _key_store import MT_APPID ,MT_APPKEY ,MT_SECRETID

class ModelMeiTuAPI(object):
    def __init__(self):
        self.headers = {'Content-Type':'application/json'}
        
    def micro_facial_analysis(self,para):
        url='https://openapi.mtlab.meitu.com/v1/micro_facial_analysis'
        url +='?api_key=%s&api_secret=%s'%(MT_APPKEY,MT_SECRETID)
        confd={
          "media_info_list": [{'media_data':para.get('photo')
                ,'media_profiles':{'media_data_type':'jpg'}
            }],
          "parameter": {'return_attributes':'facial_analysis'
                ,'return_landmark':3},
          "extra": {}          
        }
        #confd.update(para)
        payload = json.dumps(confd)
        resp = requests.request("POST", url, headers=self.headers, data=payload)
        #pdb.set_trace()
        return resp.json()
        
    def macro_facial_analysis(self,para):
        '''https://ai.meitu.com/doc?id=49&type=api&lang=zh
        '''
        url='https://openapi.mtlab.meitu.com/v2/macro_facial_analysis'
        url +='?api_key=%s&api_secret=%s'%(MT_APPKEY,MT_SECRETID)
        
        confd={
          "media_info_list": [{'media_data':para.get('photo')
                ,'media_profiles':{'media_data_type':'jpg'}
            }],
          "parameter": {'return_attributes':'gender,age,race,beauty,glasses,mustache,emotion,eyelid,poseestimation'
                ,'return_landmark':2},
          "extra": {}          
        }
        #confd.update(para)
        payload = json.dumps(confd)
        resp = requests.request("POST", url, headers=self.headers, data=payload)
        #pdb.set_trace()
        return resp.json()
        
    
    def body_recognize(self,recognize,para):
        if recognize=='contour':
            url='https://openapi.mtlab.meitu.com/v1/BodyContour'
        elif recognize=='pose':
            url='https://openapi.mtlab.meitu.com/v1/BodyPose'
        elif recognize=='apperal':
            'https://ai.meitu.com/doc?id=85&type=api&lang=zh'
            url='https://openapi.mtlab.meitu.com/v1/apperal'
        elif recognize=='HumanDetect':
            url='https://openapi.mtlab.meitu.com/v1/HumanDetect'
        elif recognize=='ornaments':
            url='https://openapi.mtlab.meitu.com/v1/Ornaments'
        url +='?api_key=%s&api_secret=%s'%(MT_APPKEY,MT_SECRETID)
        confd={
          "media_info_list": [{'media_data':para.get('photo')
                ,'media_profiles':{'media_data_type':'jpg'}
            }],
          "parameter": {},
          "extra": {}          
        }
        payload = json.dumps(confd)
        resp = requests.request("POST", url, headers=self.headers, data=payload)
        # pdb.set_trace()
        return resp.json()
        
        
    def body_fat_rate(self,para):
        jo = self.body_recognize('HumanDetect',para)
        try:
            # print res
            res = parse('$.media_info_list[0].media_extra.HumanDetect[0]').find(jo)
            rect_arr=res[0].value
            if len(rect_arr)!=4:
                raise Exception('HumanDetect result list short than 4')
        except:
            logging.warn(traceback.format_exc())
            return False
        w=rect_arr[2]-rect_arr[0]
        h=rect_arr[3]-rect_arr[1]
        rate =  h/w
        return rate
        
    def total_process(self,para):
        # mic = self.micro_facial_analysis(para)
        # print mic
        # micv= parse("$.media_info_list[0].media_extra.faces[0].face_rectangle").find(mic)
        # time.sleep(1)
        # farr= micv[0].value
        # frate = farr['height']/farr['width']
        mac = self.macro_facial_analysis(para)
        flds = ['gender','age','race','beauty_score','emotion','mustache_thick']
        macv=parse("$.media_info_list[0].media_extra.faces[0].face_attributes"
            +".%s"%flds).find(mac)
        '''gender 	Object 	"gender": {"value": 1} 性别分析结果，value的值为1代表男性，0代表女性
age 	Object 	"age": {"value": 21} 年龄分析结果，value的值为一个非负整数，标识估计的年龄
race 	Object 	"race":{"value": 0} 人种分析结果，value的值为0代表白人，1代表亚洲人，2代表黑人，3代表印度北方人，4代表印度南方人，5代表东南亚人
beauty_score 	Object 	"beauty_score":{"value": 90} 颜值分析，数值0-100
emotion 	Object 	"emotion":{"value": 0} 情绪分析结果，value的值为 0代表伤心，1代表平静，2代表微笑，3代表大笑，4代表惊讶，5代表恐惧，6代表愤怒，7代表厌恶
mustache_thick 	Object 	"mustache_thick":{"value": 0} 胡子浓密分析结果，value的值为0代表无胡须，1代表稀疏，2代表浓密
        '''
        s='''1代表男性，0代表女性
        age
        1代表亚洲人，2代表黑人，3代表印度北方人，4代表印度南方人，5代表东南亚人
        score
        0代表伤心，1代表平静，2代表微笑，3代表大笑，4代表惊讶，5代表恐惧，6代表愤怒，7代表厌恶
        0代表无胡须，1代表稀疏，2代表浓密
        '''
        mapd=[]
        for i,l in enumerate(s.splitlines()):
            if l.find('，')==-1:
                mapd.append({})
            else:
                ed = dict([p.split(':') for p in l.strip().replace('代表',':').split('，')])
                mapd.append(ed)
        time.sleep(0.1)
        # parse('$.').find(mac)[0].value
        brate = self.body_fat_rate(para)
        # pdb.set_trace()
        res={}
        for  i, e in enumerate(macv):
            key = flds[i]
            vlu = str(e.value['value'])
            print key,mapd[i],vlu
            res[key]=mapd[i].get(vlu,vlu)
        res['body_hw_rate']='%.4f'%brate
        # if frate<0.
        if brate<3.2:
            blvl ='fat'
        elif brate<3.7:
            blvl ='fit'
        else:
            blvl ='thin'
        res['body_fit']=blvl
        print json.dumps(res,ensure_ascii=False).decode('utf8').encode('gbk')
        return res
        
        
if __name__ == '__main__':
    mta  = ModelMeiTuAPI()
    import time
    for pic in ('mt_mfa.jpg','mt_fatman.jpg'):
        pb = open(pic,'rb').read()
        para={'photo':base64.b64encode(pb)}
        mta.total_process(para)
        
    # pdb.set_trace()
    # mta.macro_facial_analysis(para)