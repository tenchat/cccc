# 大学生就业信息智能分析平台 - 数据库设计文档

> 版本: v2.0 | 更新日期: 2026-03-26
>
> 特性: 支持学生、学校、用人单位三方角色，AI分析决策

---

## 一、系统概述

### 1.1 三角色权限体系

本系统支持三类用户角色，所有角色都可以：
- 访问平台数据
- 使用 AI 服务进行决策分析
- 上传和管理自己的数据

| 角色 | 说明 | 主要权限 |
|------|------|---------|
| 学生 | 高校毕业生 | 查看岗位、申请职位、AI就业指导 |
| 用人单位 | 企业HR | 发布岗位、查看学生简历、AI招聘分析 |
| 学校 | 就业指导中心 | 管理学生档案、上报就业率、AI决策分析 |

### 1.2 技术规范

- 数据库：MySQL 8.0+
- 字符集：utf8mb4
- 存储引擎：InnoDB
- 脚本位置：`backend/database/init_database.sql`

---

## 二、数据库结构（ER图）

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              认证与权限层                                         │
│  ┌──────────┐    ┌──────────┐    ┌────────────────┐    ┌──────────────────┐     │
│  │ accounts │───▶│account_  │───▶│     roles      │◀───│role_permissions │     │
│  │ (账户)   │    │  roles   │    │    (角色)       │    │  (角色权限)      │     │
│  └──────────┘    └──────────┘    └────────────────┘    └──────────────────┘     │
│        │                                                               │          │
│        │         ┌────────────────┐    ┌────────────────┐             │          │
│        └────────▶│student_profiles │    │   companies    │◀────────────┘          │
│                  │  (学生档案)     │    │   (用人单位)   │                       │
│                  └───────┬────────┘    └───────┬────────┘                       │
│                          │                     │                                │
│                          │              ┌──────▼───────┐                        │
│                          │              │job_descriptions│                      │
│                          │              │   (岗位需求)   │                      │
│                          │              └──────┬───────┘                        │
│                          │                     │                                 │
└──────────────────────────┼────────────────────┼─────────────────────────────────┘
                           │                     │
                    ┌──────▼─────────────────────▼───────┐
                    │          ai_services                 │
                    │         (AI服务类型)                  │
                    │  ┌─────────────────────────────────┐ │
                    │  │career_match | salary_prediction│ │
                    │  │skill_gap | resume_optimization  │ │
                    │  │job_recommendation | warning     │ │
                    │  └─────────────────────────────────┘ │
                    └──────────┬───────────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
    ┌─────────────────┐ ┌───────────┐ ┌──────────────────┐
    │ai_analysis_      │ │ai_recom-  │ │  ai_warnings     │
    │requests          │ │mendations │ │  (AI预警记录)     │
    │(AI分析请求)       │ │(AI推荐结果)│ └──────────────────┘
    └─────────────────┘ └───────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │                         业务数据层                              │
    │  ┌──────────┐  ┌──────────────┐  ┌────────────────┐            │
    │  │universities│ │employment_    │  │scarce_          │            │
    │  │ (院校)    │  │reports        │  │talents          │            │
    │  └──────────┘  │(就业报告)     │  │(各省稀缺人才)   │            │
    │                └──────────────┘  └────────────────┘            │
    │                                                             │
    │  ┌──────────────────┐   ┌────────────────────────────┐      │
    │  │college_employment │   │    data_audit_logs        │      │
    │  │  (学院就业率)      │   │    (数据操作审计日志)     │      │
    │  └──────────────────┘   └────────────────────────────┘      │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │                         字典表层                                  │
    │  degrees | salary_levels | work_years | industries | job_types |cities │
    └─────────────────────────────────────────────────────────────────┘
