import random
import json
import sys
import os

# 添加backend目录到sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, Base
from app.models.student import Student

# 模拟数据池
COLLEGES = ["计算机学院", "信息工程学院", "软件学院", "电子工程学院", "机械工程学院"]

MAJORS = {
    "计算机学院": ["计算机科学与技术", "信息安全", "物联网工程"],
    "信息工程学院": ["电子信息工程", "通信工程", "自动化"],
    "软件学院": ["软件工程", "数据科学与大数据技术", "人工智能"],
    "电子工程学院": ["电子科学与技术", "微电子科学与工程"],
    "机械工程学院": ["机械设计制造及其自动化", "材料成型及控制工程"]
}

PROVINCES = ["北京", "上海", "广东", "浙江", "江苏", "四川", "湖北", "湖南", "山东", "河南", "河北", "陕西", "安徽", "福建", "江西"]
GRADES = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
EMPLOYMENT_STATUS = [0, 1, 2, 3]  # 待业、就业、升学、出国
SKILLS_POOL = ["Python", "Java", "C++", "JavaScript", "SQL", "机器学习", "深度学习", "前端开发", "后端开发", "数据分析", "云计算", "网络安全"]
COMPANIES = ["阿里巴巴", "腾讯", "百度", "字节跳动", "京东", "美团", "华为", "网易", "滴滴", "拼多多", "小米", "vivo", "OPPO", "海尔", "格力"]
POSITIONS = ["软件开发工程师", "算法工程师", "数据分析师", "产品经理", "测试工程师", "运维工程师", "前端工程师", "后端工程师", "架构师", "技术项目经理"]


def generate_students(count: int = 500):
    # 创建表
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # 清除旧数据
    db.query(Student).delete()
    db.commit()

    students = []
    for i in range(count):
        college = random.choice(COLLEGES)
        major = random.choice(MAJORS[college])
        grade = random.choice(GRADES)
        status = random.choices(
            EMPLOYMENT_STATUS,
            weights=[15, 60, 15, 10]  # 待业15%、就业60%、升学15%、出国10%
        )[0]

        student = Student(
            student_id=f"{grade}1{random.randint(100000, 999999)}",
            name=f"学生{i+1}",
            college=college,
            major=major,
            grade=grade,
            province=random.choice(PROVINCES),
            gpa=round(random.uniform(2.0, 4.0), 2),
            employment_status=status,
            salary=random.randint(5000, 25000) if status == 1 else None,
            company=random.choice(COMPANIES) if status == 1 else None,
            position=random.choice(POSITIONS) if status == 1 else None,
            skills=json.dumps(random.sample(SKILLS_POOL, k=random.randint(2, 5))),
            internship="XX公司实习3个月" if random.random() > 0.5 else None,
            target_city=random.choice(PROVINCES)
        )
        students.append(student)

    db.add_all(students)
    db.commit()
    print(f"成功生成 {count} 条学生模拟数据")

    # 打印统计
    total = db.query(Student).count()
    employed = db.query(Student).filter(Student.employment_status == 1).count()
    print(f"总人数: {total}, 就业人数: {employed}, 就业率: {employed/total*100:.1f}%")

    db.close()


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    generate_students(count)