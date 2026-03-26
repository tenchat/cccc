# 数据库与 API 详细文档

## 大学生就业信息智能分析平台

---

## 一、数据库结构

### 1.1 学生表 (students)

| 字段 | 类型 | 允许空 | 默认值 | 说明 |
|------|------|--------|--------|------|
| id | INT | 否 | 自增 | 主键 |
| student_id | VARCHAR(20) | 否 | - | 学号，唯一索引 |
| name | VARCHAR(50) | 否 | - | 姓名 |
| college | VARCHAR(50) | 否 | - | 学院 |
| major | VARCHAR(50) | 否 | - | 专业 |
| grade | VARCHAR(10) | 否 | - | 届次（如 2026） |
| province | VARCHAR(20) | 否 | - | 生源省份 |
| gpa | DECIMAL(3,2) | 是 | NULL | GPA（0.00-4.00） |
| employment_status | TINYINT | 否 | 0 | 就业状态（见下表） |
| salary | INT | 是 | NULL | 起薪（元/月） |
| company | VARCHAR(100) | 是 | NULL | 就业公司 |
| position | VARCHAR(50) | 是 | NULL | 岗位 |
| skills | TEXT | 是 | NULL | 技能证书（JSON 数组格式） |
| internship | TEXT | 是 | NULL | 实习经历 |
| target_city | VARCHAR(50) | 是 | NULL | 目标城市 |
| created_at | DATETIME | 否 | 当前时间 | 创建时间 |
| updated_at | DATETIME | 否 | 当前时间 | 更新时间 |

### 1.2 就业状态枚举值

| 值 | 含义 |
|----|------|
| 0 | 待业 |
| 1 | 就业 |
| 2 | 升学 |
| 3 | 出国 |

### 1.3 学院与专业对应关系

| 学院 | 专业 |
|------|------|
| 计算机学院 | 计算机科学与技术、信息安全、物联网工程 |
| 信息工程学院 | 电子信息工程、通信工程、自动化 |
| 软件学院 | 软件工程、数据科学与大数据技术、人工智能 |
| 电子工程学院 | 电子科学与技术、微电子科学与工程 |
| 机械工程学院 | 机械设计制造及其自动化、材料成型及控制工程 |

---

## 二、数据库操作

### 2.1 创建数据库和表

```sql
-- 创建数据库
CREATE DATABASE employment_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE employment_db;

-- 创建学生表
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    college VARCHAR(50) NOT NULL COMMENT '学院',
    major VARCHAR(50) NOT NULL COMMENT '专业',
    grade VARCHAR(10) NOT NULL COMMENT '届次',
    province VARCHAR(20) NOT NULL COMMENT '生源省份',
    gpa DECIMAL(3,2) NULL COMMENT 'GPA',
    employment_status TINYINT NOT NULL DEFAULT 0 COMMENT '就业状态: 0待业 1就业 2升学 3出国',
    salary INT NULL COMMENT '起薪',
    company VARCHAR(100) NULL COMMENT '就业公司',
    position VARCHAR(50) NULL COMMENT '岗位',
    skills TEXT NULL COMMENT '技能证书(JSON)',
    internship TEXT NULL COMMENT '实习经历',
    target_city VARCHAR(50) NULL COMMENT '目标城市',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_college (college),
    INDEX idx_major (major),
    INDEX idx_grade (grade),
    INDEX idx_province (province),
    INDEX idx_employment_status (employment_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生信息表';
```

### 2.2 查看表结构

```sql
DESCRIBE students;
```

### 2.3 查看所有数据

```sql
SELECT * FROM students;
```

### 2.4 条件查询

```sql
-- 查询某个学院的待业学生
SELECT * FROM students WHERE college = '计算机学院' AND employment_status = 0;

-- 查询某个专业的就业学生
SELECT * FROM students WHERE major = '软件工程' AND employment_status = 1;

-- 查询某届学生
SELECT * FROM students WHERE grade = '2026';
```

### 2.5 统计查询

```sql
-- 统计总人数
SELECT COUNT(*) as total FROM students;

-- 统计各就业状态人数
SELECT
    SUM(CASE WHEN employment_status = 0 THEN 1 ELSE 0 END) as 待业,
    SUM(CASE WHEN employment_status = 1 THEN 1 ELSE 0 END) as 就业,
    SUM(CASE WHEN employment_status = 2 THEN 1 ELSE 0 END) as 升学,
    SUM(CASE WHEN employment_status = 3 THEN 1 ELSE 0 END) as 出国
FROM students;

-- 按学院统计
SELECT college, COUNT(*) as total,
    SUM(employment_status = 1) as employed
FROM students
GROUP BY college;

-- 统计平均薪资
SELECT AVG(salary) as avg_salary FROM students WHERE salary IS NOT NULL;
```

### 2.6 更新数据

