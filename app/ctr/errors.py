#coding:utf-8
from . import ctr
from ..__init__ import dbsession

@ctr.app_errorhandler(404)
def page_not_found(e):
    dbsession.close()
    dbsession.rollback()
    return "not found 404"

@ctr.app_errorhandler(500)
def internal_error(e):
    dbsession.close()
    dbsession.rollback()
    return "internal 500"
