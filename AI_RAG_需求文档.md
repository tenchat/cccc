# AI大模型接入需求文档

> 大学生就业信息智能分析平台 - AI模块技术方案

---

## 一、整体架构

### 1.1 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户请求层                               │
│    学生端 │ 辅导员端 │ 管理端 │ 企业端                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API网关层 (FastAPI)                         │
│         /ai/employment-profile │ /ai/job-recommendation         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI服务层                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ MiniMax API │  │ 本地知识库  │  │ RAG引擎     │              │
│  │ (云端模型)   │  │ (Vector DB) │  │ (检索+生成) │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       数据层                                     │
│   MySQL数据库  │  Redis缓存  │  向量数据库                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、技术栈

### 2.1 云端大模型

| 服务商 | 模型 | 用途 | 特点 |
|--------|------|------|------|
| **MiniMax** | MiniMax-Text-01 | 主要AI服务 | 符合4C大赛规范，中文理解强 |
| **DeepSeek** | DeepSeek-V3 | 备选AI服务 | 性价比高 |
| **硅基流动** | Qwen/Qwen2.5 | 托管部署 | 国内可用，API兼容OpenAI |

### 2.2 本地数据存储

| 类型 | 技术 | 用途 |
|------|------|------|
| 关系型数据库 | MySQL 8.0 | 学生档案、岗位信息、就业率数据 |
| 缓存 | Redis | 会话缓存、Token管理、热点数据 |
| 向量数据库 | Milvus / Qdrant / ChromaDB | 文本向量存储、相似度检索 |

### 2.3 RAG相关

| 技术 | 用途 |
|------|------|
| **LangChain** | RAG流程编排、文档分割、链式调用 |
| **LangChain-rag** | 文档检索、增强生成 |
| **Sentence-Transformers** | 文本向量化 |
| **BM25** | 关键词检索（补充向量检索） |
| **Redis Vector** | 轻量级向量检索（可选） |

### 2.4 依赖包

```
# 核心依赖
fastapi==0.109.0
uvicorn==0.27.0

# AI相关
httpx==0.27.0          # 异步HTTP客户端
langchain==0.1.0       # RAG框架
langchain-community==0.0.10  # 社区集成
sentence-transformers==2.2.2  # 文本向量化
numpy==1.26.3          # 数值计算
scikit-learn==1.3.0    # 机器学习工具

# 向量数据库（选择其一）
# pymilvus==2.3.0     # Milvus客户端
# qdrant-client==1.7.0 # Qdrant客户端
chromadb==0.4.18        # ChromaDB（轻量级，推荐）

# 文本处理
jieba==0.42.1          # 中文分词
pdfplumber==0.10.3     # PDF解析
python-docx==1.1.0    # Word文档解析

# 缓存
redis==5.0.1
```

---

## 三、数据库数据接口

### 3.1 学生档案数据

```sql
-- 学生画像数据
SELECT
    sp.student_id,
    sp.college,
    sp.major,
    sp.degree,
    sp.graduation_year,
    sp.desire_city,
    sp.desire_industry,
    sp.desire_jd_type,
    sp.desire_salary_id,
    sp.cur_industry,
    sp.cur_salary,
    sp.experience,
    a.real_name
FROM student_profiles sp
JOIN accounts a ON sp.account_id = a.account_id
WHERE sp.account_id = :account_id
```

### 3.2 就业统计数据

```sql
-- 就业概况统计
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN employment_status = 1 THEN 1 ELSE 0 END) as employed,
    SUM(CASE WHEN employment_status = 0 THEN 1 ELSE 0 END) as unemployed,
    SUM(CASE WHEN employment_status = 2 THEN 1 ELSE 0 END) as further_study,
    SUM(CASE WHEN employment_status = 3 THEN 1 ELSE 0 END) as abroad
FROM student_profiles
WHERE university_id = :university_id

-- 学院就业率
SELECT
    college,
    COUNT(*) as total,
    SUM(employment_status = 1) as employed,
    ROUND(SUM(employment_status = 1) / COUNT(*) * 100, 2) as rate
FROM student_profiles
GROUP BY college
```

