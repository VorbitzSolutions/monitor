import os
from configparser import ConfigParser

def configuration():
    config = ConfigParser()
    path = os.path.abspath(os.path.dirname(__file__)) + "/" + 'config.env'
    config.read(path)
    db_name = config["DEFAULT"]["database"]
    db_user = config["DEFAULT"]["db_user"]
    looptime = int(config["DEFAULT"]["looptime"])
    appid = config["DEFAULT"]["appid"]
    sendmsgid = config["DEFAULT"]["sendmsgid"]

    return db_name,db_user,looptime,appid,sendmsgid