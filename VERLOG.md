# 版本日志

## v1.0.0 (2026-05-03)

### 项目初始化

- 初始化 FastAPI 后端项目结构与配置
- 实现 SQLAlchemy 数据库模型（教师、班级、学生、档案记录）
- 实现 JWT 认证系统（注册、登录、Token 鉴权）
- 实现班级管理 API（创建、列表、切换）
- 实现学生 CRUD API（增删改查、搜索）
- 实现档案记录 API（时间线、添加、编辑、删除）
- 初始化 Vue 3 + Vite 前端项目
- 实现教师登录/注册页面
- 实现控制台仪表盘（班级切换、统计概览）
- 实现学生管理页面（列表搜索、新增、编辑、详情）
- 实现档案记录时间线页面
- 配置前端开发代理与 Element Plus UI

### 技术选型

| 类别 | 选型 |
|------|------|
| 后端框架 | FastAPI |
| 数据库 ORM | SQLAlchemy 2.0 + SQLite |
| 认证 | JWT (python-jose) + bcrypt |
| 前端框架 | Vue 3 + Vite |
| UI 组件 | Element Plus |
| 状态管理 | Pinia |
| HTTP 客户端 | Axios |

---

## 后续规划

### v1.1.0

- Android 客户端接入
- 学生头像上传
- Excel/CSV 数据导出

### v1.2.0

- 批量导入学生
- 数据库切换 PostgreSQL
- 权限分级
