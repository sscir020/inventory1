from app import create_app
app=create_app('development')#development
if __name__=='__main__':
    # app=create_app('testing')
    app.run(port=6004 ,debug=True)