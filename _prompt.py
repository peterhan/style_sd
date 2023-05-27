PROMPT={}

COMMON_NEG='(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck'
COMMON_para='Steps: 30, Sampler: Euler a, CFG scale: 7, Seed: 2774517884, Size: 512x728, Model hash: f68b37e71f, Model: Taiyi-Stable-Diffusion-1B-Chinese-v0.1   ,Face restoration: CodeFormer'
PROMPT['male_suit']='''
    1man, 25 years- old, full body, wearing long-sleeve white shirt and tie, muscular rand black suit, glasses,standing, soft lighting, masterpiece, best quality, 8k uhd, dslr, film grain, Fujifilm XT3 photorealistic painting art by midjourney and greg rutkowski <lora:asianmale_v10:0.6> <lora:uncutPenisLora_v10:0.6>,face    
    '''
PROMPT['female_suit']='''
    1 female, 25 years- old, full body, wearing long-sleeve white shirt and tie,  standing, soft lighting, masterpiece, best quality, 8k uhd, dslr, film grain, Fujifilm XT3 photorealistic painting art by midjourney and greg rutkowski <lora:asianmale_v10:0.6> <lora:uncutPenisLora_v10:0.6>,face   
    '''

def ui_str_to_payload(ui_str):
    payload={}
    col_name = ['prompt','negative_prompt','misc']
    payload['negative_prompt']=COMMON_NEG
    for i,l in enumerate(ui_str.strip().splitlines()):
        if l.strip()=='':
            continue
        i+=1
        print i,l
        if i>3:
            break
        if i==3:
            for item in l.strip().split(','):
                try:
                    k,v = item.split(':')
                except:
                    print item
                payload[k.strip().replace(' ','_')] = v.strip()
        elif i==1:
            payload['prompt']=l
        elif i==2:
            payload['negative_prompt'] += ' '+l.replace('Negative prompt: ','')
    override_settings = {}
    override_settings["filter_nsfw"] = True
    override_settings["CLIP_stop_at_last_layers"] = 2

    override_payload = {
                    "override_settings": override_settings
                }
    # payload.update(override_payload)
    return payload
        
import json
for k,v in PROMPT.items():
    PROMPT[k]=ui_str_to_payload(v)
    print k,json.dumps(PROMPT[k],indent=2)
