---
name: cccc-project-patterns
description: Coding patterns extracted from cccc (大学生就业信息智能分析平台)
version: 1.0.0
source: local-git-analysis
analyzed_commits: 4
---

# 大学生就业信息智能分析平台 - 项目规范

## 项目概述

- **项目名称**: cccc (大学生就业信息智能分析平台)
- **用途**: 计算机设计大赛 - 高校就业信息智能分析
- **前端**: Vue 3 + Vite + TypeScript + Element Plus + ECharts
- **后端**: FastAPI + MySQL + Redis + MiniMax AI

---

## 技术架构

### 目录结构

```
cccc/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/           # API 路由 (auth.py, student.py, ai.py, statistics.py)
│   │   ├── core/             # 核心模块 (config, database, jwt, password, redis, etc.)
│   │   ├── models/           # SQLAlchemy 模型 (account, student, company, job, etc.)
│   │   ├── schemas/          # Pydantic Schema (auth, student, company, job)
│   │   ├── services/         # 业务服务层 (auth/, student_service.py, ai_service.py)
│   │   └── cli/              # 命令行工具
│   ├── database/             # SQL 初始化脚本
│   ├── data/                 # 数据脚本 (generate_mock_data.py)
│   └── requirements.txt      # Python 依赖
│
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── api/             # API 请求封装 (request.ts, auth.ts, student.ts, dashboard.ts)
│   │   ├── components/      # 公共组件 (common/, charts/, layout/)
│   │   ├── composables/     # Vue Composables (useChart.ts)
│   │   ├── layouts/         # 布局组件 (RoleLayout.vue, MainLayout.vue)
│   │   ├── router/          # Vue Router 配置
│   │   ├── stores/          # Pinia 状态管理 (user.ts, app.ts)
│   │   ├── types/           # TypeScript 类型定义
│   │   ├── views/           # 页面组件 (student/, school/, admin/, company/)
│   │   └── App.vue          # 根组件
│   └── package.json
│
└── dataset/                  # 数据集
```

---

## 代码规范

### Python (后端)

1. **类型注解**: 所有函数签名必须使用类型注解
   ```python
   from fastapi import APIRouter, Depends
   from sqlalchemy.orm import Session

   router = APIRouter(prefix="/auth", tags=["认证"])

   @router.post("/register")
   async def register(req: RegisterRequest, db: Session = Depends(get_db)):
       ...
   ```

2. **Schema 使用 Pydantic**: 请求/响应模型使用 Pydantic
   ```python
   from pydantic import BaseModel, EmailStr

   class RegisterRequest(BaseModel):
       username: str
       password: str
       role: str
       real_name: str
       email: EmailStr | None = None
   ```

3. **模块化服务**: 业务逻辑放在 `services/` 目录
   ```
   services/
   ├── auth/
   │   ├── register.py
   │   ├── login.py
   │   └── token.py
   ├── student_service.py
   └── ai_service.py
   ```

4. **CLI 工具**: 使用 Click 构建命令行工具
   ```bash
   python -m app.cli --help
   python -m app.cli admin --username admin --name "管理员"
   python -m app.cli verify-company --company-id C001 --action approve
   ```

### TypeScript/Vue (前端)

1. **组件命名**: Vue 组件使用 PascalCase
   - 页面组件: `Dashboard.vue`, `Students.vue`
   - 布局组件: `RoleLayout.vue`, `MainLayout.vue`
   - 图表组件: `ChinaHeatmap.vue`, `EmploymentPie.vue`

2. **API 封装**: 统一使用 `request.ts` 封装
   ```typescript
   // src/api/student.ts
   import { get, post, put } from './request'

   export const getStudentList = (params: StudentListParams) => {
     return get<PaginatedResponse<StudentProfile>>('/students', { params })
   }
   ```

3. **路由组织**: 按角色模块化
   ```
   /student/*    - 学生端
   /school/*    - 学校端
   /admin/*     - 管理端
   /company/*   - 企业端
   ```

