from app import create_app,db
from app.models import *

app=create_app('development2')
app.app_context().push()
with  app.app_context():
    print("************")
    db.create_all()