"""
AI 就业指导 API
集成 MiniMax 大语言模型
"""
import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from app.services.ai_service import ai_service

router = APIRouter(prefix="/ai", tags=["AI就业指导"])


class EmploymentProfileRequest(BaseModel):
    major: str = Field(..., description="专业")
    gpa: float = Field(..., ge=0, le=4.0, description="GPA")
    skills: List[str] = Field(default=[], description="技能列表")
    target_city: str = Field(..., description="目标城市")
    internship: Optional[str] = Field(None, description="实习经历")


class JobRecommendationRequest(BaseModel):
    major: str = Field(..., description="专业")
    skills: List[str] = Field(default=[], description="技能列表")
    target_city: str = Field(..., description="目标城市")
    salary_expectation: Optional[int] = Field(None, description="期望薪资")


class SkillPathRequest(BaseModel):
    current_skills: List[str] = Field(default=[], description="当前技能列表")
    target_position: str = Field(..., description="目标岗位")


class ResumeAnalysisRequest(BaseModel):
    resume_text: str = Field(..., description="简历文本")
    target_position: str = Field(..., description="目标岗位")


class WarningRequest(BaseModel):
    major: str = Field(..., description="专业")
    gpa: float = Field(..., ge=0, le=4.0, description="GPA")
    employment_status: int = Field(..., description="就业状态 0待业 1就业 2升学 3出国")
    target_city: str = Field(..., description="目标城市")
    resume_count: int = Field(default=0, description="已投递简历数")


class GraduateVsJobRequest(BaseModel):
    target_city: str = Field(..., description="目标城市")
    expected_salary: int = Field(..., description="期望薪资")
    preparation_time: str = Field(..., description="备考时间")


@router.post("/employment-profile")
async def get_employment_profile(request: EmploymentProfileRequest):
    """
    生成就业竞争力画像

    输入学生专业、GPA、技能、目标城市等信息
    输出就业竞争力评分(0-100)及多维度分析
    """
    try:
        result = await ai_service.generate_employment_profile(
            major=request.major,
            gpa=request.gpa,
            skills=request.skills,
            target_city=request.target_city,
            internship=request.internship
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")


@router.post("/job-recommendation")
async def get_job_recommendation(request: JobRecommendationRequest):
    """
    岗位匹配推荐

    基于学生档案推荐Top-N匹配岗位
    给出每个岗位的匹配度说明
    """
    try:
        result = await ai_service.recommend_jobs(
            major=request.major,
            skills=request.skills,
            target_city=request.target_city,
            salary_expectation=request.salary_expectation
        )
        return {"recommendations": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")


@router.post("/skill-path")
async def get_skill_path(request: SkillPathRequest):
    """
    技能提升路径规划

    分析当前技能与目标岗位的Gap
    输出结构化的学习路径建议
    """
    try:
        result = await ai_service.generate_skill_path(
            current_skills=request.current_skills,
            target_position=request.target_position
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")


@router.post("/warning")
async def generate_warning(request: WarningRequest):
    """
    就业困难预警

    对未就业且接近毕业的学生生成预警标签
    推送给辅导员，支持批量生成定向辅导建议
    """
    try:
        student_data = {
            "major": request.major,
            "gpa": request.gpa,
            "employment_status": request.employment_status,
            "target_city": request.target_city,
            "resume_count": request.resume_count
        }
        result = await ai_service.generate_warning(student_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")


@router.post("/resume-analysis")
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    简历关键词优化建议

    对比简历与目标岗位的JD关键词
    AI指出语义差距，给出优化建议
    类似ATS模拟评分
    """
    try:
        result = await ai_service.analyze_resume(
            resume_text=request.resume_text,
            target_position=request.target_position
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")


@router.post("/graduate-vs-job")
async def compare_graduate_vs_job(request: GraduateVsJobRequest):
    """
    考研vs就业决策辅助

    综合当前学历对应的岗位薪资分布
    目标院校录取难度、读研后薪资提升预期
    输出量化的考研回报率分析
    """
    try:
        result = await ai_service.compare_graduate_vs_job(
            target_city=request.target_city,
            expected_salary=request.expected_salary,
            preparation_time=request.preparation_time
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")