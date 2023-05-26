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
import pdb

from PIL import Image, PngImagePlugin

if __name__ == '__main__':
    import sys
    sys.path.append('..')

import io    
from PIL import Image, PngImagePlugin
from _key_store import AL_URL,AL_TOKEN

class ModelSDText2IMG(object):
    '''/sdapi/v1/txt2img 文字生图 POST
    /sdapi/v1/img2img 图片生图 POST
    /sdapi/v1/options 获取设置 GET | 更新设置 POST（可用来更新远端的模型）
    /sdapi/v1/sd-models 获取所有的模型 GET
    '''
    def prompt2img(self,prompt,para={}):
        url = AL_URL        
        # prompt="handsome chinese male dressed in sport wear sitting in dinning room"
        confd={"prompt": "1man, 25 years- old, full body, wearing long-sleeve white shirt and tie, muscular rand black suit, glasses, drinking coffee, soft lighting, masterpiece, best quality, 8k uhd, dslr, film grain, Fujifilm XT3 photorealistic painting art by midjourney and greg rutkowski <lora:asianmale_v10:0.6> <lora:uncutPenisLora_v10:0.6>,face", "all_prompts": ["1man, 25 years- old, full body, wearing long-sleeve white shirt and tie, muscular rand black suit, glasses, drinking coffee, soft lighting, masterpiece, … face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck", "Steps: 20, Sampler: Euler a, CFG scale: 7, Seed: 2016420300, Size: 512x782, Model hash: f68b37e71f, Model: Taiyi-Stable-Diffusion-1B-Chinese-v0.1"], "styles": ["male"], "job_timestamp": "20230526173704", "clip_skip": 1, "is_using_inpainting_conditioning": False}
        confd.update(para)
        payload = confd
        
        token = AL_TOKEN
        encoded_token = base64.b64encode(token.encode("utf-8")).decode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": 'Basic %s'%encoded_token
        }
        logging.info(payload)
        logging.info(url)
        resp = requests.post(url=url+'/sdapi/v1/txt2img', json=payload, headers=headers)
        # pdb.set_trace()
        rjo = resp.json()
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
    sdt.prompt2img('usa')