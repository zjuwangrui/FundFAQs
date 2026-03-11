# 通过 GitHub 上传并部署到服务器

## 一、本地上传到 GitHub

### 1. 在项目根目录初始化并推送到 GitHub（若尚未有仓库）

在 PowerShell 中执行（将 `你的用户名` / `你的仓库名` 换成你自己的）：

```powershell
cd D:\c_25\nsep\FundFAQs

# 若从未初始化过 Git
git init
git add .
git commit -m "Initial: FundFAQs 前后端与管理员权限"

# 在 GitHub 网页上先新建一个空仓库（不要勾选 README），然后：
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

若已有远程仓库，只需提交并推送：

```powershell
cd D:\c_25\nsep\FundFAQs
git add .
git commit -m "你的提交说明"
git push origin main
```

### 2. 确认 .gitignore 已生效

以下内容不应被提交：`backend/.venv/`、`backend/*.db`、`frontend/node_modules/`、`frontend/dist/`。当前项目根目录已有 `.gitignore`，无需再改。

---

## 二、在服务器上从 GitHub 拉取并运行

假设服务器系统为 **Linux**（如 Ubuntu），且已安装 `git`、`Python 3`、`Node.js`、`npm`。

### 1. 克隆仓库

```bash
cd /opt   # 或你希望放置的目录
git clone https://github.com/你的用户名/你的仓库名.git FundFAQs
cd FundFAQs
```

### 2. 后端（Flask + Gunicorn）

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows 服务器用: .venv\Scripts\activate

pip install -r requirements.txt

# 设置管理密钥（必改，且不要提交到 Git）
export FUNDFAQ_ADMIN_SECRET="你的强密码"
export FLASK_ENV=production

# 前台试跑（确认无报错后再用下面 gunicorn）
# python app.py

# 生产运行（推荐）
gunicorn -w 4 -b 127.0.0.1:5000 "app:app"
```

保持该终端运行，或使用 systemd/supervisor 托管 gunicorn（见下文可选部分）。

### 3. 前端构建并放置静态文件

在**另一终端**或本机执行：

```bash
cd /opt/FundFAQs/frontend
npm install
npm run build
```

会生成 `frontend/dist/`。部署时由 Nginx（或其它 Web 服务器）提供该目录下的静态文件，并把 `/api` 反向代理到 `http://127.0.0.1:5000`。

### 4. Nginx 配置示例（同一台服务器提供前端 + 反向代理 API）

在 `/etc/nginx/sites-available/fundfaqs`（或你的站点配置里）加入：

```nginx
server {
    listen 80;
    server_name 你的域名或服务器IP;

    root /opt/FundFAQs/frontend/dist;
    index index.html;
    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用并重载 Nginx：

```bash
sudo ln -sf /etc/nginx/sites-available/fundfaqs /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 5. 环境变量持久化（可选）

在服务器上建议用 systemd 或 supervisor 跑 gunicorn，并把 `FUNDFAQ_ADMIN_SECRET` 写在环境里（不要写进代码）。例如 systemd 服务文件 `/etc/systemd/system/fundfaqs.service`：

```ini
[Unit]
Description=FundFAQs Flask Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/FundFAQs/backend
Environment="FUNDFAQ_ADMIN_SECRET=你的强密码"
Environment="FLASK_ENV=production"
ExecStart=/opt/FundFAQs/backend/.venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app:app"
Restart=always

[Install]
WantedBy=multi-user.target
```

然后：

```bash
sudo systemctl daemon-reload
sudo systemctl enable fundfaqs
sudo systemctl start fundfaqs
```

---

## 三、之后更新代码（从 GitHub 拉取后重新部署）

```bash
cd /opt/FundFAQs
git pull origin main

# 后端：重启 gunicorn（若用 systemd）
sudo systemctl restart fundfaqs

# 前端：重新构建并无需改 Nginx，只要 root 仍指向 dist
cd frontend && npm install && npm run build
```

按以上步骤即可完成：**本地上传到 GitHub → 服务器从 GitHub 拉取 → 后端用 gunicorn + 前端 dist + Nginx 提供页面并代理 /api**。
