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
    
from _key_store import SD_API_KEY

class ModelSDText2IMG(object):
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
        ret_eta = 0
        ret_url = None
        if jo.get('status')=='error':
            raise Exception(jo['message'])
        if 'output' in jo:
            ret_url = jo['output'][0]
        if 'eta' in jo:
            ret_eta = math.ceil(float(jo['eta']))       
        return ret_eta,ret_url,jo
   

import requests
import io
import base64
from PIL import Image, PngImagePlugin

if __name__ == '__main__':
    url = "http://8.146.200.119:8080"
    payload = {"prompt": "puppy dog", "all_prompts": ["puppy dog"], "negative_prompt": "", "all_negative_prompts": [""], "seed": 2852570473, "all_seeds": [2852570473], "subseed": 3611650335, "all_subseeds": [3611650335], "subseed_strength": 0, "width": 512, "height": 512, "sampler_name": "Euler a", "cfg_scale": 7, "steps": 20, "batch_size": 1, "restore_faces": False, "face_restoration_model": None, "sd_model_hash": "6ce0161689", "seed_resize_from_w": 0, "seed_resize_from_h": 0, "denoising_strength": None, "extra_generation_params": {}, "index_of_first_image": 0, "infotexts": ["puppy dog\\nSteps: 20, Sampler: Euler a, CFG scale: 7, Seed: 2852570473, Size: 512x512, Model hash: 6ce0161689, Model: v1-5-pruned-emaonly"], "styles": [], "job_timestamp": "20230524061323", "clip_skip": 1, "is_using_inpainting_conditioning": False}
    token = "admin:kQMGbwDi9lpiBgLgElll"
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