```sql
-- 更新单个学生就业信息
UPDATE students
SET employment_status = 1,
    company = '阿里巴巴',
    position = '后端开发工程师',
    salary = 15000
WHERE student_id = '2026100123';

-- 批量更新待业学生状态
UPDATE students
SET employment_status = 1, company = '已就业', salary = 8000
WHERE employment_status = 0 AND grade = '2025';
```

### 2.7 删除数据

```sql
-- 删除单个学生
DELETE FROM students WHERE student_id = '2026100123';

-- 删除某届学生
DELETE FROM students WHERE grade = '2020';

-- 清空表（慎用）
TRUNCATE TABLE students;
```

---

## 三、API 详细文档

> Base URL: `http://localhost:8000`
>
> 所有 API 返回格式为 JSON
>
> API 文档: http://localhost:8000/docs

### 3.1 学生管理 API

#### 获取学生列表

```
GET /api/v1/students
```

**Query 参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| page_size | int | 否 | 20 | 每页数量（最大100） |
| college | string | 否 | - | 按学院筛选 |
| major | string | 否 | - | 按专业筛选 |
| province | string | 否 | - | 按省份筛选 |
| employment_status | string | 否 | - | 按就业状态筛选（0/1/2/3） |
| grade | string | 否 | - | 按届次筛选 |

**请求示例：**
```bash
# 获取第1页，每页10条
curl "http://localhost:8000/api/v1/students?page=1&page_size=10"

# 筛选计算机学院待业学生
curl "http://localhost:8000/api/v1/students?college=计算机学院&employment_status=0"

# 筛选2026届软件工程专业学生
curl "http://localhost:8000/api/v1/students?grade=2026&major=软件工程"
```

**响应示例：**
```json
{
  "total": 500,
  "page": 1,
  "page_size": 10,
  "items": [
    {
      "id": 1,
      "student_id": "202610123456",
      "name": "学生1",
      "college": "计算机学院",
      "major": "计算机科学与技术",
      "grade": "2026",
      "province": "北京",
      "gpa": 3.55,
      "employment_status": "1",
      "salary": 15000,
      "company": "阿里巴巴",
      "position": "后端开发工程师",
      "skills": "[\"Python\", \"Java\", \"SQL\"]",
      "internship": "XX公司实习3个月",
      "target_city": "北京",
      "created_at": "2026-03-26T10:00:00",
      "updated_at": "2026-03-26T10:00:00"
    }
  ]
}
```

---

#### 获取单个学生

```
GET /api/v1/students/{id}
```

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | int | 学生ID |

**请求示例：**
```bash
curl "http://localhost:8000/api/v1/students/1"
```

**响应示例：**
```json
{
  "id": 1,
  "student_id": "202610123456",
  "name": "学生1",
  "college": "计算机学院",
  "major": "计算机科学与技术",
  "grade": "2026",
  "province": "北京",
  "gpa": 3.55,
  "employment_status": "1",
  "salary": 15000,
  "company": "阿里巴巴",
  "position": "后端开发工程师",
  "skills": "[\"Python\", \"Java\", \"SQL\"]",
  "internship": "XX公司实习3个月",
  "target_city": "北京",
  "created_at": "2026-03-26T10:00:00",
  "updated_at": "2026-03-26T10:00:00"
}
```

---

#### 新增学生

```
POST /api/v1/students
```

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| student_id | string | 是 | 学号（唯一） |
| name | string | 是 | 姓名 |
| college | string | 是 | 学院 |
| major | string | 是 | 专业 |
| grade | string | 是 | 届次 |
| province | string | 是 | 生源省份 |
| gpa | float | 否 | GPA（0-4） |
| employment_status | string | 否 | 就业状态（默认"0"） |
| salary | int | 否 | 起薪 |
| company | string | 否 | 就业公司 |
| position | string | 否 | 岗位 |
| skills | string | 否 | 技能证书（JSON数组格式字符串） |
| internship | string | 否 | 实习经历 |
| target_city | string | 否 | 目标城市 |

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/students" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "2026109999",
    "name": "张三",
    "college": "软件学院",
    "major": "软件工程",
    "grade": "2026",
    "province": "上海",
    "gpa": 3.8,
    "employment_status": "0",
    "skills": "[\"Python\", \"JavaScript\", \"Vue\"]",
    "target_city": "上海"
  }'
