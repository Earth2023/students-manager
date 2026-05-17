# 二次开发任务：学生信息管理系统

目标：添加功能 + 修改UI，完成后创建 dev branch 并 push 到远端。

## 后端改动

### 1. 学生头像/照片
- Student 模型新增 `avatar` 字段 (String, default="", 存图片文件名)
- 新增上传头像 API: `POST /api/students/{student_id}/avatar` (multipart)
- 静态文件目录 `uploads/avatars/` 存放上传的图片
- 返回头像 URL

### 2. 数据导出 CSV
- 新增 `GET /api/students/export?class_id=X` 导出当前班级学生为 CSV
- 中文表头, BOM 头支持 Excel 打开不乱码
- 统计该班级所有档案记录数

### 3. 批量导入学生 (CSV)
- 新增 `POST /api/students/import?class_id=X` (multipart file upload)
- 解析 CSV，列：学号,姓名,性别,出生日期,联系电话,家庭住址,家长姓名,家长电话,备注
- 跳过已有学号的学生，返回导入结果（成功数/失败数/失败原因）

### 4. 教师设置
- 新增 `PUT /api/auth/profile` 更新姓名、电话
- 新增 `PUT /api/auth/password` 修改密码（需旧密码验证）
- 新增 `GET /api/auth/profile` 获取完整教师信息

### 5. 搜索分页
- search API 新增 `page`、`page_size`、`class_id` 参数
- 返回 `{ items: [...], total: N, page: N, page_size: N }`

### 6. 档案记录增强
- 记录模型新增 `updated_at` 字段

## 前端改动

### 1. 暗色模式
- 在 AppHeader 添加暗色/亮色切换按钮
- 使用 Element Plus dark mode (CSS Variables)
- 持久化到 localStorage

### 2. 档案记录编辑
- RecordTimeline 组件添加"编辑"按钮
- 新增编辑对话框 (可改类型/标题/内容)
- RecordsView 中集成编辑功能

### 3. 数据导出
- 在学生管理页面添加"导出 CSV"按钮
- 在 Dashboard 添加导出按钮

### 4. 批量导入
- 学生管理页面添加"批量导入"按钮
- 导入对话框：上传 CSV + 选择目标班级
- 显示导入结果

### 5. 学生头像
- 学生详情页显示头像
- 学生表单支持上传头像
- 学生卡片显示头像

### 6. 教师设置页
- 新增 `/settings` 路由
- 修改密码 + 更新个人信息表单
- AppHeader 下拉菜单添加"设置"入口

### 7. 控制台图表
- 使用 ECharts 简单柱状图展示各类型档案记录数量
- 班级性别分布饼图

### 8. UI 优化
- 学生列表添加按性别筛选
- 学生列表添加按记录类型筛选
- 记录类型数量统计在详情页显示
- 页面整体间距和样式优化
- 响应式布局改进
- 添加加载骨架屏