### 3.3 岗位需求数据

```sql
-- 岗位技能要求
SELECT
    jd_no,
    jd_title,
    industry,
    city,
    min_salary,
    max_salary,
    min_edu_level,
    min_years,
    key_words,
    job_description
FROM job_descriptions
WHERE status = 1
```

### 3.4 学院就业率数据

```sql
-- 历年就业率
SELECT
    college_name,
    graduation_year,
    graduate_nums,
    employed_nums,
    employment_rate,
    further_study_rate,
    domestic_study_rate,
    overseas_study_rate
FROM college_employment
WHERE university_id = :university_id
ORDER BY graduation_year DESC
```

---

## 四、云端AI接口用法

### 4.1 MiniMax API

```python
# app/services/ai_service.py
import httpx
from typing import List, Dict, Any

class MiniMaxAI:
    """MiniMax AI 客户端"""

    def __init__(self, api_key: str, base_url: str = "https://api.minimaxi.com/v1"):
        self.api_key = api_key
        self.base_url = base_url

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "MiniMax-Text-01",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """调用 MiniMax Chat API"""
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
```

### 4.2 就业竞争力画像接口

```python
# app/api/v1/ai.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.ai_service import MiniMaxAI
from app.core.config import get_settings

router = APIRouter(prefix="/ai", tags=["AI就业指导"])

class EmploymentProfileRequest(BaseModel):
    major: str = Field(..., description="专业")
    gpa: float = Field(..., ge=0, le=4.0, description="GPA")
    skills: List[str] = Field(default=[], description="技能列表")
    target_city: str = Field(..., description="目标城市")
    internship: Optional[str] = Field(None, description="实习经历")

@router.post("/employment-profile")
async def employment_profile(request: EmploymentProfileRequest):
    """
    生成就业竞争力画像

    结合本地数据库的学生画像数据和云端AI分析
    """
    settings = get_settings()
    ai = MiniMaxAI(settings.MINIMAX_API_KEY, settings.MINIMAX_BASE_URL)

    # 构建提示词
    prompt = f"""分析以下学生的就业竞争力：

    专业: {request.major}
    GPA: {request.gpa}
    技能: {', '.join(request.skills) if request.skills else '无'}
    目标城市: {request.target_city}
    实习经历: {request.internship or '无'}

    请以JSON格式返回分析结果：
    {{
        "score": 就业竞争力评分(0-100),
        "professional_match": 专业匹配度(0-100),
        "skill_match": 技能契合度(0-100),
        "location_demand": 地区供需比(0-100),
        "salary_expectation": 薪资预期合理性(0-100),
        "strengths": 优势分析,
        "weaknesses": 劣势分析,
        "suggestions": 改进建议
    }}
    """

    messages = [{"role": "user", "content": prompt}]
    response = await ai.chat(messages)

    # 解析JSON响应
    import json
    try:
        result = json.loads(response)
    except:
        result = {"error": "解析失败", "raw": response}

    return result
```

---

## 五、RAG增强实现

### 5.1 RAG流程

```
用户请求 → 意图识别 → 查询改写
                        ↓
              ┌─────────┴─────────┐
              ↓                   ↓
        本地知识库检索        向量数据库检索
        (关键词/BM25)         (语义相似度)
              ↓                   ↓
              └─────────┬─────────┘
                        ↓
                  相关文档片段
                        ↓
                  上下文构建
              (系统提示 + 检索内容 + 用户问题)
                        ↓
                  云端大模型生成
                        ↓
                      响应结果
```

### 5.2 本地知识库构建