```

---

## 三、表结构详细说明

### 3.1 认证与权限相关表

#### 3.1.1 统一账户表 (accounts)

所有用户（学生、学校管理员、企业）共用此表。

| 字段 | 类型 | 说明 |
|------|------|------|
| account_id | VARCHAR(20) | 账户标识，主键 |
| username | VARCHAR(50) | 用户名，唯一 |
| password_hash | VARCHAR(255) | 密码哈希 |
| real_name | VARCHAR(50) | 真实姓名/企业名 |
| email | VARCHAR(100) | 邮箱 |
| phone | VARCHAR(20) | 手机号 |
| avatar_url | VARCHAR(255) | 头像URL |
| status | TINYINT | 状态(0=禁用 1=启用) |
| last_login_at | DATETIME | 最后登录时间 |
| created_at | DATETIME | 创建时间 |

---

#### 3.1.2 角色表 (roles)

| role_id | role_code | role_name | description |
|---------|-----------|-----------|------------|
| 1 | admin | 系统管理员 | 系统管理最高权限 |
| 2 | student | 学生 | 学生用户 |
| 3 | school_admin | 学校管理员 | 学校就业指导中心 |
| 4 | school_viewer | 学校查看员 | 学校数据查看权限 |
| 5 | company_admin | 企业管理员 | 用人单位管理员 |
| 6 | company_recruiter | 企业招聘者 | 发布岗位和管理简历 |

---

#### 3.1.3 权限表 (permissions)

| permission_code | permission_name | resource_type | action |
|----------------|-----------------|---------------|--------|
| student.profile.read | 查看自己的档案 | user | read |
| student.profile.write | 编辑自己的档案 | user | write |
| student.job.read | 查看岗位信息 | job | read |
| student.job.apply | 申请岗位 | job | write |
| student.ai.analyze | AI就业分析 | ai | write |
| company.job.write | 发布管理岗位 | job | write |
| company.student.read | 查看学生信息 | user | read |
| school.college.write | 管理学院就业率 | college | write |
| school.ai.analyze | AI决策分析 | ai | write |
| ... | ... | ... | ... |

---

### 3.2 业务数据表

#### 3.2.1 学生详细档案表 (student_profiles)

| 字段 | 类型 | 说明 |
|------|------|------|
| profile_id | INT | 档案ID，主键 |
| account_id | VARCHAR(20) | 账户ID，外键，唯一 |
| student_id | VARCHAR(20) | 学号 |
| university_id | VARCHAR(20) | 院校ID |
| college | VARCHAR(100) | 所属学院 |
| major | VARCHAR(100) | 所学专业 |
| degree | VARCHAR(20) | 学历 |
| graduation_year | INT | 毕业年份 |
| desire_city | VARCHAR(50) | 期望工作城市 |
| desire_industry | VARCHAR(50) | 期望行业 |
| desire_jd_type | VARCHAR(50) | 期望职类 |
| desire_salary_id | INT | 期望薪水ID |
| resume_url | VARCHAR(255) | 简历URL |
| skills | TEXT | 技能证书(JSON) |
| projects | TEXT | 项目经验(JSON) |
| certifications | TEXT | 证书(JSON) |

---

#### 3.2.2 用人单位表 (companies)

| 字段 | 类型 | 说明 |
|------|------|------|
| company_id | VARCHAR(20) | 企业标识，主键 |
| account_id | VARCHAR(20) | 账户ID，外键，唯一 |
| company_name | VARCHAR(100) | 公司名称 |
| company_type | VARCHAR(50) | 企业类型 |
| industry | VARCHAR(50) | 所属行业 |
| scale | VARCHAR(20) | 规模 |
| city | VARCHAR(50) | 总部城市 |
| verified | TINYINT | 认证状态(0=未认证 1=已认证) |

---

#### 3.2.3 岗位需求表 (job_descriptions)

| 字段 | 类型 | 说明 |
|------|------|------|
| jd_no | VARCHAR(20) | 职位代码，主键 |
| company_id | VARCHAR(20) | 企业ID，外键 |
| jd_title | VARCHAR(100) | 职位标题 |
| city | VARCHAR(50) | 工作城市 |
| min_salary | INT | 最低月薪 |
| max_salary | INT | 最高月薪 |
| require_nums | INT | 需求人数 |
| min_years | VARCHAR(10) | 工作年限 |
| min_edu_level | INT | 最低学历ID |
| job_description | TEXT | 职位描述 |
| status | TINYINT | 状态(0=下架 1=发布中) |
| view_count | INT | 浏览次数 |
| apply_count | INT | 申请次数 |

---

#### 3.2.4 岗位申请记录表 (job_applications)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| jd_no | VARCHAR(20) | 岗位代码，外键 |
| account_id | VARCHAR(20) | 学生账户ID |
| status | TINYINT | 状态(0=待处理 1=已查看 2=邀请面试 3=不合适 4=已录用) |
| applied_at | DATETIME | 申请时间 |

---

### 3.3 AI 服务相关表

#### 3.3.1 AI服务类型表 (ai_services)

| service_code | service_name | description |
|-------------|--------------|-------------|
| career_match | 就业方向匹配 | 根据学生档案推荐匹配的岗位 |
| salary_prediction | 薪资预测 | 预测学生可能的薪资范围 |
| skill_gap_analysis | 技能差距分析 | 分析技能与目标岗位的差距 |
| resume_optimization | 简历优化建议 | 优化简历提高通过率 |
| job_recommendation | 智能岗位推荐 | 根据企业需求推荐学生 |
| warning_student | 就业困难预警 | 预警潜在就业困难学生 |
| graduate_decision | 考研vs就业分析 | 分析考研与就业的ROI |

---

#### 3.3.2 AI分析请求记录表 (ai_analysis_requests)

| 字段 | 类型 | 说明 |
|------|------|------|
| request_id | INT | 主键 |
| service_id | INT | AI服务ID |
| account_id | VARCHAR(20) | 请求用户账户ID |
| input_data | TEXT | 输入数据(JSON) |
| output_data | TEXT | 输出结果(JSON) |
| status | VARCHAR(20) | 状态(pending/processing/completed/failed) |
| token_usage | INT | Token消耗 |
| cost | DECIMAL(10,2) | 费用 |
| created_at | DATETIME | 创建时间 |

---

#### 3.3.3 AI预警记录表 (ai_warnings)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| account_id | VARCHAR(20) | 被预警的学生账户ID |
| warning_type | VARCHAR(50) | 预警类型 |
| warning_level | VARCHAR(10) | 预警级别(red/yellow/green) |
| title | VARCHAR(100) | 预警标题 |
| content | TEXT | 预警内容 |
| suggestions | TEXT | 建议措施(JSON) |
| status | TINYINT | 状态(0=未处理 1=已处理 2=已忽略) |
| handled_by | VARCHAR(20) | 处理人 |

---

### 3.4 就业数据表

#### 3.4.1 就业报告表 (employment_reports)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| report_year | INT | 报告年份 |
| report_title | VARCHAR(200) | 报告标题 |
| source | VARCHAR(100) | 来源 |
| uploaded_by | VARCHAR(20) | 上传人账户ID |

---

#### 3.4.2 各省稀缺人才表 (scarce_talents)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| province | VARCHAR(20) | 省份 |
| industry | VARCHAR(50) | 行业 |
| occupation | VARCHAR(100) | 职业/岗位 |
| demand_rank | INT | 需求排名 |
| year | INT | 年份 |
| demand_index | DECIMAL(5,2) | 需求指数 |
| uploaded_by | VARCHAR(20) | 上传人账户ID |

---

#### 3.4.3 学院就业率表 (college_employment)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| college_name | VARCHAR(100) | 院系名称 |
| university_id | VARCHAR(20) | 院校ID |
| degree_type | VARCHAR(20) | 学历类型 |
| graduation_year | INT | 毕业年份 |
| graduate_nums | INT | 毕业人数 |
| employed_nums | INT | 就业数 |
| employment_rate | DECIMAL(5,2) | 毕业去向落实率 |
| further_study_nums | INT | 总升学人数 |
| uploaded_by | VARCHAR(20) | 上传人账户ID |

---

### 3.5 审计日志表

#### 3.5.1 数据操作审计日志表 (data_audit_logs)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| account_id | VARCHAR(20) | 操作人账户ID |
| action | VARCHAR(20) | 操作类型 |
| table_name | VARCHAR(50) | 操作的表名 |
| record_id | VARCHAR(50) | 操作的记录ID |
| old_value | TEXT | 修改前的值 |
| new_value | TEXT | 修改后的值 |
| ip_address | VARCHAR(50) | IP地址 |

---

## 四、权限控制说明

### 4.1 权限矩阵

| 资源 | 操作 | 学生 | 企业 | 学校 |
|------|------|------|------|------|
| 学生档案(自己) | 读/写 | ✓ | - | - |
| 学生档案(所有) | 读/写 | - | 部分 | ✓ |
| 岗位(自己) | 读/写/删 | - | ✓ | - |
| 岗位(所有) | 读 | ✓ | ✓ | ✓ |
| 岗位申请 | 读/写 | ✓ | ✓ | - |
| 就业报告 | 读/写 | - | - | ✓ |
| 学院就业率 | 读/写 | - | - | ✓ |
| 稀缺人才 | 读/写 | - | - | ✓ |
| AI服务 | 使用 | ✓ | ✓ | ✓ |

### 4.2 权限检查流程

```
用户请求 → 验证Token → 获取用户角色 → 查询角色权限 →
检查资源权限 → 允许/拒绝访问
```

---

## 五、AI 服务使用流程

### 5.1 学生使用 AI

```
1. 学生上传/完善档案 → student_profiles
2. 学生发起AI分析请求 → ai_analysis_requests
3. AI分析历史记录 → ai_analysis_requests
4. AI推荐结果 → ai_recommendations
5. 如有预警 → ai_warnings (推送给辅导员)
```

### 5.2 企业使用 AI

```
1. 企业发布岗位 → job_descriptions
2. 企业发起AI推荐请求 → ai_analysis_requests
3. AI推荐合适学生 → ai_recommendations
4. AI分析招聘效果 → ai_analysis_requests
```

### 5.3 学校使用 AI

```
1. 学校上传就业数据 → college_employment / scarce_talents
2. 学校发起综合分析请求 → ai_analysis_requests
3. AI生成决策建议 → ai_recommendations
4. AI自动生成预警 → ai_warnings
5. 辅导员处理预警
```

---

## 六、数据操作示例

### 6.1 创建用户并分配角色

```sql
-- 1. 创建学生账户
INSERT INTO accounts (account_id, username, password_hash, real_name, phone)
VALUES ('STU001', 'zhangsan', 'hash_value', '张三', '13800138000');

