import pymysql

class DBConnection(object):
    host = "bxwuncwod1yxvwwned5s-mysql.services.clever-cloud.com"
    DB = "bxwuncwod1yxvwwned5s"
    userDB = "ujo5pftfpvqiwoqw"
    passDB = "OTNfrdZFDJEVuHqeGajm"
    
    instance = None

    def __new__(cls,*args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args,**kargs)
        return cls.instance

    def __init__(self):        
        self.conexion = pymysql.connect(host=self.host, user=self.userDB, passwd=self.passDB, db=self.DB)
