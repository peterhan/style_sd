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
import shutil

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    
from _key_store import SD_API_KEY
from _prompt import PROMPT
import webbrowser

class ModelSDText2IMG(object):
    def prompt2img(self,para={}):
        url = "https://stablediffusionapi.com/api/v3/text2img"
        # prompt="handsome chinese male dressed in sport wear sitting in dinning room"
        confd={
          "key": SD_API_KEY,
          "prompt": None,
          "negative_prompt": None,
          "width": "512",
          "height": "784",
          "samples": "1",
          "num_inference_steps": "20",
          "seed": None,
          "guidance_scale": 7.5,
          "safety_checker": "yes",
          "multi_lingual": "no",
          "panorama": "no",
          "self_attention": "no",
          "upscale": "no",
          "embeddings_model": "deliberate-v2",
          "webhook": None,
          "track_id": None
        }
        if 'style' in para:
            k=para['style']
            logging.info('style :%s',k)
            if k not in PROMPT:
                raise Exception('style not define in _prompt.py')
            sconfd=PROMPT.get(k,{})
            logging.info('confd :%s',sconfd)
            confd.update(sconfd)
        
        confd.update(para)
        payload = json.dumps(confd)
        
        headers = {
          'Content-Type': 'application/json'
        }
        resp = requests.request("POST", url, headers=headers, data=payload)
        
        jo = resp.json()
        js = json.dumps(jo,indent=2)
        logging.debug(js)
        ret_eta = 0
        ret_url = None
        if jo.get('status')=='error':
            raise Exception(jo['message'])
        if 'output' in jo:
            ret_url = jo['output'][0]
        if 'eta' in jo:
            ret_eta = math.ceil(float(jo['eta']))
            
        resp = requests.get(ret_url,stream=True)
        fpath = './images/%s'%(ret_url.split('/')[-1])
        if resp.status_code == 200:
            with open(fpath, 'wb') as f:
                for chunk in resp:
                    f.write(chunk)
        
        ret= {'eta':ret_eta,'url':ret_url,'local_url':fpath.strip('.')}
        webbrowser.open(ret_url)
        return ret
        
if __name__ == '__main__':
    sdt  = ModelSDText2IMG()
    logging.getLogger().setLevel(logging.DEBUG)
    ret = sdt.prompt2img({'style':'female_suit'})
    # pdb.set_trace()