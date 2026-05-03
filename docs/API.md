# API 文档

基础地址：`http://127.0.0.1:18765/api`

认证方式：`Authorization: Bearer <token>`

---

## 认证

### 注册

```
POST /auth/register
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 2-50 字符 |
| password | string | 是 | 6-128 字符 |
| name | string | 是 | 教师姓名 |
| phone | string | 否 | 联系电话 |

**响应 200**

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### 登录

```
POST /auth/login
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**响应 200**

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### 获取当前用户

```
GET /auth/me
```

**响应 200**

```json
{
  "id": 1,
  "username": "teacher1",
  "name": "张老师",
  "phone": "13800138000"
}
```

---

## 班级

### 获取班级列表

```
GET /classes
```

**响应 200**

```json
[
  {
    "id": 1,
    "name": "三年级一班",
    "grade": "三年级",
    "student_count": 42
  }
]
```

### 创建班级

```
POST /classes
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 班级名称，如"三年级一班" |
| grade | string | 否 | 年级 |

**响应 201**

```json
{
  "id": 1,
  "name": "三年级一班",
  "grade": "三年级",
  "student_count": 0
}
```

### 获取班级学生 ID 列表

```
GET /classes/{class_id}/students
```

**响应 200**

```json
[1, 2, 3]
```

---

## 学生

### 添加学生

```
POST /students?class_id=1
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| class_id | int | 否 | 同时将学生加入指定班级 |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| student_no | string | 是 | 学号，唯一 |
| name | string | 是 | 姓名 |
| gender | string | 否 | 性别 |
| birth_date | string | 否 | 出生日期 (YYYY-MM-DD) |
| phone | string | 否 | 联系电话 |
| address | string | 否 | 家庭住址 |
| parent_name | string | 否 | 家长姓名 |
| parent_phone | string | 否 | 家长电话 |
| notes | string | 否 | 备注 |

**响应 201**

```json
{
  "id": 1,
  "student_no": "2024001",
  "name": "小明",
  "gender": "男",
  "birth_date": null,
  "phone": "13900139001",
  "address": "",
  "parent_name": "明爸爸",
  "parent_phone": "13900139000",
  "notes": "",
  "classes": [
    {
      "id": 1,
      "name": "三年级一班",
      "grade": "三年级"
    }
  ]
}
```

### 获取学生详情

```
GET /students/{student_id}
```

**响应 200** 结构同上，包含 `classes` 字段。

### 更新学生信息

```
PUT /students/{student_id}
```

请求体所有字段均为可选，只发送需要修改的字段。

### 删除学生

```
DELETE /students/{student_id}
```

**响应 204** 无内容

### 搜索学生

```
GET /students/search?q=关键字&class_id=1
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 按姓名或学号模糊搜索 |
| class_id | int | 否 | 限定班级范围 |

**响应 200**

```json
[
  {
    "id": 1,
    "student_no": "2024001",
    "name": "小明",
    "classes": [
      {
        "id": 1,
        "name": "三年级一班",
        "grade": "三年级"
      }
    ]
  }
]
```

---

## 档案记录

### 获取学生档案记录列表

```
GET /students/{student_id}/records
```

**响应 200**

```json
[
  {
    "id": 1,
    "student_id": 1,
    "teacher_id": 1,
    "teacher_name": "张老师",
    "title": "期中考试成绩",
    "content": "数学98分，语文95分",
    "record_type": "学业",
    "created_at": "2026-05-03T08:00:00Z"
  }
]
```

### 添加档案记录

```
POST /students/{student_id}/records
```

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 记录标题 |
| content | string | 是 | 记录内容 |
| record_type | string | 否 | 类型：`学业` `行为` `健康` `其他`（默认） |

**响应 201**

### 更新档案记录

```
PUT /students/{student_id}/records/{record_id}
```

或

```
PUT /records/{record_id}
```

### 删除档案记录

```
DELETE /students/{student_id}/records/{record_id}
```

或

```
DELETE /records/{record_id}
```

**响应 204** 无内容

---

## 错误响应

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 认证失败/凭据无效 |
| 404 | 资源不存在 |
| 422 | 请求体验证失败 |
| 500 | 服务器内部错误 |

错误体格式：

```json
{
  "detail": "错误描述信息"
}
```

---

在线 API 文档 (Swagger UI)：`http://127.0.0.1:18765/docs`
