
from flask import Flask
import settings
from extension import db, cors
# 引入蓝图
from blueprints.attendance import bp as attendance_bp
from blueprints.user import bp as user_bp
from blueprints.department import bp as department_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
# 初始化 SSLify，并强制使用 HTTPS

app.config.from_object(settings.MySqlConfig)
app.config.from_object(settings.JwtConfig)
app.config.from_object(settings.LoggingConfig)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
cors.init_app(app)
# 初始化日志配置
settings.LoggingConfig.init_app(app)
# 注册蓝图
app.register_blueprint(attendance_bp)
app.register_blueprint(user_bp)
app.register_blueprint(department_bp)


@app.route('/')
def hello_world():  # put application's code here
    return "This is hahah index"


if __name__ == '__main__':
    app.run(host='10.21.150.132',port=5000,debug=True)