-- 2. 分配学生角色
INSERT INTO account_roles (account_id, role_id)
SELECT 'STU001', role_id FROM roles WHERE role_code = 'student';

-- 3. 创建学生档案
INSERT INTO student_profiles (
    account_id, student_id, university_id, college, major,
    degree, graduation_year, desire_city, desire_industry
) VALUES (
    'STU001', '2026001', 'U001', '计算机学院', '软件工程',
    '本科', 2026, '北京', '互联网/IT'
);
```

### 6.2 创建企业并发布岗位

```sql
-- 1. 创建企业账户
INSERT INTO accounts (account_id, username, password_hash, real_name)
VALUES ('CO001', 'alibaba_hr', 'hash_value', '阿里巴巴HR');

-- 2. 分配企业角色
INSERT INTO account_roles (account_id, role_id)
SELECT 'CO001', role_id FROM roles WHERE role_code = 'company_admin';

-- 3. 创建企业信息
INSERT INTO companies (company_id, account_id, company_name, industry, city, verified)
VALUES ('C001', 'CO001', '阿里巴巴', '互联网/IT', '杭州', 1);

-- 4. 发布岗位
INSERT INTO job_descriptions (
    jd_no, company_id, jd_title, city, min_salary, max_salary,
    min_edu_level, job_description
) VALUES (
    'JD001', 'C001', '后端开发工程师', '杭州', 15000, 25000,
    3, '负责XXX系统开发...'
);
```

### 6.3 学生申请岗位

```sql
INSERT INTO job_applications (jd_no, account_id, resume_url, cover_letter)
VALUES ('JD001', 'STU001', '/uploads/resume.pdf', '尊敬的HR...');
```

### 6.4 发起AI分析请求

```sql
-- 记录AI请求
INSERT INTO ai_analysis_requests (
    service_id, account_id, input_data, status
) VALUES (
    1, 'STU001',
    '{"major":"软件工程","degree":"本科","skills":["Java","Python"],"gpa":3.5}',
    'completed'
);

