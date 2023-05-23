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
    
from _key_store import MT_APPID ,MT_APPKEY ,MT_SECRETID

class ModelMeiTuAPI():