```python
# app/services/rag/knowledge_base.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from typing import List
import chromadb

class KnowledgeBase:
    """本地知识库管理"""

    def __init__(self, persist_directory: str = "./data/vector_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="shibing624/text2vec-base-chinese",
            model_kwargs={'device': 'cpu'}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n", "。", "！", "？", "，", "、", ""]
        )

    def load_employment_reports(self, db: Session):
        """加载就业报告到知识库"""
        from app.models import EmploymentReport

        reports = db.query(EmploymentReport).all()
        documents = []

        for report in reports:
            text = f"""
            报告标题：{report.report_title}
            年份：{report.report_year}
            来源：{report.source}
            内容摘要：{report.summary}
            """
            documents.append(text)

        return documents

    def load_scarce_talents(self, db: Session):
        """加载稀缺人才数据"""
        from app.models import ScarceTalent

        talents = db.query(ScarceTalent).all()
        documents = []

        for talent in talents:
            text = f"""
            省份：{talent.province}
            行业：{talent.industry}
            紧缺岗位：{talent.occupation}
            需求排名：{talent.demand_rank}
            年份：{talent.year}
            平均薪资：{talent.avg_salary}元/月
            需求指数：{talent.demand_index}
            """
            documents.append(text)

        return documents

    def load_college_employment(self, db: Session):
        """加载学院就业率数据"""
        from app.models import CollegeEmployment

        data = db.query(CollegeEmployment).all()
        documents = []

        for item in data:
            text = f"""
            院系：{item.college_name}
            学历类型：{item.degree_type}
            毕业年份：{item.graduation_year}
            毕业人数：{item.graduate_nums}
            就业人数：{item.employed_nums}
            就业率：{item.employment_rate}%
            升学率：{item.further_study_rate}%
            境内升学：{item.domestic_study_nums}人({item.domestic_study_rate}%)
            境外升学：{item.overseas_study_nums}人({item.overseas_study_rate}%)
            """
            documents.append(text)

        return documents

    def build_vectorstore(self, documents: List[str], collection_name: str):
        """构建向量数据库"""
        texts = self.text_splitter.split_text("\n".join(documents))

        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=collection_name
        )

        vectorstore.persist()
        return vectorstore

    def retrieve(self, query: str, collection_name: str, k: int = 5) -> List[str]:
        """检索相关文档"""
        vectorstore = Chroma(
            client=chromadb.PersistentClient(path=self.persist_directory),
            collection_name=collection_name,
            embedding_function=self.embeddings
        )

        results = vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
```

### 5.3 RAG增强的就业画像

```python
# app/services/rag/enhanced_profile.py

from typing import List, Dict, Any
from app.services.ai_service import MiniMaxAI
from app.services.rag.knowledge_base import KnowledgeBase

class RAGEnhancedProfile:
    """RAG增强的就业竞争力分析"""

    def __init__(self, db: Session):
        self.db = db
        self.kb = KnowledgeBase()
        self.ai = MiniMaxAI()

    async def generate_profile(
        self,
        student_data: Dict[str, Any],
        local_context: bool = True
    ) -> Dict[str, Any]:
        """
        生成就业竞争力画像（带RAG增强）

        Args:
            student_data: 学生基本信息
            local_context: 是否启用本地知识库增强
        """
        # 1. 构建系统提示词
        system_prompt = """你是一个专业的就业分析师，拥有丰富的高校就业数据知识。
        请根据学生的信息和相关就业数据，分析其就业竞争力。"""

        # 2. 如果启用RAG，检索相关本地数据
        context_docs = []
        if local_context:
            # 检索该专业的就业数据
            major_query = f"{student_data['major']} 就业情况 薪资"
            context_docs = self.kb.retrieve(major_query, "colleges", k=3)

            # 检索目标城市的岗位需求
            city_query = f"{student_data['target_city']} 岗位需求 薪资"
            city_docs = self.kb.retrieve(city_query, "jobs", k=3)
            context_docs.extend(city_docs)

        # 3. 构建用户问题
        user_prompt = f"""学生信息：
        - 专业：{student_data['major']}
        - GPA：{student_data['gpa']}
        - 技能：{', '.join(student_data.get('skills', []))}
        - 目标城市：{student_data['target_city']}
        - 实习经历：{student_data.get('internship', '无')}

        {'相关就业数据：\n' + '\n'.join(context_docs) if context_docs else ''}

        请分析该学生的就业竞争力，以JSON格式返回："""

        # 4. 调用AI生成
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = await self.ai.chat(messages)

        # 5. 解析并返回结果
        import json
        try:
            result = json.loads(response)
            result["context_used"] = len(context_docs) > 0
            return result
        except:
            return {"error": "解析失败", "raw": response}
```