-- 记录AI返回结果
INSERT INTO ai_recommendations (
    request_id, recommend_type, target_id, target_name, match_score, reason
) VALUES (
    1, 'job', 'JD001', '后端开发工程师', 85.5,
    '专业对口，技能匹配度较高，有知名企业实习经历'
);
```

### 6.5 生成就业困难预警

```sql
INSERT INTO ai_warnings (
    account_id, warning_type, warning_level, title, content, suggestions
) VALUES (
    'STU001', 'skill_gap', 'yellow',
    '技能与市场需求存在差距',
    '您的技能主要集中在传统Web开发，但对目标岗位要求的高并发、分布式经验不足',
    '["建议学习Redis缓存优化", "补充微服务架构经验", "增加项目实战"]'
);
```

### 6.6 审计日志记录

```sql
INSERT INTO data_audit_logs (
    account_id, action, table_name, record_id, old_value, new_value, ip_address
) VALUES (
    'STU001', 'update', 'student_profiles', 'STU001',
    '{"desire_city":"上海"}',
    '{"desire_city":"北京"}',
    '192.168.1.100'
);
```

---

## 七、数据库导出与导入

### 7.1 导出数据库

```bash
# 导出完整数据库
mysqldump -u root -p employment_db > employment_db_v2.sql

# 压缩导出
mysqldump -u root -p employment_db | gzip > employment_db_v2.sql.gz

