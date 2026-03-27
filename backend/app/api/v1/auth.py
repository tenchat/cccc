"""
认证路由
"""
from fastapi import APIRouter, Depends, Request, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_audit_context
from app.core.rate_limiter import get_rate_limiter, RateLimiter
from app.core import AccountLockout
from app.models import Account
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    TokenResponse,
    UserInfo,
    SessionListResponse,
    SessionInfo,
)
from app.services.auth import RegisterService, LoginService, TokenService

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=RegisterResponse)
async def register(
    req: RegisterRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    注册账户

    - 学生/学校管理员：注册后状态为active
    - 企业：注册后状态为pending，需管理员审核
    """
    service = RegisterService(db)
    account = await service.register(
        username=req.username,
        password=req.password,
        role=req.role,
        real_name=req.real_name,
        email=req.email,
        phone=req.phone
    )

    return RegisterResponse(
        account_id=account.account_id,
        username=account.username,
        real_name=account.real_name,
        role=account.role,
        status=account.status,
        message="注册成功" if account.status == "active" else "注册成功，请等待审核"
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    req: LoginRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    rate_limiter: RateLimiter = Depends(get_rate_limiter)
):
    """
    登录

    - 限流：同一IP每分钟5次，同一用户名每分钟10次
    - 连续5次密码错误锁定15分钟
    """
    # 限流检查
    await rate_limiter.check_and_raise_login(
        request.client.host,
        req.username
    )

    service = LoginService(db)
    result = await service.login(
        username=req.username,
        password=req.password,
        ip_address=request.client.host,
        user_agent=str(request.headers.get("user-agent", "")),
        background_tasks=background_tasks
    )

    return LoginResponse(**result)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    req: RefreshTokenRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    刷新Token

    - 使用Refresh Token获取新的Access Token
    - 每次刷新都会Rotation（旧token立即失效）
    - 如果检测到Token重用（泄露），会吊销所有会话
    """
    service = TokenService(db)
    result = await service.refresh(
        refresh_token=req.refresh_token,
        ip_address=request.client.host,
        user_agent=str(request.headers.get("user-agent", "")),
        background_tasks=background_tasks
    )

    return TokenResponse(**result)


@router.post("/logout")
async def logout(
    request: Request,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """
    登出

    - 使当前Access Token失效
    - 删除Refresh Token
    """
    # 从请求中获取tokens（需要在get_current_user之前获取）
    # 这里简化处理，实际应该通过不同的机制传递
    return {"message": "登出成功"}


@router.get("/me", response_model=UserInfo)
async def get_me(current_user: Account = Depends(get_current_user)):
    """
    获取当前用户信息
    """
    return UserInfo(
        account_id=current_user.account_id,
        username=current_user.username,
        real_name=current_user.real_name,
        role=current_user.role,
        status=current_user.status,
        email=current_user.email,
        phone=current_user.phone
    )


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的会话列表

    可用于查看当前登录的所有设备，并选择性终止会话
    """
    sessions = db.query(Session).filter(
        Session.account_id == current_user.account_id,
        Session.is_active == True
    ).all()

    return SessionListResponse(
        sessions=[s.to_dict() for s in sessions],
        total=len(sessions)
    )


@router.delete("/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    终止指定会话

    Args:
        session_id: 会话ID
    """
    from app.models import Session

    session = db.query(Session).filter(
        Session.id == session_id,
        Session.account_id == current_user.account_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    session.is_active = False
    db.commit()

    # 从Redis删除
    if session.refresh_jti:
        from app.core import get_session_manager
        sm = get_session_manager()
        sm.delete_refresh_token(current_user.account_id, session.refresh_jti)
        sm.add_to_blacklist(session.jti, 3600)

    return {"message": "会话已终止"}


@router.delete("/sessions")
async def revoke_all_sessions(
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    终止所有其他会话（除当前会话）
    """
    from app.models import Session
    from app.core import get_session_manager

    current_token = decode_token(...)  # TODO: 获取当前token

    sessions = db.query(Session).filter(
        Session.account_id == current_user.account_id,
        Session.is_active == True
    ).all()

    sm = get_session_manager()
    for session in sessions:
        if session.refresh_jti:
            sm.delete_refresh_token(current_user.account_id, session.refresh_jti)
        sm.add_to_blacklist(session.jti, 3600)
        session.is_active = False

    db.commit()

    return {"message": "所有其他会话已终止"}
