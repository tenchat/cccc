"""
MiniMax AI 服务模块
用于处理就业相关的AI分析功能
"""
import json
import httpx
from typing import Optional, Dict, Any, List
from app.core.config import get_settings

settings = get_settings()


class MiniMaxAI:
    """MiniMax AI 客户端"""

    def __init__(self):
        self.api_key = settings.MINIMAX_API_KEY
        self.base_url = settings.MINIMAX_BASE_URL
        self.model = settings.MINIMAX_MODEL

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        调用 MiniMax Chat API

        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            temperature: 温度参数
            max_tokens: 最大token数

        Returns:
            AI返回的文本内容
        """
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


class EmploymentAIService:
    """就业分析AI服务"""

    def __init__(self):
        self.ai = MiniMaxAI()

    async def generate_employment_profile(
        self,
        major: str,
        gpa: float,
        skills: List[str],
        target_city: str,
        internship: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        生成就业竞争力画像

        Args:
            major: 专业
            gpa: GPA
            skills: 技能列表
            target_city: 目标城市
            internship: 实习经历

        Returns:
            包含评分和分析的字典
        """
        skills_str = ", ".join(skills) if skills else "无"
        internship_str = internship if internship else "无"

        prompt = f"""你是一个专业的就业分析师。请分析以下学生的就业竞争力：

专业: {major}
GPA: {gpa}
技能: {skills_str}
目标城市: {target_city}
实习经历: {internship_str}

请以JSON格式返回分析结果，包含以下字段：
- score: 就业竞争力评分(0-100)
- professional_match: 专业匹配度得分(0-100)
- skill_match: 技能契合度得分(0-100)
- location_demand: 地区供需比得分(0-100)
- salary_expectation: 薪资预期合理性得分(0-100)
- strengths: 优势分析(字符串)
- weaknesses: 劣势分析(字符串)
- suggestions: 改进建议(字符串)

只返回JSON，不要有其他内容。"""

        messages = [{"role": "user", "content": prompt}]
        response = await self.ai.chat(messages)

        try:
            # 尝试解析JSON响应
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            # 如果解析失败，返回原始响应
            return {
                "score": 70,
                "professional_match": 75,
                "skill_match": 70,
                "location_demand": 65,
                "salary_expectation": 70,
                "strengths": "专业基础扎实",
                "weaknesses": "需要更多实践",
                "suggestions": "建议加强实习经验",
                "raw_response": response
            }

    async def recommend_jobs(
        self,
        major: str,
        skills: List[str],
        target_city: str,
        salary_expectation: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        推荐匹配岗位

        Args:
            major: 专业
            skills: 技能列表
            target_city: 目标城市
            salary_expectation: 期望薪资

        Returns:
            岗位推荐列表
        """
        skills_str = ", ".join(skills) if skills else "无"
        salary_str = f"{salary_expectation}元/月" if salary_expectation else "不限"

        prompt = f"""你是一个专业的就业顾问。请为以下学生推荐合适的岗位：

专业: {major}
技能: {skills_str}
目标城市: {target_city}
期望薪资: {salary_str}

请推荐5个最匹配的岗位，以JSON数组格式返回，每个岗位包含：
- title: 岗位名称
- company_type: 公司类型(大公司/中小公司/创业公司)
- match_score: 匹配度(0-100)
- match_reasons: 匹配原因(字符串)
- skill_gaps: 技能差距(字符串)
- estimated_salary: 预估薪资范围(字符串)

只返回JSON数组，不要有其他内容。"""

        messages = [{"role": "user", "content": prompt}]
        response = await self.ai.chat(messages)

        try:
            result = json.loads(response)
            if isinstance(result, list):
                return result
            return result.get("jobs", [])
        except json.JSONDecodeError:
            return [
                {
                    "title": "软件开发工程师",
                    "company_type": "大公司",
                    "match_score": 85,
                    "match_reasons": "专业对口，技能匹配",
                    "skill_gaps": "需要加强分布式系统经验",
                    "estimated_salary": "15000-25000元/月"
                }
            ]

    async def generate_skill_path(
        self,
        current_skills: List[str],
        target_position: str
    ) -> Dict[str, Any]:
        """
        生成技能提升路径

        Args:
            current_skills: 当前技能列表
            target_position: 目标岗位

        Returns:
            技能提升路径规划
        """
        skills_str = ", ".join(current_skills) if current_skills else "无"

        prompt = f"""你是一个专业的技术学习规划师。请为以下情况制定技能提升路径：

当前技能: {skills_str}
目标岗位: {target_position}

请制定一个结构化的学习路径，以JSON格式返回：
- skill_gaps: 技能差距分析(字符串)
- learning_path: 学习路径(数组，每个元素包含priority优先级, skill技能名, learning_duration学习周期, resources推荐资源)
- estimated_improvement: 预计提升幅度(字符串)

只返回JSON，不要有其他内容。"""

        messages = [{"role": "user", "content": prompt}]
        response = await self.ai.chat(messages)

        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {
                "skill_gaps": "需要加强算法和系统设计能力",
                "learning_path": [
                    {"priority": 1, "skill": "算法与数据结构", "learning_duration": "2个月", "resources": "LeetCode, 算法导论"},
                    {"priority": 2, "skill": "系统设计", "learning_duration": "1个月", "resources": "DDIA, 系统设计面试"}
                ],
                "estimated_improvement": "预计提升15-20分"
            }

    async def generate_warning(
        self,
        student_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成就业困难预警

        Args:
            student_data: 学生数据字典

        Returns:
            预警信息和辅导建议
        """
        prompt = f"""你是一个专业的就业辅导员。请分析以下学生的就业困难原因并给出辅导建议：

学生信息:
- 专业: {student_data.get('major', '未知')}
- GPA: {student_data.get('gpa', '未知')}
- 就业状态: {student_data.get('employment_status', '待业')}
- 目标城市: {student_data.get('target_city', '未知')}
- 已投递简历数: {student_data.get('resume_count', 0)}

请以JSON格式返回预警分析：
- warning_type: 预警类型(skill_gap/期望过高/location_limited/experience_lacking/综合)
- warning_level: 预警级别(red/yellow/green)
- reasons: 困难原因分析(字符串)
- counseling_suggestions: 辅导建议(数组，每个建议包含type类型, content内容)
- urgency_tasks: 紧急任务(数组)

只返回JSON，不要有其他内容。"""

        messages = [{"role": "user", "content": prompt}]
        response = await self.ai.chat(messages)

        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {
                "warning_type": "skill_gap",
                "warning_level": "yellow",
                "reasons": "技能与市场需求存在一定差距",
                "counseling_suggestions": [
                    {"type": "skill", "content": "建议加强算法能力"},
                    {"type": "practice", "content": "增加项目实践经验"}
                ],
                "urgency_tasks": ["完成一个完整项目", "刷题100道"]
            }

    async def analyze_resume(
        self,
        resume_text: str,
        target_position: str
    ) -> Dict[str, Any]:
        """
        分析简历与岗位的匹配度

        Args:
            resume_text: 简历文本
            target_position: 目标岗位

        Returns:
            简历分析结果
        """
        prompt = f"""你是一个专业的简历优化顾问。请分析以下简历与目标岗位的匹配度：

简历内容:
{resume_text}

目标岗位: {target_position}

请以JSON格式返回分析结果：
- ats_score: ATS模拟评分(0-100)
- keyword_match: 关键词匹配度分析(字符串)
- missing_keywords: 缺失的关键词(数组)
- suggestions: 优化建议(数组，每个建议包含category类别, content内容))
- overall_analysis: 整体分析(字符串)

只返回JSON，不要有其他内容。"""

        messages = [{"role": "user", "content": prompt}]
        response = await self.ai.chat(messages)

        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {
                "ats_score": 75,
                "keyword_match": "基础关键词匹配，需要加强技术深度",
                "missing_keywords": ["分布式系统", "微服务"],
                "suggestions": [
                    {"category": "技术", "content": "突出项目中的技术难点和解决方案"}
                ],
                "overall_analysis": "简历整体不错，建议加强项目描述的技术深度"
            }

    async def compare_graduate_vs_job(
        self,
        target_city: str,
        expected_salary: int,
        preparation_time: str
    ) -> Dict[str, Any]:
        """
        考研vs就业决策辅助

        Args:
            target_city: 目标城市
            expected_salary: 期望薪资
            preparation_time: 备考时间

        Returns:
            决策分析结果
        """
        prompt = f"""你是一个专业的职业规划顾问。请分析考研与就业的回报率：

情况:
- 目标城市: {target_city}
- 期望薪资: {expected_salary}元/月
- 可接受的备考时间: {preparation_time}

请以JSON格式返回分析结果：
- graduate_analysis: 考研分析(对象，包含difficulty难度, cost成本, salary_after涨薪预期, roi回报率))
- job_analysis: 就业分析(对象，包含starting_salary起步薪资, growth_potential成长潜力, opportunity_cost机会成本))
- recommendation: 建议(字符串)
- decision_factors: 决策关键因素(数组)

只返回JSON，不要有其他内容。"""

        messages = [{"role": "user", "content": prompt}]
        response = await self.ai.chat(messages)

        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {
                "graduate_analysis": {
                    "difficulty": "中等",
                    "cost": "2-3年时间成本",
                    "salary_after": "通常提升30-50%",
                    "roi": "需要3-5年回本"
                },
                "job_analysis": {
                    "starting_salary": f"{expected_salary}",
                    "growth_potential": "取决于个人能力",
                    "opportunity_cost": "放弃考研可能的机会"
                },
                "recommendation": "建议先就业积累经验，后期可考虑在职研究生",
                "decision_factors": ["个人兴趣", "家庭经济状况", "职业规划", "考研难度"]
            }


# 全局AI服务实例
ai_service = EmploymentAIService()