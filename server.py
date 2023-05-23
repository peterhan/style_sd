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
        uhtml='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload</title>
</head>
<body>
    <h1>Upload</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" id="file" />
        <input type="submit" value="upload" />
    </form>%s
</body>
</html>
        '''%html
        self.write(uhtml)
    
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
            ret_d = {'status':'error', 'info':traceback.format_exc()}
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
        


# CONST
MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB
MAX_STREAMED_SIZE = 16*GB

# Class&Function Defination
@tornado.web.stream_request_body
class UploadHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.bytes_read = 0
        self.meta = dict()
        self.receiver = self.get_receiver()

    # def prepare(self):
    """If no stream_request_body"""
    #     self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)

    def data_received(self, chunk):
        self.receiver(chunk)

    def get_receiver(self):
        self.index = 0
        SEPARATE = b'\r\n'

        def receiver(chunk):
            if self.index == 0:
                self.index +=1
                split_chunk             = chunk.split(SEPARATE)
                self.meta['boundary']   = SEPARATE + split_chunk[0] + b'--' + SEPARATE
                self.meta['header']     = SEPARATE.join(split_chunk[0:3])
                self.meta['header']     += SEPARATE *2
                self.meta['filename']   = split_chunk[1].split(b'=')[-1].replace(b'"',b'').decode()

                chunk = chunk[len(self.meta['header']):] # Stream掐头
                import os
                self.fp = open(os.path.join('upload',self.meta['filename']), "wb")
                self.fp.write(chunk)
            else:
                self.fp.write(chunk)
        return receiver

    def post(self, *args, **kwargs):
        # Stream去尾
        self.meta['content_length'] = int(self.request.headers.get('Content-Length')) - \
                                      len(self.meta['header']) - \
                                      len(self.meta['boundary'])

        self.fp.seek(self.meta['content_length'], 0)
        self.fp.truncate()
        self.fp.close()
        self.finish('OK')
        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/style_sd/text2img", SDText2IMG),
            (r"/style_sd/macro_facial_analysis", FacialEstimater),
            (r"/upload", UploadHandler),
        ]
        ,debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()