4. **图标导入**: Element Plus 图标需显式导入
   ```typescript
   import { Refresh, Loading } from '@element-plus/icons-vue'
   ```

---

## Git 提交规范

项目目前使用**描述性提交信息**：

| 类型 | 示例 |
|------|------|
| 功能 | "Add student profile management" |
| 重构 | "Refactor code structure for improved readability" |
| 修复 | "Fix login validation error" |
| 初始化 | "Initialization" |

**建议未来采用 Conventional Commits**：
```
feat: 添加学生档案管理功能
fix: 修复登录验证错误
refactor: 重构代码结构
docs: 更新API文档
chore: 更新依赖版本
```

---

## API 设计模式

### RESTful 端点结构

```
认证:
POST   /api/v1/auth/register     - 注册
POST   /api/v1/auth/login        - 登录
POST   /api/v1/auth/refresh      - 刷新Token
POST   /api/v1/auth/logout        - 登出
GET    /api/v1/auth/me           - 当前用户

学生:
GET    /api/v1/students          - 学生列表
GET    /api/v1/students/{id}     - 学生详情
GET    /api/v1/students/profile  - 我的档案
PUT    /api/v1/students/profile  - 更新档案

统计:
GET    /api/v1/statistics/summary     - 统计汇总
GET    /api/v1/statistics/by-college - 学院统计

AI:
GET    /api/v1/ai/services           - AI服务列表
POST   /api/v1/ai/analyze            - 发起分析
```

### 请求/响应模式

```typescript
// 请求封装
export const get = <T>(url: string, config?: RequestConfig) => {
  return request.get<T>(url, config)
}

// 响应类型
interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
}
```

---

## 数据库模式

### 核心表关系

```
accounts (账户)
├── account_roles ──► roles (角色)
├── student_profiles (学生档案)
├── companies (企业)
└── school_admins (学校管理员)

job_descriptions (岗位) ──► companies (企业)
job_applications (申请) ──► accounts, job_descriptions
```

### 角色体系

| 角色代码 | 角色名称 | 说明 |
|---------|---------|------|
| admin | 系统管理员 | 最高权限 |
| student | 学生 | 普通学生用户 |
| school_admin | 学校管理员 | 就业指导中心 |
| school_viewer | 学校查看员 | 数据查看 |
| company_admin | 企业管理员 | 用人单位 |
| company_recruiter | 企业招聘者 | 发布岗位 |

---

## 常见任务模式

### 添加新的 API 端点

1. **后端**:
   - 在 `app/schemas/` 添加 Pydantic Model
   - 在 `app/api/v1/` 添加路由
   - 在 `app/services/` 添加业务逻辑

2. **前端**:
   - 在 `src/api/` 添加 API 函数
   - 在 `src/views/` 添加页面组件
   - 在 `src/router/index.ts` 添加路由

### 添加新的图表组件

1. 在 `frontend/src/components/charts/` 创建组件
2. 使用 `vue-echarts` + ECharts
3. 在 `useChart.ts` 中注册图表类型

---

## 环境配置

### 后端环境变量 (.env)

```env
MINIMAX_API_KEY=your-api-key
MINIMAX_BASE_URL=https://api.minimax.chat/v1
MINIMAX_MODEL=MiniMax-Text-01
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/employment_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Python 环境

```bash
# 使用 conda 环境
conda activate cccc

# 安装依赖
pip install -r requirements.txt

# 启动后端
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端环境

```bash
cd frontend
npm install
npm run dev    # 开发服务器
npm run build  # 生产构建
```

---

## 测试验证

### 后端健康检查

```bash
curl http://localhost:8000/health
# 预期: {"status": "healthy"}
```

### 前端构建验证

```bash
cd frontend
npm run build  # 必须无错误通过
npx vue-tsc --noEmit  # TypeScript 类型检查
```

---

*Generated from git history analysis (4 commits analyzed)*
