
from flask import Flask,session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
from main_config import Config,Prt
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
db=SQLAlchemy()
bootstrap=Bootstrap()
# login_manager=LoginManager()
# login_manager.login_view = "ctr.log_user_in"
# login_manager.login_message = "welcome login."

# engine=create_engine(Config.DATABASE_URI)#'mysql+pymysql://root:hard_guess@localhost:3306/testdb1?charset=utf8&autocommit=true'
# # engine=create_engine('mysql+pymysql://root:hard_guess@localhost:3306/testdb1?charset=utf8&autocommit=true')#'mysql+pymysql://root:hard_guess@localhost:3306/testdb1?charset=utf8&autocommit=true'
# DBSession=sessionmaker(bind=engine)
# dbsession=DBSession()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    Prt.prt(Config.DATABASE_URI)
    db.init_app(app)
    bootstrap.init_app(app)
    # login_manager.init_app(app)
    # session['userid'] = None
    # session['username'] = None
    # session['userpass'] = None
    # from .ctr import ctr as ctr_blueprint
    # app.register_blueprint(ctr_blueprint)
    from app.ctr import ctr
    app.register_blueprint(ctr)
    # app.register_blueprint(ctr,url_prefix='/ctr')


    return app

