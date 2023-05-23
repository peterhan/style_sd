import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
from tornado.options import define, options
import logging

import requests
import json
import time
import pdb

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    
from _key_store import SD_API_KEY

class ModelSDText2IMG():        
    def prompt2img(self,prompt,para={}):
        url = "https://stablediffusionapi.com/api/v3/text2img"
        # prompt="handsome chinese male dressed in sport wear sitting in dinning room"
        confd={
          "key": SD_API_KEY,
          "prompt": prompt,
          "negative_prompt": None,
          "width": "512",
          "height": "512",
          "samples": "1",
          "num_inference_steps": "20",
          "seed": None,
          "guidance_scale": 7.5,
          "safety_checker": "yes",
          "multi_lingual": "no",
          "panorama": "no",
          "self_attention": "no",
          "upscale": "no",
          "embeddings_model": "embeddings_model_id",
          "webhook": None,
          "track_id": None
        }
        confd.update(para)
        payload = json.dumps(confd)
        
        headers = {
          'Content-Type': 'application/json'
        }
        resp = requests.request("POST", url, headers=headers, data=payload)
        
        jo = resp.json()
        js = json.dumps(jo,indent=2)
        logging.debug(js)
        ret_url = jo['output'][0]
        ret_eta = 0
        if 'eta' in jo:
            ret_eta = math.ceil(float(jo['eta']))       
        return ret_eta,ret_url,jo
        
if __name__ == '__main__':
    sdt  = SDText2IMG(None,None)