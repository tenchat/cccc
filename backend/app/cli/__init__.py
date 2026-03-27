"""
CLI工具
"""
import click
from datetime import datetime

from app.core.database import SessionLocal, engine, Base
from app.core.password import hash_password, verify_password
from app.models import Account, Role, Company, ROLE_CODES
from app.core.lockout import force_unlock


def create_admin(username: str, real_name: str, password: str = "Admin123!"):
    """创建管理员账户"""
    db = SessionLocal()
    try:
        # 生成account_id
        account_id = f"ADM{datetime.now().strftime('%H%M%S')}"

        # 创建账户
        account = Account(
            account_id=account_id,
            username=username,
            password_hash=hash_password(password),
            real_name=real_name,
            status="active"
        )

        # 获取admin角色
        role = db.query(Role).filter(Role.role_code == "admin").first()
        if not role:
            click.echo("错误: admin角色不存在")
            return

        account.roles.append(role)
        db.add(account)
        db.commit()

        click.echo(f"管理员创建成功!")
        click.echo(f"  账户ID: {account_id}")
        click.echo(f"  用户名: {username}")
        click.echo(f"  临时密码: {password}")
        click.echo(f"请立即修改密码!")

    finally:
        db.close()


def unlock_account(account_id: str):
    """解锁账号"""
    force_unlock(account_id)
    click.echo(f"账号已解锁: {account_id}")


def verify_company(company_id: str, action: str):
    """审核企业"""
    db = SessionLocal()
    try:
        company = db.query(Company).filter(
            Company.company_id == company_id
        ).first()

        if not company:
            click.echo(f"错误: 企业不存在 {company_id}")
            return

        if action == "approve":
            company.verified = True
            company.verified_at = datetime.utcnow()
            db.commit()
            click.echo(f"企业已审核通过: {company.company_name}")
        elif action == "reject":
            company.verified = False
            company.verified_at = datetime.utcnow()
            db.commit()
            click.echo(f"企业已拒绝: {company.company_name}")

    finally:
        db.close()


@click.group()
def cli():
    """就业信息平台CLI工具"""
    pass


@cli.command()
def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)
    click.echo("数据库表初始化完成")


@cli.command()
def create_roles():
    """创建默认角色"""
    db = SessionLocal()
    try:
        roles = [
            ("student", "学生", "学生用户"),
            ("school_admin", "学校管理员", "学校就业指导中心"),
            ("company_admin", "企业管理员", "用人单位管理员"),
            ("admin", "系统管理员", "系统管理最高权限"),
        ]

        for code, name, desc in roles:
            existing = db.query(Role).filter(Role.role_code == code).first()
            if not existing:
                role = Role(role_code=code, role_name=name, description=desc)
                db.add(role)
                click.echo(f"创建角色: {name}")

        db.commit()
        click.echo("角色创建完成")

    finally:
        db.close()


@cli.command()
@click.option('--username', required=True, help='用户名')
@click.option('--name', required=True, help='姓名')
@click.option('--password', default='Admin123!', help='密码')
def admin(username, name, password):
    """创建管理员账户"""
    create_admin(username, name, password)


@cli.command()
@click.option('--account-id', required=True, help='账户ID')
def unlock(account_id):
    """解锁账号"""
    unlock_account(account_id)


@cli.command()
@click.option('--company-id', required=True, help='企业ID')
@click.option('--action', required=True, type=click.Choice(['approve', 'reject']), help='操作')
def verify_company_cmd(company_id, action):
    """审核企业"""
    verify_company(company_id, action)


@cli.command()
def list_companies():
    """列出待审核企业"""
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.verified == False).all()
        if not companies:
            click.echo("没有待审核的企业")
            return

        click.echo(f"待审核企业 ({len(companies)}):")
        for c in companies:
            click.echo(f"  {c.company_id}: {c.company_name}")

    finally:
        db.close()


if __name__ == '__main__':
    cli()
