#!coding:utf8
from datetime import datetime,timedelta
import time
from multiprocessing.pool import ThreadPool
import logging
import traceback
import json
import sys
import requests

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
from tornado.options import define, options

from model.meitu_api import ModelMeiTuAPI
from model.sd_text2img import ModelSDText2IMG


if 'prod' in sys.argv:
    print('Production Mode')    
    define("port", default=8899, help="run on the given port", type=int)
else:
    print('Test Mode')    
    define("port", default=8898, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        lst = [
            '/style_sd/text2img?prompt=asia'
            ,'/style_sd/macro_facial_analysis'
        ]
        html = []
        for itm in lst:
            html .append("<a href='{0}'>{0}</a>".format(itm))
        html = '<br/>'.join(html)
        self.write(html)
    
class FacialEstimater(tornado.web.RequestHandler):
    def get(self):
        pass
    
    def post(self,action):
        mmta = ModelMeiTuAPI()
        jo = tornado.escape.json_decode(self.request.body)
        resp = mmta.macro_facial_analysis(para = jo)
        self.write(resp)    
    
class SDText2IMG(tornado.web.RequestHandler):
    def get(self):
        msdt = ModelSDText2IMG()
        prompt = self.get_argument('prompt').replace(',',' ')
        try:
            ret_eta, ret_url, jo = msdt.prompt2img(prompt)
            ret_d = {'status':'ok', 'data':{'eta':ret_eta, 'url':ret_url}}
        except:
            ret_d = {'status':'error', traceback.format_exc()}
        self.write(json.dumps(ret_d))
    
    def post(self,action):
        jo = tornado.escape.json_decode(self.request.body)
        self.write('' + action)  
   
class MeiTuAPI(tornado.web.RequestHandler):
    def get(self):
        self.write('')
    
    def post(self,action):
        mmta = ModelMeiTuAPI()
        jo = tornado.escape.json_decode(self.request.body)
        resp = mmta.macro_facial_analysis(para = jo)
        self.write(resp)
        
        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/style_sd/text2img", SDText2IMG),
            (r"/style_sd/macro_facial_analysis", FacialEstimater),
        ]
        ,debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()