```

**响应示例：**
```json
{
  "id": 101,
  "student_id": "2026109999",
  "name": "张三",
  "college": "软件学院",
  "major": "软件工程",
  "grade": "2026",
  "province": "上海",
  "gpa": 3.8,
  "employment_status": "0",
  "salary": null,
  "company": null,
  "position": null,
  "skills": "[\"Python\", \"JavaScript\", \"Vue\"]",
  "internship": null,
  "target_city": "上海",
  "created_at": "2026-03-26T10:30:00",
  "updated_at": "2026-03-26T10:30:00"
}
```

**错误示例（学号重复）：**
```json
{
  "detail": "学号已存在"
}
```

---

#### 更新学生

```
PUT /api/v1/students/{id}
```

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | int | 学生ID |

**请求体：**（只传需要更新的字段）

```bash
# 更新学生就业状态
curl -X PUT "http://localhost:8000/api/v1/students/101" \
  -H "Content-Type: application/json" \
  -d '{
    "employment_status": "1",
    "company": "腾讯",
    "position": "前端开发工程师",
    "salary": 18000
  }'
```

**响应示例：**
```json
{
  "id": 101,
  "student_id": "2026109999",
  "name": "张三",
  "college": "软件学院",
  "major": "软件工程",
  "grade": "2026",
  "province": "上海",
  "gpa": 3.8,
  "employment_status": "1",
  "salary": 18000,
  "company": "腾讯",
  "position": "前端开发工程师",
  "skills": "[\"Python\", \"JavaScript\", \"Vue\"]",
  "internship": null,
  "target_city": "上海",
  "created_at": "2026-03-26T10:30:00",
  "updated_at": "2026-03-26T10:35:00"
}
```

---

#### 删除学生

```
DELETE /api/v1/students/{id}
```

**请求示例：**
```bash
curl -X DELETE "http://localhost:8000/api/v1/students/101"
```

**响应：** 无内容（状态码 204）

**错误示例（学生不存在）：**
```json
{
  "detail": "学生不存在"
}
```

---

### 3.2 批量导入 API

#### 批量导入学生（CSV/Excel）

```
POST /api/v1/students/import
```

**请求方式：** `multipart/form-data`

**表单字段：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | CSV 或 Excel 文件 |

**CSV 格式要求：**

| 列名 | 必填 | 说明 |
|------|------|------|
| student_id | 是 | 学号 |
| name | 是 | 姓名 |
| college | 是 | 学院 |
| major | 是 | 专业 |
| grade | 是 | 届次 |
| province | 是 | 生源省份 |
| gpa | 否 | GPA |
| employment_status | 否 | 就业状态（默认0） |
| salary | 否 | 起薪 |
| company | 否 | 就业公司 |
| position | 否 | 岗位 |
| skills | 否 | 技能证书（逗号分隔） |
| internship | 否 | 实习经历 |
| target_city | 否 | 目标城市 |

**CSV 示例：**
```csv
student_id,name,college,major,grade,province,gpa,employment_status,salary,company,position,skills,target_city
2026100001,李四,计算机学院,计算机科学与技术,2026,北京,3.5,1,15000,阿里巴巴,后端开发,Python;Java;SQL,北京
2026100002,王五,软件学院,软件工程,2026,上海,3.8,0,,,Python;Vue,上海
2026100003,赵六,信息工程学院,通信工程,2026,广东,3.2,2,,,通信原理,深圳
```

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/students/import" \
  -F "file=@students.csv"
```

**响应示例：**
```json
{
  "total": 3,
  "success": 3,
  "failed": 0,
  "errors": []
}
```

**部分成功响应（示例）：**
```json
{
  "total": 3,
  "success": 2,
  "failed": 1,
  "errors": [
    {
      "row": 2,
      "student_id": "2026100001",
      "error": "学号已存在"
    }
  ]
}
```

---

### 3.3 统计 API

#### 统计汇总

```
GET /api/v1/statistics/summary
```

**请求示例：**
```bash
curl "http://localhost:8000/api/v1/statistics/summary"
```

**响应示例：**
```json
{
  "total": 500,
  "employed": 302,
  "unemployed": 75,
  "further_study": 75,
  "abroad": 48,
  "employment_rate": 60.4
}
```

---

#### 按学院统计

```
GET /api/v1/statistics/by-college
```

**响应示例：**
```json
[
  {"college": "计算机学院", "total": 120, "employed": 75},
  {"college": "信息工程学院", "total": 100, "employed": 60},
  {"college": "软件学院", "total": 130, "employed": 85},
  {"college": "电子工程学院", "total": 80, "employed": 45},
  {"college": "机械工程学院", "total": 70, "employed": 37}
]
```

---

#### 按专业统计

```
GET /api/v1/statistics/by-major
```

**响应示例：**
```json
[
  {"major": "计算机科学与技术", "college": "计算机学院", "total": 50, "employed": 32},
  {"major": "软件工程", "college": "软件学院", "total": 80, "employed": 55}
]
```

---

#### 按省份统计

```
GET /api/v1/statistics/by-province
```

**响应示例：**
```json
[
  {"province": "北京", "total": 50},
  {"province": "上海", "total": 45},
  {"province": "广东", "total": 60},
  {"province": "浙江", "total": 40}
]
```

---

