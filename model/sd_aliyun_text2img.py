#!coding:utf8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
from tornado.options import define, options
import logging

import datetime
import requests
import json
import base64
import time
import traceback
import pdb

from PIL import Image, PngImagePlugin

if __name__ == '__main__':
    import sys
    sys.path.append('..')

import io    
from PIL import Image, PngImagePlugin
from _key_store import AL_URL,AL_TOKEN
from _prompt import PROMPT


class ModelSDText2IMG(object):
    '''/sdapi/v1/txt2img 文字生图 POST
    /sdapi/v1/img2img 图片生图 POST
    /sdapi/v1/options 获取设置 GET | 更新设置 POST（可用来更新远端的模型）
    /sdapi/v1/sd-models 获取所有的模型 GET
    '''
    def prompt2img(self,para={}):
        url = AL_URL        
        # prompt="handsome chinese male dressed in sport wear sitting in dinning room"
        confd = para
        if 'style' in para:
            k=para['style']
            logging.info('style :%s',k)
            if k  not in PROMPT:
                raise Exception('style not define in _prompt.py')
            confd=PROMPT.get(k,{})
            logging.info('confd :%s',confd)
        
        payload = confd
        
        token = AL_TOKEN
        encoded_token = base64.b64encode(token.encode("utf-8")).decode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": 'Basic %s'%encoded_token
        }
        logging.info('payload:%s',json.dumps(payload,indent=2))
        logging.info(url)
        resp = requests.post(url=url+'/sdapi/v1/txt2img', json=payload, headers=headers)
        # pdb.set_trace()
        try:
            rjo = resp.json()
        except:
            print resp.text
            traceback.print_exc()
        dt=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        ret=[]
        for i,binimg in enumerate(rjo['images']):
            image = Image.open(io.BytesIO(base64.b64decode(binimg.split(",", 1)[0])))
            png_payload = {
                "image": "data:image/png;base64," + binimg
            }
            resp2 = requests.post(url=url+'/sdapi/v1/png-info', json=png_payload, headers=headers)
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", resp2.json().get("info"))
            fname='images/output.%s.%s.png'%(dt,i)            
            image.save(fname, pnginfo=pnginfo)
            ret.append({'url':'/'+fname})
        return ret
   


if __name__ == '__main__':
    sdt  = ModelSDText2IMG()
    logging.getLogger().setLevel(logging.DEBUG)
    sdt.prompt2img({'style':'male_suite'})
    