### 5.4 智能问答（RAG问答）

```python
# app/services/rag/qa_system.py

class EmploymentQA:
    """就业信息智能问答系统"""

    def __init__(self, db: Session):
        self.db = db
        self.kb = KnowledgeBase()
        self.ai = MiniMaxAI()

    async def ask(
        self,
        question: str,
        user_role: str = "student",
        university_id: str = None
    ) -> Dict[str, Any]:
        """
        智能问答

        Args:
            question: 用户问题
            user_role: 用户角色（student/counselor/admin）
            university_id: 学校ID（用于过滤数据）
        """
        # 1. 意图识别
        intent = self._identify_intent(question)

        # 2. 根据意图构建查询
        queries = self._build_queries(question, intent, university_id)

        # 3. 多路检索
        all_docs = []
        for query, collection in queries:
            docs = self.kb.retrieve(query, collection, k=5)
            all_docs.extend(docs)

        # 4. 去重和排序
        unique_docs = self._deduplicate(all_docs)

        # 5. 构建提示词
        prompt = self._build_prompt(question, unique_docs, user_role)

        # 6. 调用AI
        messages = [{"role": "user", "content": prompt}]
        response = await self.ai.chat(messages)

        return {
            "question": question,
            "answer": response,
            "sources": unique_docs[:3],  # 返回参考来源
            "intent": intent
        }

    def _identify_intent(self, question: str) -> str:
        """识别问题意图"""
        keywords = {
            "就业率": ["就业率", "找工作", "签约"],
            "薪资": ["薪资", "工资", "待遇", "起薪"],
            "升学": ["考研", "升学", "保研", "留学"],
            "岗位": ["岗位", "职位", "招聘", "JD"],
            "行业": ["行业", "前景", "发展"],
            "技能": ["技能", "能力", "要求"]
        }

        for intent, words in keywords.items():
            if any(w in question for w in words):
                return intent
        return "general"

    def _build_queries(
        self,
        question: str,
        intent: str,
        university_id: str
    ) -> List[tuple]:
        """构建检索查询"""
        queries = []

        if intent == "就业率":
            queries.append((f"就业率 {university_id}", "colleges"))
            queries.append(("全国高校就业率", "reports"))
        elif intent == "薪资":
            queries.append((question, "jobs"))
            queries.append(("行业薪资水平", "talents"))
        elif intent == "岗位":
            queries.append((question, "jobs"))
        elif intent == "升学":
            queries.append((f"升学率 {university_id}", "colleges"))
        else:
            queries.append((question, "colleges"))
            queries.append((question, "jobs"))

        return queries

    def _build_prompt(
        self,
        question: str,
        context_docs: List[str],
        user_role: str
    ) -> str:
        """构建提示词"""
        role_prompts = {
            "student": "你正在为一名大学生解答就业相关问题。",
            "counselor": "你正在为一名辅导员解答就业数据相关问题。",
            "admin": "你正在为学校管理层解答就业统计相关问题。"
        }

        context = "\n\n".join(context_docs) if context_docs else "无相关数据"

        prompt = f"""你是大学生就业信息分析专家。{role_prompts.get(user_role, '')}

参考信息：
{context}

用户问题：{question}

请根据参考信息回答用户问题。如果参考信息不足，请基于你的知识给出合理回答。
"""
        return prompt
```

---

## 六、API接口汇总

### 6.1 AI服务接口

| 方法 | 端点 | 说明 | RAG增强 |
|------|------|------|---------|
| POST | `/api/v1/ai/employment-profile` | 就业竞争力画像 | ✅ 支持 |
| POST | `/api/v1/ai/job-recommendation` | 岗位匹配推荐 | ✅ 支持 |
| POST | `/api/v1/ai/skill-path` | 技能提升路径 | ❌ |
| POST | `/api/v1/ai/warning` | 就业困难预警 | ✅ 支持 |
| POST | `/api/v1/ai/resume-analysis` | 简历关键词优化 | ❌ |
| POST | `/api/v1/ai/graduate-vs-job` | 考研vs就业决策 | ✅ 支持 |
| POST | `/api/v1/ai/qa` | 智能问答 | ✅ 必须 |