### 3.4 AI 就业指导 API

#### 就业竞争力画像

```
POST /api/v1/ai/employment-profile
```

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/employment-profile" \
  -H "Content-Type: application/json" \
  -d '{
    "major": "软件工程",
    "gpa": 3.5,
    "skills": ["Python", "Java", "SQL", "Vue"],
    "target_city": "上海",
    "internship": "在腾讯实习3个月"
  }'
```

**响应示例：**
```json
{
  "score": 78,
  "professional_match": 82,
  "skill_match": 75,
  "location_demand": 80,
  "salary_expectation": 75,
  "strengths": "专业基础扎实，有知名企业实习经历",
  "weaknesses": "缺乏大型分布式系统开发经验",
  "suggestions": "建议加强分布式系统学习，参与开源项目积累经验"
}
```

---

#### 岗位匹配推荐

```
POST /api/v1/ai/job-recommendation
```

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/job-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "major": "软件工程",
    "skills": ["Python", "Java", "SQL"],
    "target_city": "北京",
    "salary_expectation": 15000
  }'
```

**响应示例：**
```json
{
  "recommendations": [
    {
      "title": "后端开发工程师",
      "company_type": "大公司",
      "match_score": 85,
      "match_reasons": "专业对口，技能匹配度较高",
      "skill_gaps": "需要加强微服务架构经验",
      "estimated_salary": "15000-25000元/月"
    }
  ]
}
```

---

#### 技能提升路径

```
POST /api/v1/ai/skill-path
```

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/skill-path" \
  -H "Content-Type: application/json" \
  -d '{
    "current_skills": ["Python", "Java", "SQL"],
    "target_position": "资深后端开发工程师"
  }'
```

---

#### 就业困难预警

```
POST /api/v1/ai/warning
```

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/warning" \
  -H "Content-Type: application/json" \
  -d '{
    "major": "软件工程",
    "gpa": 2.8,
    "employment_status": 0,
    "target_city": "北京",
    "resume_count": 5
  }'
```

---

#### 简历关键词优化

```
POST /api/v1/ai/resume-analysis
```

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/resume-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "毕业于XX大学软件工程专业，熟悉Python和Java开发...",
    "target_position": "后端开发工程师"
  }'
```

---

#### 考研 vs 就业决策

```
POST /api/v1/ai/graduate-vs-job
```

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/graduate-vs-job" \
  -H "Content-Type: application/json" \
  -d '{
    "target_city": "上海",
    "expected_salary": 15000,
    "preparation_time": "6个月"
  }'
```

---

## 四、Python SDK / Requests 调用示例

### 4.1 安装依赖

```bash
pip install requests
```

### 4.2 学生 CRUD 操作

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 获取学生列表
def get_students(page=1, page_size=20, **filters):
    params = {"page": page, "page_size": page_size, **filters}
    response = requests.get(f"{BASE_URL}/students", params=params)
    return response.json()

# 获取单个学生
def get_student(student_id):
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    return response.json()

# 新增学生
def create_student(data):
    response = requests.post(f"{BASE_URL}/students", json=data)
    return response.json()

# 更新学生
def update_student(student_id, data):
    response = requests.put(f"{BASE_URL}/students/{student_id}", json=data)
    return response.json()

# 删除学生
def delete_student(student_id):
    response = requests.delete(f"{BASE_URL}/students/{student_id}")
    return response.status_code == 204

# 统计汇总
def get_summary():
    response = requests.get(f"{BASE_URL}/statistics/summary")
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 新增学生
    new_student = {
        "student_id": "2026999999",
        "name": "测试学生",
        "college": "计算机学院",
        "major": "计算机科学与技术",
        "grade": "2026",
        "province": "北京",
        "gpa": 3.5,
        "employment_status": "0"
    }
    result = create_student(new_student)
    print(f"新增学生: {result['name']}, ID: {result['id']}")

    # 获取学生列表
    students = get_students(page=1, college="计算机学院")
    print(f"计算机学院学生总数: {students['total']}")

    # 更新学生就业状态
    update_student(result['id'], {
        "employment_status": "1",
        "company": "字节跳动",
        "position": "后端开发",
        "salary": 20000
    })

    # 删除学生
    delete_student(result['id'])
    print("学生已删除")
```

### 4.3 批量导入 CSV

```python
import requests

# 批量导入学生
def import_students(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            "http://localhost:8000/api/v1/students/import",
            files=files
        )
    return response.json()

# 使用示例
result = import_students("students.csv")
print(f"导入完成: 成功{result['success']}条, 失败{result['failed']}条")
if result['errors']:
    print(f"错误详情: {result['errors']}")
```

---

## 五、常见错误码

| HTTP 状态码 | 说明 |
|-------------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无内容返回） |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 422 | 数据验证失败 |
| 500 | 服务器内部错误 |
