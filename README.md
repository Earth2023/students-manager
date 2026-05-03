# 学生信息管理系统

面向全体教师的学生信息管理平台，支持 Web 端访问。教师可切换班级、查询/更改学生信息、随时提交学生档案记录，每位学生独立建档。

## 功能特性

- **教师认证** — 注册、登录、JWT 身份验证
- **班级管理** — 创建班级、多班级切换、班级学生概览
- **学生管理** — 学生信息增删改查、按姓名/学号搜索
- **档案记录** — 按学生维度记录学业/行为/健康等信息，时间线展示
- **统计概览** — 控制台仪表盘，班级人数、记录总数一目了然

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI (Python 3.11) |
| 数据库 | SQLAlchemy + SQLite（可切换 PostgreSQL/MySQL） |
| 认证 | JWT (python-jose) + bcrypt |
| 前端框架 | Vue 3 + Vite |
| UI 组件 | Element Plus |
| 状态管理 | Pinia |
| HTTP 客户端 | Axios |

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

服务运行在 http://127.0.0.1:8000

交互式 API 文档：http://127.0.0.1:8000/docs

### 前端

```bash
cd web
npm install
npm run dev
```

服务运行在 http://127.0.0.1:5173

前端开发服务器自动将 `/api` 请求代理到后端。

## 项目结构

```
├── backend/
│   └── app/
│       ├── main.py              # 应用入口
│       ├── config.py            # 配置
│       ├── database.py          # 数据库连接
│       ├── models/              # SQLAlchemy 数据模型
│       ├── schemas/             # Pydantic 校验模型
│       ├── api/                 # RESTful 路由
│       └── core/                # 安全与依赖
├── web/
│   └── src/
│       ├── router/              # 前端路由
│       ├── stores/              # Pinia 状态
│       ├── api/                 # Axios API 层
│       ├── views/               # 页面组件
│       └── components/          # 通用组件
├── README.md
└── VERLOG.md
```

## 后续计划

- [ ] Android 客户端对接
- [ ] 学生照片/头像上传
- [ ] 数据导出（Excel/CSV）
- [ ] 批量导入学生
- [ ] 数据库切换至 PostgreSQL
