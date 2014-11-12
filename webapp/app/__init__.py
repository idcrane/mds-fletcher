from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
from app import views
from app import textscrape
from app import blogclassify

# if not app.debug:
#     import logging
#     from logging.handlers import RotatingFileHandler
#     file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 5 * 1024 * 1024, 10)
#     file_handler.setFormatter(logging.Formatter(i'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     app.logger.setLevel(logging.INFO)
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
    # app.logger.info('fletcher startup')
