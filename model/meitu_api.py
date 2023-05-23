import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
from tornado.options import define, options
import logging

import requests
import base64
import json
import time
import pdb

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    
from _key_store import MT_APPID ,MT_APPKEY ,MT_SECRETID

class ModelMeiTuAPI(object):
    def __init__(self):
        self.headers = {'Content-Type':'application/json'}
        
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
        return resp
        
    
    def body_recognize(self,recognize,para):
        if recognize=='contour':
            url='https://openapi.mtlab.meitu.com/v1/BodyContour'
        elif recognize=='pose':
            url='https://openapi.mtlab.meitu.com/v1/BodyPose'
        elif recognize=='apperal':
            'https://ai.meitu.com/doc?id=85&type=api&lang=zh'
            url='https://openapi.mtlab.meitu.com/v1/apperal'
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
        pdb.set_trace()
        return resp
        
if __name__ == '__main__':
    mta  = ModelMeiTuAPI()
    pb = open('mt_mfa.jpg','rb').read()
    para={'photo':base64.b64encode(pb)}
    mta.body_recognize('apperal',para)
    # pdb.set_trace()
    # mta.macro_facial_analysis(para)