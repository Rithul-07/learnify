from flask import Flask
from config import Config

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY']='hefgudgfjb wujgwf'
    
    
    from routes.auth import auth
    app.register_blueprint(auth,url_prefix='/')

    from routes.views import views
    app.register_blueprint(views,url_prefix='/')

    return app
app=create_app()
if __name__ == '__main__':
    app.run(debug=True)

