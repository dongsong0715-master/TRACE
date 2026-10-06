"""Interactive local administrator creation. No default password or public admin registration."""

from getpass import getpass

from sqlalchemy import select

from app.core.config import Settings
from app.core.database import create_database
from app.core.security import hash_password
from app.models import User
from app.schemas.auth import Credentials


def main():
    username = input("管理员用户名（3–64位字母、数字、下划线）：")
    password = getpass("密码（8–128位，不回显）：")
    if password != getpass("确认密码："):
        raise SystemExit("密码不一致，未创建。")
    credentials = Credentials(username=username, password=password)
    settings = Settings()
    engine, factory = create_database(settings)
    try:
        with factory() as db:
            if db.scalar(select(User).where(User.username == credentials.username)):
                raise SystemExit("用户名已存在，未更改原账号。")
            db.add(
                User(
                    username=credentials.username,
                    password_hash=hash_password(password),
                    role="admin",
                    is_demo=settings.data_mode == "demo",
                )
            )
            db.commit()
        print("管理员已创建。当前可登录；内容维护业务由后续模块实现。")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
