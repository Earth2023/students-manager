# 学生信息管理系统

面向全体教师的学生信息管理平台，支持 **Web** 与 **Android** 双端访问。教师可切换班级、查询/更改学生信息、随时提交学生档案记录，每位学生独立建档。

## 功能特性

- **教师认证** — 注册、登录、JWT 身份验证
- **班级管理** — 创建班级、多班级切换、班级学生概览
- **学生管理** — 学生信息增删改查、按姓名/学号搜索
- **档案记录** — 按学生维度记录学业/行为/健康等信息，时间线展示
- **统计概览** — 控制台仪表盘，班级人数、记录总数一目了然
- **Android 客户端** — Capacitor 封装，支持 Android 9+

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI (Python 3.11+) |
| 数据库 | SQLAlchemy + SQLite（可切换 PostgreSQL/MySQL） |
| 认证 | JWT (python-jose) + bcrypt |
| 前端框架 | Vue 3 + Vite |
| UI 组件 | Element Plus |
| 状态管理 | Pinia |
| 移动端 | Capacitor 8 (Android) |

## 快速开始

### 方式一：一键部署（推荐）

Windows：
```bash
start.bat
```

Linux / macOS：
```bash
chmod +x start.sh && ./start.sh
```

脚本会自动安装依赖、构建前端、启动服务。访问 http://127.0.0.1:18765

### 方式二：开发模式

Windows：
```bash
start-dev.bat
```

Linux / macOS：
```bash
chmod +x start-dev.sh && ./start-dev.sh
```

开发模式下后端 (18765) 和前端 (5173) 独立运行，支持热重载。

### 方式三：手动启动

```bash
# 终端 1：后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 18765

# 终端 2：前端
cd web
npm install
npm run dev
```

前端开发服务器运行在 http://127.0.0.1:5173，`/api` 请求自动代理到后端。

## 构建 Android APK

```bash
# 1. 构建前端
cd web && npm run build

# 2. 同步到 Android
npx cap sync android

# 3. 构建 APK
cd ../android && ./gradlew assembleDebug

# 4. APK 位于:
#    android/app/build/outputs/apk/debug/app-debug.apk
```

安装到模拟器（以 MuMu 12 为例）：
```bash
adb connect 127.0.0.1:16384
adb -s 127.0.0.1:16384 reverse tcp:18765 tcp:18765
adb -s 127.0.0.1:16384 install -r android/app/build/outputs/apk/debug/app-debug.apk
```

> **注意**: Android 端默认通过 ADB 反向代理连接宿主机后端。更换服务端地址请编辑 `web/public/server-config.json` 后重新构建。

## 项目结构

```
├── backend/                    # Python FastAPI 后端
│   └── app/
│       ├── main.py             # 应用入口（含静态文件服务）
│       ├── config.py           # 配置
│       ├── database.py         # 数据库连接
│       ├── models/             # SQLAlchemy 数据模型
│       ├── schemas/            # Pydantic 校验模型
│       ├── api/                # RESTful 路由
│       └── core/               # 安全与依赖
├── web/                        # Vue 3 前端
│   └── src/
│       ├── router/             # 前端路由
│       ├── stores/             # Pinia 状态管理
│       ├── api/                # Axios API 层
│       ├── views/              # 页面组件
│       └── components/         # 通用组件
├── android/                    # Capacitor Android 工程
│   └── app/src/main/java/      # Android Java 源码
├── docs/
│   └── API.md                  # REST API 文档
├── start.bat                   # Windows 一键部署
├── start-dev.bat               # Windows 开发模式
├── start.sh                    # Linux/macOS 一键部署
├── start-dev.sh                # Linux/macOS 开发模式
└── README.md
```

## API 文档

启动后端后访问 http://127.0.0.1:18765/docs 查看 Swagger UI，或查看 [docs/API.md](docs/API.md)。

## 后续计划

- [x] Android 客户端
- [ ] 学生照片/头像上传
- [ ] 数据导出（Excel/CSV）
- [ ] 批量导入学生
- [ ] 数据库切换至 PostgreSQL