# 导出指定表
mysqldump -u root -p employment_db accounts roles student_profiles > users.sql
```

### 7.2 导入数据库

```bash
# 方法1：命令行
mysql -u root -p employment_db < employment_db_v2.sql

# 方法2：登录后执行
mysql -u root -p
USE employment_db;
SOURCE employment_db_v2.sql;
```

---

## 八、API 接口（新增）

### 8.1 账户与权限 API

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/register` | 注册账户 |
| POST | `/api/v1/auth/login` | 登录 |
| GET | `/api/v1/auth/me` | 获取当前用户信息 |
| GET | `/api/v1/roles` | 获取角色列表 |
| GET | `/api/v1/permissions` | 获取权限列表 |

### 8.2 学生档案 API

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/students/profile` | 获取我的档案 |
| PUT | `/api/v1/students/profile` | 更新我的档案 |
| GET | `/api/v1/students` | 获取所有学生列表(学校/企业) |
| GET | `/api/v1/students/{account_id}` | 获取学生详情(权限控制) |

### 8.3 企业与岗位 API

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/companies` | 获取企业列表 |
| POST | `/api/v1/companies` | 创建企业信息 |
| GET | `/api/v1/jobs` | 获取岗位列表 |
| POST | `/api/v1/jobs` | 发布岗位 |
| GET | `/api/v1/jobs/my` | 获取我的发布(企业) |
| POST | `/api/v1/jobs/apply` | 申请岗位(学生) |
| GET | `/api/v1/applications` | 获取申请记录 |

### 8.4 就业数据 API

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/college-employment/import` | 导入学院就业率 |
| GET | `/api/v1/college-employment` | 查询学院就业率 |
| POST | `/api/v1/scarce-talents/import` | 导入稀缺人才数据 |
| GET | `/api/v1/scarce-talents` | 查询稀缺人才 |
| POST | `/api/v1/reports/upload` | 上传就业报告 |
| GET | `/api/v1/reports` | 查询就业报告 |

### 8.5 AI 服务 API

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/ai/services` | 获取AI服务列表 |
| POST | `/api/v1/ai/analyze` | 发起AI分析请求 |
| GET | `/api/v1/ai/requests/{id}` | 获取分析结果 |
| GET | `/api/v1/ai/recommendations` | 获取推荐列表 |
| GET | `/api/v1/ai/warnings` | 获取预警列表 |
| PUT | `/api/v1/ai/warnings/{id}/handle` | 处理预警 |

---

## 九、常见问题

### 9.1 权限不足
检查账户是否分配了正确角色：
```sql
SELECT a.username, r.role_name
FROM accounts a
JOIN account_roles ar ON a.account_id = ar.account_id
JOIN roles r ON ar.role_id = r.role_id
WHERE a.account_id = 'STU001';
```

### 9.2 AI 服务调用失败
检查 AI 服务是否启用：
```sql
SELECT service_code, service_name, enabled FROM ai_services;
```

---

## 十、文件清单

| 文件路径 | 说明 |
|---------|------|
| `backend/database/init_database.sql` | 数据库初始化脚本 v2.0 |
| `backend/DATABASE.md` | 本文档 |

---

## 十一、更新记录

### v2.0 (2026-03-26)
- 新增统一账户表(accounts)，支持学生/学校/企业三方
- 新增角色与权限系统(roles, permissions)
- 新增学生详细档案表(student_profiles)
- 新增岗位申请记录表(job_applications)
- 新增AI服务相关表(ai_services, ai_analysis_requests, ai_recommendations, ai_warnings)
- 新增数据操作审计日志表(data_audit_logs)
- 完善就业数据表的上传人关联
