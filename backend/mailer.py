import smtplib
import threading
from email.mime.text import MIMEText
from email.header import Header
from config import active_config


def send_notification(subject: str, body: str):
    """Start a thread to send an email notification."""
    # check if server configured
    if not active_config.MAIL_SERVER:
        print("Mail notification skipped: MAIL_SERVER not configured.")
        return

    # Use a thread to avoid blocking the HTTP response
    t = threading.Thread(target=_send_sync, args=(subject, body))
    t.start()



def _send_sync(subject: str, body: str):
    """Internal function to send email via SMTP."""
    sender = active_config.MAIL_DEFAULT_SENDER or active_config.MAIL_USERNAME
    
    # 兼容旧配置: ADMIN_EMAIL 单个邮箱 vs ADMIN_EMAILS 复数列表
    recipients_str = getattr(active_config, 'ADMIN_EMAILS', '') or getattr(active_config, 'ADMIN_EMAIL', '')
    
    if not recipients_str:
        print("[Mailer] No recipients configured.")
        return

    # 按逗号分割并去重
    recipient_list = [email.strip() for email in recipients_str.split(',') if email.strip()]

    if not recipient_list:
        return

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    # To 字段通常只写第一个收件人或群组名，防止隐私泄露或太长，
    # 但为了简单起见，这里显示所有收件人
    msg['To'] = ", ".join(recipient_list)

    try:
        if active_config.MAIL_USE_TLS:
            # 587 or other TLS ports
            server = smtplib.SMTP(active_config.MAIL_SERVER, active_config.MAIL_PORT)
            server.starttls()
        else:
            # 465 (SSL) or 25 (unencrypted)
            if active_config.MAIL_PORT == 465:
                server = smtplib.SMTP_SSL(active_config.MAIL_SERVER, active_config.MAIL_PORT)
            else:
                server = smtplib.SMTP(active_config.MAIL_SERVER, active_config.MAIL_PORT)

        if active_config.MAIL_USERNAME and active_config.MAIL_PASSWORD:
            server.login(active_config.MAIL_USERNAME, active_config.MAIL_PASSWORD)

        # SMTP sendmail accepts a list for recipients
        server.sendmail(sender, recipient_list, msg.as_string())
        server.quit()
        print(f"[Mailer] Notification sent to {len(recipient_list)} recipients: {recipient_list}")

    except Exception as e:
        print(f"[Mailer] Failed to send email: {e}")
