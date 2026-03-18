# FundFAQs 资助政策答疑平台

基于 **Vue 3 + Vite + TypeScript**（前端）与 **Python Flask + SQLite**（后端）的资助政策答疑网站，支持文章发布、浏览、搜索与评论功能。

## 功能特性

- 📄 **文章管理**：发布、编辑、浏览文章，完整 Markdown 格式支持
- 🔍 **全文搜索**：按标题和内容实时搜索文章
- 💬 **评论系统**：无需注册，任何人均可评论，按时间倒序分页展示
- 📱 **响应式设计**：适配桌面与移动端
- ✏️ **Markdown 编辑器**：内置 md-editor-v3，支持实时分屏预览、工具栏操作
- 📧 **邮件通知**：集成 SMTP 服务，新评论或新管理员加入时自动通知所有管理员（多收件人同步）
- ⚙️ **动态配置**：通过后台界面管理发件服务和追加接收邮箱，配置自动持久化

## 项目结构

```
FundFAQs/
├── backend/
│   ├── app.py              # Flask 主应用（路由 + REST API）
│   ├── fund_faqs.db        # SQLite 数据库（自动生成）
│   └── requirements.txt    # Python 依赖
└── frontend/
    ├── index.html          # Vite 入口 HTML
    ├── vite.config.ts      # Vite 配置（含 /api 反向代理）
    ├── tsconfig.json       # TypeScript 配置
    ├── package.json        # 前端依赖
    └── src/
        ├── main.ts         # 应用入口
        ├── App.vue         # 根组件（Header / Footer）
        ├── api/
        │   └── index.ts    # Axios 封装的 API 模块
        ├── types/
        │   └── index.ts    # TypeScript 类型定义
        ├── router/
        │   └── index.ts    # Vue Router 路由配置
        ├── assets/
        │   └── main.css    # 全局样式
        └── views/
            ├── HomeView.vue          # 首页（文章列表 + 搜索）
            ├── ArticleDetailView.vue # 文章详情页（Markdown 渲染 + 评论）
            └── EditArticleView.vue   # 文章编辑 / 发布页
```

## 快速启动

### 1. 启动后端

```bash
cd backend

# 创建并激活虚拟环境（Windows）
python -m venv .venv
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动 Flask（默认 http://localhost:5000）
python app.py
```

### 2. 启动前端

```bash
cd frontend

# 安装依赖（首次）
npm install

# 启动开发服务器（默认 http://localhost:5173）
npm run dev
```

> 前端开发服务器已通过 `vite.config.ts` 将 `/api` 请求代理到后端 `http://localhost:5000`，无需额外跨域配置。

### 3. 生产构建

```bash
cd frontend
npm run build   # 产物输出至 frontend/dist/
```

将 `dist/` 部署到静态服务器，并将后端以生产模式运行即可。

## 邮件配置说明

1.  **动态添加管理员**：在首页点击「⚙ 邮箱配置」，输入管理员密钥 `zizhumail` 和新邮箱信息。
2.  **多收件人机制**：每次配置会**追加**新邮箱到管理员列表，所有在列的管理员都会同时收到评论通知。
3.  **支持服务**：建议使用 QQ 或 163 邮箱（需开启 SMTP 服务并使用授权码）。

## API 接口详情

| 方法 | 路径 | 权限要求 | 说明 |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/articles` | 公开 | 获取文章列表（`page` / `per_page` 分页） |
| `GET` | `/api/articles/search` | 公开 | 全文搜索（`q` / `page` / `per_page`） |
| `GET` | `/api/articles/<id>` | 公开 | 获取单篇文章详情 |
| `POST` | `/api/articles` | 公开 | 发布新文章 |
| `PUT` | `/api/articles/<id>` | **管理员** | 更新文章（需 `secret`） |
| `GET` | `/api/articles/<id>/comments` | 公开 | 获取评论列表（分页） |
| `POST` | `/api/articles/<id>/comments` | 公开 | 发表评论（**触发邮件通知**） |
| `POST` | `/api/system/email-config` | **管理员** | 配置发件箱并**追加**管理员接收邮箱（需 `secret`） |

## 技术栈

| 层 | 技术 |
|----|------|
| 前端框架 | Vue 3（Composition API + `<script setup>`） |
| 构建工具 | Vite 5 |
| 类型系统 | TypeScript 5 |
| 路由 | Vue Router 4 |
| HTTP 请求 | Axios |
| Markdown 编辑 | md-editor-v3 |
| Markdown 渲染 | marked + DOMPurify（防 XSS） |
| 后端框架 | Python Flask 3 |
| 数据库 | SQLite（内置，零配置） |
| 跨域 | Flask-CORS |
