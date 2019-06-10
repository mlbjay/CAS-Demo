# encoding: utf-8
# venv的激活环境：/Users/jayli/venv/xxx/bin/activate

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
# 导入后，即可产生映射
from models import User, TGT


manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