### 6.2 知识库管理接口

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/knowledge/rebuild` | 重建知识库 |
| GET | `/api/v1/knowledge/status` | 知识库状态 |
| POST | `/api/v1/knowledge/add` | 添加文档 |
| DELETE | `/api/v1/knowledge/clear` | 清除知识库 |

---

## 七、数据流示例

### 7.1 就业画像分析流程

```
1. 学生提交请求
   POST /api/v1/ai/employment-profile
   {
     "major": "软件工程",
     "gpa": 3.5,
     "skills": ["Python", "Java", "SQL"],
     "target_city": "上海"
   }

2. 后端处理
   ├─ 2.1 查询本地数据库
   │     SELECT * FROM student_profiles WHERE major='软件工程'
   │     → 获取该专业就业率、平均薪资等统计数据
   │
   ├─ 2.2 RAG检索
   │     向量数据库检索"软件工程 上海 就业"
   │     → 获取相关就业报告片段、岗位需求片段
   │
   └─ 2.3 构建增强提示词
         [系统提示] + [本地统计] + [RAG检索结果] + [用户问题]

3. 调用云端AI
   POST https://api.minimaxi.com/v1/chat/completions
   {
     "model": "MiniMax-Text-01",
     "messages": [
       {"role": "system", "content": "你是就业分析师..."},
       {"role": "user", "content": "学生信息：\n本地数据：\n就业报告片段：\n用户问题："}
     ]
   }

4. 返回结果
   {
     "score": 78,
     "professional_match": 82,
     "skill_match": 75,
     "context_used": true,
     "sources": ["2024年高校就业报告-上海篇", "上海软件岗位需求分析"]
   }
```

---

## 八、部署建议

### 8.1 开发环境

```bash
# 1. 安装依赖
pip install langchain langchain-community sentence-transformers
pip install chromadb jieba

# 2. 下载向量化模型（首次运行自动下载）
# shibing624/text2vec-base-chinese 约500MB
```

### 8.2 向量化模型选择

| 模型 | 大小 | 适用场景 | 推荐度 |
|------|------|----------|--------|
| shibing624/text2vec-base-chinese | ~500MB | 通用中文语义 | ⭐⭐⭐⭐⭐ |
| bert-base-chinese | ~400MB | 通用语义 | ⭐⭐⭐⭐ |
| moka-ai/m3e-base | ~500MB | 中文嵌入 | ⭐⭐⭐⭐ |
| text2vec | ~300MB | 轻量级 | ⭐⭐⭐ |

### 8.3 性能优化

- 向量数据库持久化到磁盘，加速重启
- 热门查询结果Redis缓存
- 异步构建知识库，不阻塞主服务
- 模型量化减少内存占用

---

## 九、文件结构

```
backend/app/
├── services/
│   ├── ai_service.py           # 云端AI客户端
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── knowledge_base.py   # 知识库管理
│   │   ├── embeddings.py       # 向量化处理
│   │   ├── retriever.py        # 检索器
│   │   └── enhanced_profile.py # RAG增强分析
│   └── qa_system.py            # 智能问答
├── api/v1/
│   └── ai.py                   # AI接口路由
└── core/
    └── config.py               # 配置（含API Key）
```

---

## 十、总结

本方案实现：
1. **云端AI**：MiniMax API 提供基础生成能力
2. **本地数据**：MySQL数据库提供学生画像、就业统计等结构化数据
3. **RAG增强**：向量数据库存储就业报告等文档，实现检索增强生成
4. **混合架构**：云端AI + 本地数据 + RAG = 更准确的AI分析

关键优势：
- 学生档案、岗位需求等敏感数据保存在本地
- RAG减少AI幻觉，提高回答准确性
- 支持上下文理解，给出个性化建议
- 可扩展：后续可接入更多数据源
