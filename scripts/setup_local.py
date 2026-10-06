"""Create local config without overwriting existing files. Standard-library only."""

import argparse
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description="TRACE local configuration")
    parser.add_argument("--database", choices=["sqlite", "mysql"], default="sqlite")
    args = parser.parse_args()
    backend_env = ROOT / "backend" / ".env"
    root_env = ROOT / ".env"
    if backend_env.exists() or (args.database == "mysql" and root_env.exists()):
        parser.error("配置已存在，未覆盖。请手动编辑 .env，切换数据库后执行迁移。")
    secret = secrets.token_urlsafe(48)
    if args.database == "mysql":
        password = secrets.token_urlsafe(24)
        root_password = secrets.token_urlsafe(24)
        root_env.write_text(
            f"MYSQL_DATABASE=trace\nMYSQL_USER=trace_app\nMYSQL_PASSWORD={password}\n"
            f"MYSQL_ROOT_PASSWORD={root_password}\nMYSQL_PORT=3307\n",
            encoding="utf-8",
        )
        database_url = f"mysql+pymysql://trace_app:{password}@127.0.0.1:3307/trace"
    else:
        database_url = f"sqlite:///{(ROOT / 'backend' / 'trace.db').as_posix()}"
    backend_env.write_text(
        f"APP_ENV=development\nDATABASE_URL={database_url}\nJWT_SECRET={secret}\n"
        "PUBLIC_ORIGIN=http://localhost:5173\nACCESS_TOKEN_MINUTES=120\n"
        "COOKIE_SECURE=false\nDATA_MODE=demo\nAI_MODE=live\n"
        "LLM_BASE_URL=\nLLM_MODEL=\nLLM_API_KEY=\n",
        encoding="utf-8",
    )
    print("已创建本地配置。请在 backend 中执行 python -m alembic upgrade head。")
    print("启动后通过页面注册学生账号。配置、密码与本地数据库已列入 .gitignore。")


if __name__ == "__main__":
    main()
