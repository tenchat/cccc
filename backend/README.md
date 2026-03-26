# 大学生就业信息智能分析平台 - 后端

基于 FastAPI 的就业信息分析后端服务，集成 MiniMax 大语言模型。

---

## 环境要求

- Python 3.10+
- MySQL 8.0+ (或使用 Docker)
- Redis 6.0+ (可选，用于缓存)

---

## 第一步：安装 MySQL 并创建数据库

### 方式一：本地安装 MySQL

1. 下载并安装 [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)

2. 启动 MySQL 服务

3. 登录 MySQL
   ```bash
   mysql -u root -p
   ```

4. 创建数据库
   ```sql
   CREATE DATABASE employment_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. 确认数据库创建成功
   ```sql
   SHOW DATABASES;
   ```

### 方式二：使用 Docker

```bash
# 拉取 MySQL 镜像
docker pull mysql:8.0

# 运行 MySQL 容器
docker run -d \
  --name mysql-employment \
  -e MYSQL_ROOT_PASSWORD=your_password \
  -e MYSQL_DATABASE=employment_db \
  -p 3306:3306 \
  mysql:8.0

# 验证容器运行
docker ps
```

---

## 第二步：创建虚拟环境并安装依赖

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

---

## 第三步：配置环境变量

1. 复制环境变量模板
   ```bash
   copy .env.example .env
   # Linux/Mac:
   # cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入真实配置

```env
# MiniMax API配置（必须）
MINIMAX_API_KEY=your-minimax-api-key-here
MINIMAX_BASE_URL=https://api.minimaxi.com/anthropic
MINIMAX_MODEL=MiniMax-M2.7

# 数据库配置（必须）
# 格式: mysql+pymysql://用户名:密码@主机:端口/数据库名
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/employment_db

# Redis配置（可选，不填则不使用缓存）
REDIS_URL=redis://localhost:6379/0
```

### MiniMax API Key 获取

1. 访问 [MiniMax 开放平台](https://www.minimaxi.com/)
2. 注册/登录账号
3. 在控制台创建 API Key
4. 复制 API Key 到 `.env` 文件

---

## 第四步：启动后端服务

```bash
# 确保在 backend 目录下，虚拟环境已激活
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

看到以下输出表示启动成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

---

## 第五步：验证服务

### API 文档

访问 FastAPI 自动生成的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 健康检查

```bash
curl http://localhost:8000/health
```

预期响应：
```json
{"status": "healthy"}
```

### 测试学生列表 API

```bash
curl http://localhost:8000/api/v1/students
```

预期响应：
```json
{"total": 0, "page": 1, "page_size": 20, "items": []}
```

---

## 第六步：生成模拟数据

```bash
# 在 backend 目录下执行
python data/generate_mock_data.py
```

默认生成 500 条学生数据。指定数量：
```bash
python data/generate_mock_data.py 1000
```

预期输出：
```
成功生成 500 条学生模拟数据
总人数: 500, 就业人数: 302, 就业率: 60.4%
```

---

## 第七步：再次验证

```bash
# 获取学生列表
curl "http://localhost:8000/api/v1/students?page=1&page_size=5"

# 获取统计汇总
curl http://localhost:8000/api/v1/statistics/summary

# 按学院统计
curl http://localhost:8000/api/v1/statistics/by-college
```

---

## 项目结构

```
backend/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── api/v1/
│   │   ├── student.py       # 学生管理 API
│   │   ├── statistics.py    # 统计 API
│   │   └── ai.py            # AI 就业指导 API
│   ├── core/
│   │   ├── config.py        # 配置管理
│   │   └── database.py      # 数据库连接
│   ├── models/
│   │   └── student.py       # 学生数据模型
│   ├── schemas/
│   │   └── student.py       # Pydantic 模型
│   └── services/
│       ├── student_service.py  # 学生服务
│       └── ai_service.py       # AI 服务
├── data/
│   └── generate_mock_data.py # 模拟数据生成
├── .env                      # 环境变量（勿提交）
├── .env.example              # 环境变量模板
├── .gitignore
└── requirements.txt
```

---

## API 端点汇总

### 学生管理

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/students` | 获取学生列表（支持分页、筛选） |
| GET | `/api/v1/students/{id}` | 获取学生详情 |
| POST | `/api/v1/students` | 新增学生 |
| PUT | `/api/v1/students/{id}` | 更新学生 |
| DELETE | `/api/v1/students/{id}` | 删除学生 |

### 统计

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/statistics/summary` | 统计汇总 |
| GET | `/api/v1/statistics/by-college` | 按学院统计 |
| GET | `/api/v1/statistics/by-major` | 按专业统计 |
| GET | `/api/v1/statistics/by-province` | 按省份统计 |

### AI 就业指导

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/ai/employment-profile` | 就业竞争力画像 |
| POST | `/api/v1/ai/job-recommendation` | 岗位匹配推荐 |
| POST | `/api/v1/ai/skill-path` | 技能提升路径规划 |
| POST | `/api/v1/ai/warning` | 就业困难预警 |
| POST | `/api/v1/ai/resume-analysis` | 简历关键词优化 |
| POST | `/api/v1/ai/graduate-vs-job` | 考研vs就业决策辅助 |

---

## 常见问题

### 1. MySQL 连接被拒绝

检查：
- MySQL 服务是否启动
- 端口 3306 是否被占用
- 用户名密码是否正确

```bash
# Windows 检查 MySQL 服务
net start | findstr mysql

# Linux 检查
sudo systemctl status mysql
```

### 2. 依赖安装失败

```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 虚拟环境激活失败（Windows）

```powershell
# 使用 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate
```

### 4. 数据库表未创建

启动服务时会自动创建表。如果未创建，手动执行：

```python
from app.core.database import engine, Base
from app.models.student import Student

Base.metadata.create_all(bind=engine)
```

---

## Docker 一键启动（推荐）

如果只想快速体验，可以使用 Docker Compose：

```bash
cd backend

# 启动所有服务（MySQL + Redis + 后端）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 下一步

完成后端搭建后，可以继续：

1. **前端项目搭建** - Vue 3 + ECharts 可视化
2. **AI 功能测试** - 在 API 文档中测试 AI 接口
3. **数据导入** - 开发 Excel/CSV 批量导入功能
