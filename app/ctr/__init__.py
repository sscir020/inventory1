
from flask import Blueprint

ctr=Blueprint('ctr',__name__)

from . import errors,material_routers,customerservice_routers,device_routers,record_routers,buy_rework_routers,other_routers#nform_routers,form_routers
