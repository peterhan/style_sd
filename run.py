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

from model.sdtext2img import ModelSDText2IMG


if 'prod' in sys.argv:
    print('Production Mode')    
    define("port", default=8899, help="run on the given port", type=int)
else:
    print('Test Mode')    
    define("port", default=8898, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        lst = ['/style_sd/text2img?prompt=asia']
        html = []
        for itm in lst:
            html .append("<a href='{0}'>{0}</a>".format(itm))
        html = '<br/>'.join(html)
        self.write(html)

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
    
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/style_sd/text2img", SDText2IMG),
        ]
        ,debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()