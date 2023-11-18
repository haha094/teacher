from flask import Flask

import settings
from extension import db
# 引入蓝图
from blueprints.attendance import bp as attendance_bp
from blueprints.user import bp as user_bp

from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(settings.MySqlConfig)
db.init_app(app)
migrate = Migrate(app, db)
# 注册蓝图
app.register_blueprint(attendance_bp)
app.register_blueprint(user_bp)


@app.route('/')
def hello_world():  # put application's code here
    return "This is hahah index"


if __name__ == '__main__':
    app.run(debug=True)
