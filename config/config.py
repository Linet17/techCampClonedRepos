class Development():
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:0000@127.0.0.1:5432/abcDB'
    SECRET_KEY = 'c700e114ddca374f461b614b1b51a25e'
    DEBUG = True

class Production():
    SQLALCHEMY_DATABASE_URI = 'postgres://fbxdklkefsuwuj:8f6d21bece5a0d0471400746c7fb314365133002013e0f1b7a0ccf5b71e09f92@ec2-54-247-177-254.eu-west-1.compute.amazonaws.com:5432/d75nudivraa7d4'
    SECRET_KEY = 'c700e114ddca374f461b614b1b51a25e'
    DEBUG = False