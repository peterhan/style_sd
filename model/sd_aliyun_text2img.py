#!coding:utf8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
from tornado.options import define, options
import logging

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
        confd= {
         "denoising_strength": 0,
         "prompt": "puppy dogs", #提示词
         "negative_prompt": "", #反向提示词
         "seed": -1, #种子，随机数
         "batch_size": 2, #每次张数
         "n_iter": 1, #生成批次
         "steps": 50, #生成步数
         "cfg_scale": 7, #关键词相关性
         "width": 512, #宽度
         "height": 512, #高度
         "restore_faces": False, #脸部修复
         "tiling": False, #可平埔
         "override_settings": {
             "sd_model_checkpoint" :"wlop-any.ckpt [7331f3bc87]"
          }, # 一般用于修改本次的生成图片的stable diffusion 模型，用法需保持一致
           "script_args": [
              0,
              True,
              True,
              "LoRA",
              "dingzhenlora_v1(fa7c1732cc95)",
              1,
              1
          ], # 一般用于lora模型或其他插件参数，如示例，我放入了一个lora模型， 1，1为两个权重值，一般只用到前面的权重值1
         "sampler_index": "Euler" #采样方法
        }
        confd.update(para)
        payload = confd
        
        token = AL_TOKEN
        encoded_token = base64.b64encode(token.encode("utf-8")).decode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": 'Basic %s'%encoded_token
        }
        resp = requests.post(url=url+'/sdapi/v1/txt2img', json=payload, headers=headers)
        pdb.set_trace()
        rjo = resp.json()
        for i in rjo['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
            png_payload = {
                "image": "data:image/png;base64," + i
            }
            resp2 = requests.post(url=url+'/sdapi/v1/png-info', json=png_payload, headers=headers)
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", resp2.json().get("info"))
            image.save('output.png', pnginfo=pnginfo)
   


if __name__ == '__main__':
    sdt  = ModelSDText2IMG()
    logging.getLogger().setLevel(logging.DEBUG)
    sdt.prompt2img('usa')