#coding:utf-8
from flask import Blueprint

ctr=Blueprint('ctr',__name__)

from . import errors,nform_routers,form_routers
