"""Blueprint for system configuration endpoints."""

import os
from flask import Blueprint, request

from config import active_config
from utils import error_response

system_bp = Blueprint("system", __name__)

def _require_admin_secret(data: dict):
    """Validate admin secret for protected operations."""
    secret = str(data.get("secret", "")).strip()
    if not secret:
        return error_response("缺少管理密钥", 403)
    if secret != active_config.ADMIN_SECRET:
        return error_response("管理密钥不正确", 403)
    return None

@system_bp.route("/email-config", methods=["POST"])
def update_email_config():
    data = request.get_json(silent=True) or {}

    # 1. 验证管理员权限
    err = _require_admin_secret(data)
    if err is not None:
        return err
    
    # 2. 获取并验证参数
    email = str(data.get("email", "")).strip()
    auth_code = str(data.get("auth_code", "")).strip()
    
    if not email:
        return error_response("邮箱地址不能为空")
    if not auth_code:
        return error_response("授权码不能为空")
        
    # 3. 严格设置 SMTP 服务器，并对不支持的邮箱报错
    smtp_server = ""
    smtp_port = 465
    is_tls = False
    
    # 强制校验邮箱后缀，避免 163/QQ 混用等低级错误
    if email.endswith("@qq.com"):
        smtp_server = "smtp.qq.com"
        smtp_port = 465
        is_tls = False
    elif email.endswith("@163.com"):
        smtp_server = "smtp.163.com"
        smtp_port = 465
        is_tls = False
    elif email.endswith("@gmail.com"):
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        is_tls = True
    else:
        # 如果不是常见邮箱，为了避免配置混乱，我们暂时不支持自动推断
        # 或者可以要求前端传递 smtp_server 等参数
        return error_response(f"目前自动配置不支持 {email.split('@')[-1]} 类型的邮箱，请使用 QQ 或 163 邮箱。", 400)

    # 4. 更新运行时配置并持久化写入 config.py
    # 注意：这里我们只更新 发件人 配置，
    # 并且把这个新发件人，重置为唯一的首选发件箱
    active_config.MAIL_SERVER = smtp_server
    active_config.MAIL_PORT = smtp_port
    active_config.MAIL_USE_TLS = is_tls

    active_config.MAIL_USERNAME = email
    active_config.MAIL_PASSWORD = auth_code
    active_config.MAIL_DEFAULT_SENDER = f"FundFAQs <{email}>"
    
    # ------------------------------------------------------------------
    # 核心修改：真正的追加模式（不清除）
    # ------------------------------------------------------------------
    current_emails_str = getattr(active_config, 'ADMIN_EMAILS', '')
    if current_emails_str:
        # 拆分并去重，保留原有列表
        email_set = set([e.strip() for e in current_emails_str.split(',') if e.strip()])
    else:
        email_set = set()
    
    email_set.add(email) # 将新邮箱加入集合
    new_emails_str = ",".join(email_set)
    
    # 更新运行时配置中的收件人列表
    active_config.ADMIN_EMAILS = new_emails_str
    active_config.ADMIN_EMAIL = new_emails_str

    # 读取原始 config.py 内容
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.py")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # 替换对应的配置项
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("MAIL_SERVER:"):
                new_lines.append(f'    MAIL_SERVER: str = "{smtp_server}"\n')
            elif stripped.startswith("MAIL_PORT:"):
                new_lines.append(f'    MAIL_PORT: int = {smtp_port}\n')
            elif stripped.startswith("MAIL_USE_TLS:"):
                tls_val = "True" if is_tls else "False"
                new_lines.append(f'    MAIL_USE_TLS: bool = {tls_val}\n')
            elif stripped.startswith("MAIL_USERNAME:"):
                new_lines.append(f'    MAIL_USERNAME: str = "{email}"\n')
            elif stripped.startswith("MAIL_PASSWORD:"):
                new_lines.append(f'    MAIL_PASSWORD: str = "{auth_code}"\n')
            elif stripped.startswith("MAIL_DEFAULT_SENDER:"):
                new_lines.append(f'    MAIL_DEFAULT_SENDER: str = "FundFAQs <{email}>"\n')
            # 关键：写入合并后的新（长）列表
            elif stripped.startswith("ADMIN_EMAILS:"):
                new_lines.append(f'    ADMIN_EMAILS: str = "{new_emails_str}"\n')
            elif stripped.startswith("ADMIN_EMAIL:"):
                new_lines.append(f'    ADMIN_EMAIL: str = "{new_emails_str}"\n')
            else:
                new_lines.append(line)
        
        with open(config_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    except Exception as e:
        print(f"Failed to persist config: {e}")
        # 不阻断流程，仅打印错误，因为运行时配置已经更新了

    # 5. 尝试发送一封测试邮件验证配置
    from mailer import send_notification
    try:
        send_notification(
            subject="【FundFAQs】新管理员加入通知", 
            body=f"已成功添加新管理员邮箱：{email}。\n\n当前所有接收通知的管理员列表：\n{new_emails_str}"
        )


    except Exception as e:
        return error_response(f"配置保存成功，但发送测试邮件失败: {str(e)}")

    return {"message": "邮箱配置更新成功，测试邮件已发送"}
