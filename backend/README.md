# 大学生就业信息智能分析平台 - 后端开发指南

> 版本: v3.0 | 更新日期: 2026-03-26
>
> 特性: 模块化架构 | JWT认证 | Redis缓存 | AI智能分析

---

## 目录

1. [环境要求](#一环境要求)
2. [快速开始](#二快速开始)
3. [数据库配置（新手向）](#三数据库配置新手向)
4. [项目配置](#四项目配置)
5. [数据库结构详解](#五数据库结构详解)
6. [SQL模块说明](#六sql模块说明)
7. [项目结构](#七项目结构)
8. [CLI工具使用](#八cli工具使用)
9. [API接口说明](#九api接口说明)
10. [启动与验证](#十启动与验证)
11. [常见问题](#十一常见问题)

---

## 一、环境要求

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Python | 3.10+ | 编程语言 |
| MySQL | 8.0+ | 主数据库 |
| Redis | 6.0+ | 缓存（可选） |
| Git | 任意 | 代码管理 |

---

## 二、快速开始

### 2.1 一键启动（推荐）

```bash
# 进入后端目录
cd backend

# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
copy .env.example .env
# 编辑 .env 文件，填入真实配置（详见第四章）

# 5. 初始化数据库（详见第三章）
mysql -u root -p
SOURCE database/init.sql;

# 6. 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2.2 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 预期输出
{"status": "healthy"}
```

---

## 三、数据库配置（新手向）

### 3.1 什么是数据库？

**数据库（Database）** 就像一个电子化的文件柜，用来存储、组织和管理数据。

- **MySQL** 是一种常用的数据库管理系统
- **表（Table）** 是数据库中的基本单元，类似 Excel 表格
- **SQL** 是用来操作数据库的语言

### 3.2 安装 MySQL

#### 方式一：下载安装包

1. 访问 https://dev.mysql.com/downloads/mysql/
2. 选择 Windows Installer 或 macOS
3. 下载并安装，设置 root 用户密码

#### 方式二：使用 Docker（推荐）

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

# 验证运行
docker ps
```

#### 方式三：使用 phpStudy（Windows用户推荐）

1. 下载 phpStudy（https://www.xp.cn/）
2. 启动 MySQL 服务
3. 打开 phpMyAdmin 管理界面

### 3.3 登录 MySQL

打开终端（命令提示符），输入：

```bash
mysql -u root -p
```

- `-u root` 表示使用 root 用户
- `-p` 表示需要密码

按回车后输入密码即可登录。

**登录成功后的样子：**
```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.23 MySQL Community Server

mysql>
```

> 注意：`mysql>` 是 MySQL 的命令提示符，表示等待输入 SQL 命令

### 3.4 创建数据库并导入数据

**步骤1：创建数据库**

```sql
-- 创建名为 employment_db 的数据库
CREATE DATABASE employment_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**命令说明：**
- `CREATE DATABASE` - 创建数据库
- `employment_db` - 数据库名称（可以自定义）
- `DEFAULT CHARACTER SET utf8mb4` - 使用 UTF8 编码，支持中文

**验证创建成功：**
```sql
-- 查看所有数据库
SHOW DATABASES;
```

你会看到类似输出：
```
+--------------------+
| Database           |
+--------------------+
| employment_db      |  <-- 新创建的数据库
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
```

**步骤2：选中数据库**

```sql
USE employment_db;
```

**步骤3：导入 SQL 文件**

现在来创建数据库表。SQL 文件位于 `database/init_database.sql`。

#### 方法一：MySQL 命令行导入（推荐）

```bash
# 在系统命令行执行（退出 MySQL 后）
mysql -u root -p employment_db < database/init_database.sql
```

#### 方法二：在 MySQL 内执行 SOURCE 命令

```sql
SOURCE database/init_database.sql;
```

#### 方法三：使用 Navicat 或 phpMyAdmin

1. 打开 Navicat/phpMyAdmin
2. 选择 `employment_db` 数据库
3. 点击"导入"或"运行 SQL 文件"
4. 选择 `init_database.sql` 文件

### 3.5 验证导入成功

```sql
-- 查看所有表
SHOW TABLES;
```

**预期输出：**
```
+------------------------+
| Tables_in_employment_db|
+------------------------+
| accounts               |
| account_roles          |
| ai_analysis_requests   |
| ai_recommendations     |
| ai_services            |
| ai_warnings           |
| cities                 |
| companies              |
| data_audit_logs       |
| degrees                |
| employment_reports     |
| industries             |
| job_applications       |
| job_descriptions       |
| job_types              |
| permissions            |
| roles                  |
| salary_levels          |
| scarce_talents         |
| college_employment     |
| student_profiles       |
| universities           |
| work_years             |
+------------------------+
```

### 3.6 常见 SQL 命令示例

#### 查看表结构
```sql
-- 查看 accounts 表的所有字段
DESCRIBE accounts;
```

#### 查看表数据
```sql
-- 查看所有角色
SELECT * FROM roles;

-- 查看所有学生（限制10条）
SELECT * FROM student_profiles LIMIT 10;

-- 查看启用状态的用户
SELECT * FROM accounts WHERE status = 1;
```

#### 插入数据
```sql
-- 插入一条用户记录
INSERT INTO accounts (account_id, username, password_hash, real_name, phone)
VALUES ('STU001', 'zhangsan', 'hashed_password', '张三', '13800138000');
```

#### 更新数据
```sql
-- 更新用户信息
UPDATE accounts SET real_name = '李四' WHERE account_id = 'STU001';
```

#### 删除数据
```sql
-- 删除用户（谨慎使用！）
DELETE FROM accounts WHERE account_id = 'STU001';
```

#### 退出 MySQL
```sql
exit;

### 3.7 常见 SQL 命令

#### 查看表结构
```sql
-- 查看 accounts 表的所有字段
DESCRIBE accounts;

-- 或者
DESC accounts;
```

**输出示例：**
```
+-------------+-------------+------+-----+-------------------+----------------+
| Field       | Type        | Null | Key | Extra             | Comment        |
+-------------+-------------+------+-----+-------------------+----------------+
| account_id  | varchar(20) | NO   | PRI |                   | 账户标识       |
| username    | varchar(50) | NO   | UNI |                   | 用户名         |
| password_hash | varchar(255) | NO  |     |                   | 密码哈希       |
| real_name   | varchar(50) | YES  |     |                   | 真实姓名       |
| email       | varchar(100)| YES  | MUL |                   | 邮箱           |
| phone       | varchar(20) | YES  | MUL |                   | 手机号         |
| status      | tinyint     | YES  | MUL |                   | 状态           |
+-------------+-------------+------+-----+-------------------+----------------+
```

#### 查看表数据
```sql
-- 查看所有角色
SELECT * FROM roles;

-- 查看所有学生（限制10条）
SELECT * FROM student_profiles LIMIT 10;

-- 查看特定条件的数据
SELECT * FROM accounts WHERE status = 1;
```

#### 插入数据
```sql
-- 插入一条用户记录
INSERT INTO accounts (account_id, username, password_hash, real_name, phone)
VALUES ('STU001', 'zhangsan', 'hashed_password', '张三', '13800138000');
```

#### 更新数据
```sql
-- 更新用户信息
UPDATE accounts SET real_name = '李四' WHERE account_id = 'STU001';
```

#### 删除数据
```sql
-- 删除用户（谨慎使用！）
DELETE FROM accounts WHERE account_id = 'STU001';
```

#### 退出 MySQL
```sql
exit;
```

---

## 四、项目配置

### 4.1 环境变量配置

复制配置文件模板：

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件：

```env
# ===================
# MiniMax AI 配置（必须）
# ===================
MINIMAX_API_KEY=your-api-key-here
MINIMAX_BASE_URL=https://api.minimax.chat/v1
MINIMAX_MODEL=MiniMax-Text-01

# ===================
# 数据库配置（必须）
# ===================
# 格式: mysql+pymysql://用户名:密码@主机:端口/数据库名
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/employment_db

# ===================
# Redis 配置（可选）
# 不填则使用内存缓存
# ===================
REDIS_URL=redis://localhost:6379/0

# ===================
# JWT 配置（必须）
# ===================
# 生成密钥方法：python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 4.2 MiniMax API Key 获取

1. 访问 https://www.minimaxi.com/
2. 注册/登录账号
3. 进入控制台创建 API Key
4. 复制到 `.env` 文件的 `MINIMAX_API_KEY`

### 4.3 生成密钥

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

复制输出到 `SECRET_KEY` 配置项。

---

---

## 五、数据库结构

### 6.1 表清单

共 24 张表，涵盖学生、学校、企业、岗位、AI服务等完整业务。

| 表名 | 说明 |
|------|------|
| accounts | 统一账户表（学生/学校/企业共用） |
| roles | 角色表 |
| permissions | 权限表 |
| account_roles | 用户角色关联表 |
| role_permissions | 角色权限关联表 |
| universities | 院校表 |
| student_profiles | 学生详细档案表 |
| companies | 用人单位表 |
| job_descriptions | 岗位需求表 |
| job_applications | 岗位申请记录表 |
| degrees | 学历字典 |
| salary_levels | 薪资字典 |
| work_years | 工作年限字典 |
| industries | 行业字典 |
| job_types | 职类字典 |
| cities | 城市字典 |
| employment_reports | 就业报告表 |
| scarce_talents | 各省稀缺人才表 |
| college_employment | 学院就业率表 |
| ai_services | AI服务类型表 |
| ai_analysis_requests | AI分析请求记录表 |
| ai_recommendations | AI推荐结果表 |
| ai_warnings | AI预警记录表 |
| data_audit_logs | 数据操作审计日志表 |

### 6.2 核心表说明

#### accounts - 统一账户表

所有用户（学生、学校管理员、企业）共用此表。

| 字段 | 类型 | 说明 |
|------|------|------|
| account_id | VARCHAR(20) | 账户ID，主键 |
| username | VARCHAR(50) | 用户名，唯一 |
| password_hash | VARCHAR(255) | 密码哈希（加密存储） |
| real_name | VARCHAR(50) | 真实姓名/企业名 |
| email | VARCHAR(100) | 邮箱 |
| phone | VARCHAR(20) | 手机号 |
| status | TINYINT | 状态：0=禁用，1=启用 |
| last_login_at | DATETIME | 最后登录时间 |

#### roles - 角色表

| 角色代码 | 角色名称 | 说明 |
|---------|---------|------|
| admin | 系统管理员 | 最高权限 |
| student | 学生 | 普通学生用户 |
| school_admin | 学校管理员 | 就业指导中心 |
| school_viewer | 学校查看员 | 数据查看 |
| company_admin | 企业管理员 | 用人单位 |
| company_recruiter | 企业招聘者 | 发布岗位 |

#### student_profiles - 学生档案表

| 字段 | 类型 | 说明 |
|------|------|------|
| profile_id | INT | 档案ID |
| account_id | VARCHAR(20) | 关联账户ID |
| student_id | VARCHAR(20) | 学号 |
| university_id | VARCHAR(20) | 院校代码 |
| college | VARCHAR(100) | 学院 |
| major | VARCHAR(100) | 专业 |
| degree | VARCHAR(20) | 学历 |
| graduation_year | INT | 毕业年份 |

#### companies - 企业表

| 字段 | 类型 | 说明 |
|------|------|------|
| company_id | VARCHAR(20) | 企业ID |
| account_id | VARCHAR(20) | 关联账户ID |
| company_name | VARCHAR(100) | 企业名称 |
| industry | VARCHAR(50) | 所属行业 |
| scale | VARCHAR(20) | 规模 |
| verified | TINYINT | 认证状态 |

#### job_descriptions - 岗位表

| 字段 | 类型 | 说明 |
|------|------|------|
| jd_no | VARCHAR(20) | 岗位编号 |
| company_id | VARCHAR(20) | 发布企业 |
| jd_title | VARCHAR(100) | 岗位名称 |
| city | VARCHAR(50) | 工作城市 |
| min_salary | INT | 最低薪资 |
| max_salary | INT | 最高薪资 |
| status | TINYINT | 状态：0=下架，1=发布中 |

#### ai_services - AI服务表

| 服务代码 | 服务名称 | 说明 |
|---------|---------|------|
| career_match | 就业方向匹配 | 推荐就业方向 |
| salary_prediction | 薪资预测 | 预测薪资范围 |
| skill_gap_analysis | 技能差距分析 | 分析技能差距 |
| resume_optimization | 简历优化 | 优化简历 |
| job_recommendation | 岗位推荐 | 智能推荐岗位 |

---

## 六、SQL基础语法

### 7.1 常用SQL命令

#### CREATE - 创建

```sql
-- 创建表
CREATE TABLE 表名 (
    字段名 类型 约束,
    字段名 类型 约束
);

-- 示例
CREATE TABLE test (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT
);
```

#### INSERT - 插入

```sql
-- 插入单条
INSERT INTO 表名 (字段1, 字段2) VALUES (值1, 值2);

-- 插入多条
INSERT INTO 表名 (字段1, 字段2) VALUES
(值1, 值2),
(值3, 值4),
(值5, 值6);
```

#### SELECT - 查询

```sql
-- 查询所有
SELECT * FROM 表名;

-- 条件查询
SELECT 字段1, 字段2 FROM 表名 WHERE 条件;

-- 排序
SELECT * FROM 表名 ORDER BY 字段 DESC;

-- 限制数量
SELECT * FROM 表名 LIMIT 10;

-- 统计数量
SELECT COUNT(*) FROM 表名;

-- 分组统计
SELECT 字段, COUNT(*) FROM 表名 GROUP BY 字段;
```

#### UPDATE - 更新

```sql
UPDATE 表名 SET 字段1 = 新值 WHERE 条件;
```

#### DELETE - 删除

```sql
DELETE FROM 表名 WHERE 条件;
```

---

## 七、项目结构

```
backend/
├── app/
│   ├── main.py                 # FastAPI 入口
│   ├── api/v1/                 # API 路由
│   │   ├── auth.py            # 认证接口
│   │   ├── student.py         # 学生接口
│   │   ├── statistics.py      # 统计接口
│   │   └── ai.py              # AI接口
│   ├── core/                   # 核心模块
│   │   ├── config.py          # 配置管理
│   │   ├── database.py        # 数据库连接
│   │   ├── password.py        # 密码加密
│   │   ├── jwt.py             # JWT令牌
│   │   ├── redis_client.py    # Redis客户端
│   │   ├── rate_limiter.py    # 限流器
│   │   ├── lockout.py         # 账户锁定
│   │   ├── session.py         # 会话管理
│   │   ├── audit.py           # 审计日志
│   │   ├── errors.py          # 错误定义
│   │   └── dependencies.py     # 依赖注入
│   ├── models/                 # 数据模型
│   │   ├── account.py         # 账户模型
│   │   ├── role.py           # 角色模型
│   │   ├── student.py        # 学生模型
│   │   ├── company.py        # 企业模型
│   │   └── job.py            # 岗位模型
│   ├── schemas/                # Pydantic模型
│   │   ├── auth.py           # 认证Schema
│   │   └── student.py        # 学生Schema
│   ├── services/               # 业务服务
│   │   └── auth/             # 认证服务
│   │       ├── register.py   # 注册
│   │       ├── login.py      # 登录
│   │       └── token.py      # Token
│   └── cli/                    # 命令行工具
│       └── __init__.py        # CLI命令
├── database/                    # SQL文件
│   └── init_database.sql      # 数据库初始化脚本
├── data/                        # 数据脚本
│   └── generate_mock_data.py # 模拟数据
├── .env                         # 环境变量
├── .env.example                # 环境变量模板
└── requirements.txt            # 依赖
```

---

## 八、CLI工具使用

CLI工具提供命令行方式管理数据库和账户。

### 8.1 可用命令

```bash
python -m app.cli --help
```

**输出：**
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  就业信息平台CLI工具

Options:
  --help  Show this message and exit.

Commands:
  init-db          初始化数据库表
  create-roles     创建默认角色
  admin            创建管理员账户
  unlock           解锁账号
  verify-company   审核企业
  list-companies   列出待审核企业
```

### 8.2 初始化数据库

```bash
# 初始化所有表（使用SQLAlchemy自动创建）
python -m app.cli init-db
```

### 8.3 创建默认角色

```bash
python -m app.cli create-roles
```

### 8.4 创建管理员

```bash
# 创建管理员账户
python -m app.cli admin --username admin --name "系统管理员" --password "Admin123!"

# 如果不指定密码，使用默认密码 Admin123!
python -m app.cli admin --username admin --name "系统管理员"
```

### 8.5 解锁账号

当账户被锁定时（连续5次密码错误）：

```bash
python -m app.cli unlock --account-id STU001
```

### 8.6 审核企业

```bash
# 通过审核
python -m app.cli verify-company --company-id C001 --action approve

# 拒绝审核
python -m app.cli verify-company --company-id C001 --action reject
```

### 8.7 列出待审核企业

```bash
python -m app.cli list-companies
```

---

## 九、API接口说明

### 9.1 认证接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/v1/auth/register` | 注册 | 否 |
| POST | `/api/v1/auth/login` | 登录 | 否 |
| POST | `/api/v1/auth/refresh` | 刷新Token | 否 |
| POST | `/api/v1/auth/logout` | 登出 | 是 |
| GET | `/api/v1/auth/me` | 获取当前用户 | 是 |
| GET | `/api/v1/auth/sessions` | 会话列表 | 是 |
| DELETE | `/api/v1/auth/sessions/{id}` | 终止会话 | 是 |

### 9.2 学生接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/students` | 学生列表 | 是 |
| GET | `/api/v1/students/{id}` | 学生详情 | 是 |
| GET | `/api/v1/students/profile` | 我的档案 | 是 |
| PUT | `/api/v1/students/profile` | 更新档案 | 是 |

### 9.3 统计接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/statistics/summary` | 统计汇总 | 是 |
| GET | `/api/v1/statistics/by-college` | 学院统计 | 是 |
| GET | `/api/v1/statistics/by-major` | 专业统计 | 是 |
| GET | `/api/v1/statistics/by-province` | 省份统计 | 是 |

### 9.4 AI接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/ai/services` | AI服务列表 | 是 |
| POST | `/api/v1/ai/analyze` | 发起分析 | 是 |
| GET | `/api/v1/ai/requests/{id}` | 分析结果 | 是 |
| GET | `/api/v1/ai/recommendations` | 推荐列表 | 是 |
| GET | `/api/v1/ai/warnings` | 预警列表 | 是 |

### 9.5 API调用示例

#### 注册

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "Aa123456!",
    "role": "student",
    "real_name": "张三",
    "email": "zhangsan@example.com",
    "phone": "13800138000"
  }'
```

#### 登录

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "Aa123456!"
  }'
```

#### 获取用户信息

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer your_access_token"
```

---

## 十、启动与验证

### 10.1 启动服务

```bash
# 开发模式（热重载）
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 10.2 验证

```bash
# 健康检查
curl http://localhost:8000/health

# API文档
# 浏览器访问 http://localhost:8000/docs
```

### 10.3 生成模拟数据

```bash
python data/generate_mock_data.py
```

---

## 十一、常见问题

### Q1: MySQL 连接被拒绝

**原因：**
- MySQL 服务未启动
- 端口 3306 被占用
- 用户名密码错误

**解决方法：**

```bash
# Windows 检查 MySQL 服务
net start | findstr mysql

# 启动 MySQL 服务
net start mysql
```

### Q2: 依赖安装失败

```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 虚拟环境激活失败（Windows）

```powershell
# 使用 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate
```

### Q4: Redis 连接失败

Redis 是可选的。如果不使用 Redis，系统会使用内存缓存。

如果需要使用 Redis：
1. 安装 Redis Desktop Manager 或在服务器安装
2. 确保 `.env` 中 `REDIS_URL` 配置正确
3. 如果只是开发环境，可以先不配置 Redis

### Q5: 账户被锁定

连续 5 次密码错误会锁定账户 15 分钟。

**解决方法：**
```bash
# 使用 CLI 解锁
python -m app.cli unlock --account-id 你的账户ID
```

### Q6: 如何重置数据库？

```sql
-- 删除所有表（按外键顺序）
DROP TABLE IF EXISTS job_applications;
DROP TABLE IF EXISTS job_descriptions;
DROP TABLE IF EXISTS ai_warnings;
DROP TABLE IF EXISTS ai_recommendations;
DROP TABLE IF EXISTS ai_analysis_requests;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS student_profiles;
DROP TABLE IF EXISTS data_audit_logs;
DROP TABLE IF EXISTS universities;
DROP TABLE IF EXISTS account_roles;
DROP TABLE IF EXISTS permissions;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS accounts;
-- 字典表
DROP TABLE IF EXISTS degrees;
DROP TABLE IF EXISTS salary_levels;
DROP TABLE IF EXISTS work_years;
DROP TABLE IF EXISTS industries;
DROP TABLE IF EXISTS job_types;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS scarce_talents;
DROP TABLE IF EXISTS employment_reports;
DROP TABLE IF EXISTS college_employment;
DROP TABLE IF EXISTS ai_services;

-- 重新导入
SOURCE database/init_database.sql;
```

---

## 下一步

完成后端搭建后，可以：

1. **启动前端** - Vue 3 + ECharts 可视化
2. **测试AI功能** - 在 http://localhost:8000/docs 测试
3. **扩展功能** - 参考 plan 文件添加新功能

---

*文档版本: v3.0 | 最后更新: 2026-03-26*
