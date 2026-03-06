# FundFAQs 资助政策答疑平台

基于 **Vue 3 + Vite + TypeScript**（前端）与 **Python Flask + SQLite**（后端）的资助政策答疑网站，支持文章发布、浏览、搜索与评论功能。

## 功能特性

- 📄 **文章管理**：发布、编辑、浏览文章，完整 Markdown 格式支持
- 🔍 **全文搜索**：按标题和内容实时搜索文章
- 💬 **评论系统**：无需注册，任何人均可评论，按时间倒序分页展示
- 📱 **响应式设计**：适配桌面与移动端
- ✏️ **Markdown 编辑器**：内置 md-editor-v3，支持实时分屏预览、工具栏操作

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

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/articles` | 获取文章列表（`page` / `per_page` 分页） |
| GET | `/api/articles/search` | 全文搜索（`q` / `page` / `per_page`） |
| POST | `/api/articles` | 发布新文章 |
| GET | `/api/articles/<id>` | 获取单篇文章详情 |
| PUT | `/api/articles/<id>` | 更新文章 |
| GET | `/api/articles/<id>/comments` | 获取评论列表（分页） |
| POST | `/api/articles/<id>/comments` | 发表评论 |

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
