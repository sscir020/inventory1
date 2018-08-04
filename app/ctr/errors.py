
from . import ctr
from ..__init__ import db#session

@ctr.app_errorhandler(404)
def page_not_found(e):
    db.session.close()
    db.session.rollback()
    return "not found 404"

@ctr.app_errorhandler(500)
def internal_error(e):
    db.session.close()
    db.session.rollback()
    return "internal 500"
