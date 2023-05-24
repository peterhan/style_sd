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
    def prompt2img(self,prompt,para={}):
        url = AL_URL        
        # prompt="handsome chinese male dressed in sport wear sitting in dinning room"
        confd= {"prompt": prompt, "all_prompts": [prompt], "negative_prompt": "", "all_negative_prompts": [""], "seed": 2852570473, "all_seeds": [2852570473], "subseed": 3611650335, "all_subseeds": [3611650335], "subseed_strength": 0, "width": 512, "height": 512, "sampler_name": "Euler a", "cfg_scale": 7, "steps": 20, "batch_size": 1, "restore_faces": False, "face_restoration_model": None, "sd_model_hash": "6ce0161689", "seed_resize_from_w": 0, "seed_resize_from_h": 0, "denoising_strength": None, "extra_generation_params": {}, "index_of_first_image": 0, "infotexts": ["puppy dog\\nSteps: 20, Sampler: Euler a, CFG scale: 7, Seed: 2852570473, Size: 512x512, Model hash: 6ce0161689, Model: v1-5-pruned-emaonly"], "styles": [], "job_timestamp": "20230524061323", "clip_skip": 1, "is_using_inpainting_conditioning": False}
        confd.update(para)
        payload = json.dumps(confd)
        
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