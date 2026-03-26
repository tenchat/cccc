-- =====================================================
-- 大学生就业信息智能分析平台 - 数据库初始化脚本
-- 版本: v2.0
-- 更新日期: 2026-03-26
-- 特性: 支持学生、学校、用人单位三方角色，AI分析决策
-- =====================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- -----------------------------------------
-- 1. 统一用户表 (accounts) - 学生/学校/企业共用
-- -----------------------------------------
DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
    `account_id` VARCHAR(20) PRIMARY KEY COMMENT '账户标识',
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
    `real_name` VARCHAR(50) COMMENT '真实姓名/企业名',
    `email` VARCHAR(100) COMMENT '邮箱',
    `phone` VARCHAR(20) COMMENT '手机号',
    `avatar_url` VARCHAR(255) COMMENT '头像URL',
    `status` TINYINT DEFAULT 1 COMMENT '状态(0=禁用 1=启用)',
    `last_login_at` DATETIME COMMENT '最后登录时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_username` (`username`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='统一账户表';

-- -----------------------------------------
-- 2. 角色表 (roles)
-- -----------------------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
    `role_id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '角色ID',
    `role_code` VARCHAR(20) NOT NULL UNIQUE COMMENT '角色代码',
    `role_name` VARCHAR(50) NOT NULL COMMENT '角色名称',
    `description` VARCHAR(255) COMMENT '描述',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- 角色初始数据
INSERT INTO `roles` (`role_code`, `role_name`, `description`) VALUES
('admin', '系统管理员', '系统管理最高权限'),
('student', '学生', '学生用户'),
('school_admin', '学校管理员', '学校就业指导中心'),
('school_viewer', '学校查看员', '学校数据查看权限'),
('company_admin', '企业管理员', '用人单位管理员'),
('company_recruiter', '企业招聘者', '发布岗位和管理简历');

-- -----------------------------------------
-- 3. 用户角色关联表 (account_roles)
-- -----------------------------------------
DROP TABLE IF EXISTS `account_roles`;
CREATE TABLE `account_roles` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `account_id` VARCHAR(20) NOT NULL COMMENT '账户ID',
    `role_id` INT NOT NULL COMMENT '角色ID',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY `uk_account_role` (`account_id`, `role_id`),
    FOREIGN KEY (`account_id`) REFERENCES `accounts`(`account_id`) ON DELETE CASCADE,
    FOREIGN KEY (`role_id`) REFERENCES `roles`(`role_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户角色关联表';

-- -----------------------------------------
-- 4. 权限表 (permissions)
-- -----------------------------------------
DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
    `permission_id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '权限ID',
    `permission_code` VARCHAR(50) NOT NULL UNIQUE COMMENT '权限代码',
    `permission_name` VARCHAR(50) NOT NULL COMMENT '权限名称',
    `resource_type` VARCHAR(20) COMMENT '资源类型(user/job/report/college/scarce)',
    `action` VARCHAR(20) COMMENT '操作类型(read/write/delete/export)',
    `description` VARCHAR(255) COMMENT '描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限表';

-- 权限初始数据
INSERT INTO `permissions` (`permission_code`, `permission_name`, `resource_type`, `action`, `description`) VALUES
-- 学生权限
('student.profile.read', '查看自己的档案', 'user', 'read', '学生查看自己的档案信息'),
('student.profile.write', '编辑自己的档案', 'user', 'write', '学生编辑自己的档案信息'),
('student.job.read', '查看岗位信息', 'job', 'read', '查看所有岗位信息'),
('student.job.apply', '申请岗位', 'job', 'write', '申请岗位'),
('student.ai.analyze', 'AI就业分析', 'ai', 'write', '使用AI分析就业方向'),
-- 企业权限
('company.profile.read', '查看企业信息', 'company', 'read', '查看自己的企业信息'),
('company.profile.write', '编辑企业信息', 'company', 'write', '编辑企业信息'),
('company.job.read', '查看岗位信息', 'job', 'read', '查看自己发布的岗位'),
('company.job.write', '发布管理岗位', 'job', 'write', '发布和管理岗位'),
('company.student.read', '查看学生信息', 'user', 'read', '查看学生简历信息'),
('company.ai.analyze', 'AI招聘分析', 'ai', 'write', '使用AI分析招聘效果'),
-- 学校权限
('school.student.read', '查看学生信息', 'user', 'read', '查看所有学生信息'),
('school.student.write', '管理学生信息', 'user', 'write', '编辑学生信息'),
('school.company.read', '查看企业信息', 'company', 'read', '查看合作企业信息'),
('school.company.write', '管理企业信息', 'company', 'write', '审核管理企业'),
('school.report.read', '查看就业报告', 'report', 'read', '查看就业报告'),
('school.report.write', '上传就业报告', 'report', 'write', '上传就业报告'),
('school.college.read', '查看学院就业率', 'college', 'read', '查看学院就业率'),
('school.college.write', '管理学院就业率', 'college', 'write', '编辑学院就业率'),
('school.scarce.read', '查看稀缺人才', 'scarce', 'read', '查看稀缺人才目录'),
('school.scarce.write', '管理稀缺人才', 'scarce', 'write', '编辑稀缺人才数据'),
('school.ai.analyze', 'AI决策分析', 'ai', 'write', '使用AI做就业决策分析'),
-- 管理员权限
('admin.all', '超级管理权限', 'all', 'all', '拥有所有权限');

-- -----------------------------------------
-- 5. 角色权限关联表 (role_permissions)
-- -----------------------------------------
DROP TABLE IF EXISTS `role_permissions`;
CREATE TABLE `role_permissions` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `role_id` INT NOT NULL,
    `permission_id` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY `uk_role_permission` (`role_id`, `permission_id`),
    FOREIGN KEY (`role_id`) REFERENCES `roles`(`role_id`) ON DELETE CASCADE,
    FOREIGN KEY (`permission_id`) REFERENCES `permissions`(`permission_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色权限关联表';

-- 为学生角色分配权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 2, `permission_id` FROM `permissions` WHERE `permission_code` LIKE 'student.%' OR `permission_code` LIKE 'company.job.read';

-- 为学校管理员分配权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 3, `permission_id` FROM `permissions` WHERE `permission_code` LIKE 'school.%' OR `permission_code` LIKE 'company.%' OR `permission_code` LIKE 'admin.all';

-- 为企业管理员分配权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 5, `permission_id` FROM `permissions` WHERE `permission_code` LIKE 'company.%';

-- -----------------------------------------
-- 6. 院校表 (universities)
-- -----------------------------------------
DROP TABLE IF EXISTS `universities`;
CREATE TABLE `universities` (
    `university_id` VARCHAR(20) PRIMARY KEY COMMENT '院校代码',
    `university_name` VARCHAR(100) NOT NULL COMMENT '院校名称',
    `province` VARCHAR(20) COMMENT '所在省份',
    `city` VARCHAR(50) COMMENT '所在城市',
    `university_type` VARCHAR(50) COMMENT '院校类型',
    `admin_level` VARCHAR(20) COMMENT '主管单位',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_province` (`province`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='院校表';

-- -----------------------------------------
-- 7. 学生详细档案表 (student_profiles)
-- -----------------------------------------
DROP TABLE IF EXISTS `student_profiles`;
CREATE TABLE `student_profiles` (
    `profile_id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '档案ID',
    `account_id` VARCHAR(20) NOT NULL UNIQUE COMMENT '账户ID',
    `student_id` VARCHAR(20) COMMENT '学号',
    `university_id` VARCHAR(20) COMMENT '院校ID',
    `college` VARCHAR(100) COMMENT '所属学院',
    `major` VARCHAR(100) COMMENT '所学专业',
    `degree` VARCHAR(20) COMMENT '学历',
    `graduation_year` INT COMMENT '毕业年份',
    `live_city` VARCHAR(50) COMMENT '现居住地',
    `desire_city` VARCHAR(50) COMMENT '期望工作城市',
    `desire_industry` VARCHAR(50) COMMENT '期望行业',
    `desire_jd_type` VARCHAR(50) COMMENT '期望职类',
    `desire_salary_id` INT COMMENT '期望薪水ID',
    `cur_industry` VARCHAR(50) COMMENT '最近工作行业',
    `cur_jd_type` VARCHAR(50) COMMENT '最近工作职类',
    `cur_salary` INT COMMENT '最近薪水',
    `age` INT COMMENT '年龄',
    `start_work_date` DATE COMMENT '开始工作时间',
    `experience` TEXT COMMENT '经验描述',
    `resume_url` VARCHAR(255) COMMENT '简历附件URL',
    `skills` TEXT COMMENT '技能证书(JSON)',
    `projects` TEXT COMMENT '项目经验(JSON)',
    `certifications` TEXT COMMENT '证书(JSON)',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`account_id`) REFERENCES `accounts`(`account_id`) ON DELETE CASCADE,
    FOREIGN KEY (`university_id`) REFERENCES `universities`(`university_id`),
    INDEX `idx_university` (`university_id`),
    INDEX `idx_college` (`college`),
    INDEX `idx_major` (`major`),
    INDEX `idx_graduation_year` (`graduation_year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生详细档案表';

-- -----------------------------------------
-- 8. 用人单位表 (companies)
-- -----------------------------------------
DROP TABLE IF EXISTS `companies`;
CREATE TABLE `companies` (
    `company_id` VARCHAR(20) PRIMARY KEY COMMENT '企业标识',
    `account_id` VARCHAR(20) NOT NULL UNIQUE COMMENT '账户ID',
    `company_name` VARCHAR(100) NOT NULL COMMENT '公司名称',
    `company_type` VARCHAR(50) COMMENT '企业类型',
    `industry` VARCHAR(50) COMMENT '所属行业',
    `scale` VARCHAR(20) COMMENT '规模',
    `city` VARCHAR(50) COMMENT '总部城市',
    `address` VARCHAR(255) COMMENT '详细地址',
    `business_license` VARCHAR(255) COMMENT '营业执照URL',
    `contact_person` VARCHAR(50) COMMENT '联系人',
    `contact_phone` VARCHAR(20) COMMENT '联系电话',
    `description` TEXT COMMENT '企业简介',
    `verified` TINYINT DEFAULT 0 COMMENT '认证状态(0=未认证 1=已认证)',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`account_id`) REFERENCES `accounts`(`account_id`) ON DELETE CASCADE,
    INDEX `idx_industry` (`industry`),
    INDEX `idx_city` (`city`),
    INDEX `idx_verified` (`verified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用人单位表';

-- -----------------------------------------
-- 9. 岗位需求表 (job_descriptions)
-- -----------------------------------------
DROP TABLE IF EXISTS `job_descriptions`;
CREATE TABLE `job_descriptions` (
    `jd_no` VARCHAR(20) PRIMARY KEY COMMENT '职位代码',
    `company_id` VARCHAR(20) NOT NULL COMMENT '企业ID',
    `jd_title` VARCHAR(100) NOT NULL COMMENT '职位标题',
    `city` VARCHAR(50) NOT NULL COMMENT '工作城市',
    `jd_sub_type` VARCHAR(50) COMMENT '职位子类',
    `industry` VARCHAR(50) COMMENT '所属行业',
    `require_nums` INT DEFAULT 1 COMMENT '需求人数',
    `max_salary` INT COMMENT '最高月薪',
    `min_salary` INT COMMENT '最低月薪',
    `start_date` DATE COMMENT '开始日期',
    `end_date` DATE COMMENT '结束日期',
    `is_travel` TINYINT DEFAULT 0 COMMENT '是否出差',
    `min_years` VARCHAR(10) COMMENT '工作年限',
    `key_words` VARCHAR(255) COMMENT '关键字',
    `min_edu_level` INT COMMENT '最低学历ID',
    `max_edu_level` INT COMMENT '最高学历ID',
    `is_mangerial` TINYINT DEFAULT 0 COMMENT '是否管理经验',
    `resume_language_required` VARCHAR(50) COMMENT '语言需求',
    `job_description` TEXT COMMENT '职位描述',
    `status` TINYINT DEFAULT 1 COMMENT '状态(0=下架 1=发布中)',
    `view_count` INT DEFAULT 0 COMMENT '浏览次数',
    `apply_count` INT DEFAULT 0 COMMENT '申请次数',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`) ON DELETE CASCADE,
    FOREIGN KEY (`min_edu_level`) REFERENCES `degrees`(`id`) ON DELETE SET NULL,
    FOREIGN KEY (`max_edu_level`) REFERENCES `degrees`(`id`) ON DELETE SET NULL,
    INDEX `idx_company` (`company_id`),
    INDEX `idx_city` (`city`),
    INDEX `idx_industry` (`industry`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='岗位需求表';

-- -----------------------------------------
-- 10. 岗位申请记录表 (job_applications)
-- -----------------------------------------
DROP TABLE IF EXISTS `job_applications`;
CREATE TABLE `job_applications` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `jd_no` VARCHAR(20) NOT NULL COMMENT '岗位代码',
    `account_id` VARCHAR(20) NOT NULL COMMENT '学生账户ID',
    `resume_url` VARCHAR(255) COMMENT '投递的简历',
    `cover_letter` TEXT COMMENT '求职信',
    `status` TINYINT DEFAULT 0 COMMENT '状态(0=待处理 1=已查看 2=邀请面试 3=不合适 4=已录用)',
    `remark` TEXT COMMENT '备注',
    `applied_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`jd_no`) REFERENCES `job_descriptions`(`jd_no`) ON DELETE CASCADE,
    FOREIGN KEY (`account_id`) REFERENCES `accounts`(`account_id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_jd_account` (`jd_no`, `account_id`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='岗位申请记录表';

-- -----------------------------------------
-- 11. 学历字典表 (degrees)
-- -----------------------------------------
DROP TABLE IF EXISTS `degrees`;
CREATE TABLE `degrees` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE,
    `level` INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学历字典';

-- -----------------------------------------
-- 12. 薪资字典表 (salary_levels)
-- -----------------------------------------
DROP TABLE IF EXISTS `salary_levels`;
CREATE TABLE `salary_levels` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `min_salary` INT NOT NULL,
    `max_salary` INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='薪资字典';

-- -----------------------------------------
-- 13. 工作年限字典表 (work_years)
-- -----------------------------------------
DROP TABLE IF EXISTS `work_years`;
CREATE TABLE `work_years` (
    `code` VARCHAR(10) PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL,
    `min_years` INT NOT NULL,
    `max_years` INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='工作年限字典';

-- -----------------------------------------
-- 14. 行业字典表 (industries)
-- -----------------------------------------
DROP TABLE IF EXISTS `industries`;
CREATE TABLE `industries` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `parent_id` INT,
    INDEX `idx_parent` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行业字典';

-- -----------------------------------------
-- 15. 职类字典表 (job_types)
-- -----------------------------------------
DROP TABLE IF EXISTS `job_types`;
CREATE TABLE `job_types` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `parent_id` INT,
    INDEX `idx_parent` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='职类字典';

-- -----------------------------------------
-- 16. 城市字典表 (cities)
-- -----------------------------------------
DROP TABLE IF EXISTS `cities`;
CREATE TABLE `cities` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `province` VARCHAR(20) NOT NULL,
    `level` INT DEFAULT 2,
    INDEX `idx_province` (`province`),
    INDEX `idx_level` (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='城市字典';

-- -----------------------------------------
-- 17. 就业报告表 (employment_reports)
-- -----------------------------------------
DROP TABLE IF EXISTS `employment_reports`;
CREATE TABLE `employment_reports` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `report_year` INT NOT NULL COMMENT '报告年份',
    `report_title` VARCHAR(200) NOT NULL COMMENT '报告标题',
    `source` VARCHAR(100) COMMENT '来源',
    `publish_date` DATE COMMENT '发布日期',
    `summary` TEXT COMMENT '摘要',
    `content_url` VARCHAR(255) COMMENT '原文链接/文件路径',
    `uploaded_by` VARCHAR(20) COMMENT '上传人账户ID',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`uploaded_by`) REFERENCES `accounts`(`account_id`),
    INDEX `idx_year` (`report_year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='就业报告表';

-- -----------------------------------------
-- 18. 各省稀缺人才表 (scarce_talents)
-- -----------------------------------------
DROP TABLE IF EXISTS `scarce_talents`;
CREATE TABLE `scarce_talents` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `province` VARCHAR(20) NOT NULL COMMENT '省份',
    `industry` VARCHAR(50) COMMENT '行业',
    `occupation` VARCHAR(100) COMMENT '职业/岗位',
    `demand_rank` INT COMMENT '需求排名',
    `year` INT COMMENT '年份',
    `demand_index` DECIMAL(5,2) COMMENT '需求指数',
    `avg_salary` INT COMMENT '平均薪资',
    `source` VARCHAR(100) COMMENT '数据来源',
    `uploaded_by` VARCHAR(20) COMMENT '上传人账户ID',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`uploaded_by`) REFERENCES `accounts`(`account_id`),
    INDEX `idx_province` (`province`),
    INDEX `idx_year` (`year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='各省稀缺人才目录';

-- -----------------------------------------
-- 19. 学院就业率表 (college_employment)
-- -----------------------------------------
DROP TABLE IF EXISTS `college_employment`;
CREATE TABLE `college_employment` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `college_name` VARCHAR(100) NOT NULL COMMENT '院系名称',
    `university_id` VARCHAR(20) COMMENT '院校ID',
    `degree_type` VARCHAR(20) COMMENT '学历类型',
    `graduation_year` INT NOT NULL COMMENT '毕业年份',
    `graduate_nums` INT NOT NULL COMMENT '毕业人数',
    `employed_nums` INT NOT NULL COMMENT '就业数',
    `employment_rate` DECIMAL(5,2) COMMENT '毕业去向落实率',
    `signed_nums` INT COMMENT '签约人数',
    `signed_rate` DECIMAL(5,2) COMMENT '签约率',
    `further_study_nums` INT COMMENT '总升学人数',
    `further_study_rate` DECIMAL(5,2) COMMENT '总升学率',
    `domestic_study_nums` INT COMMENT '境内升学人数',
    `domestic_study_rate` DECIMAL(5,2) COMMENT '境内升学率',
    `overseas_study_nums` INT COMMENT '境外升学人数',
    `overseas_study_rate` DECIMAL(5,2) COMMENT '境外升学率',
    `uploaded_by` VARCHAR(20) COMMENT '上传人账户ID',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`university_id`) REFERENCES `universities`(`university_id`),
    FOREIGN KEY (`uploaded_by`) REFERENCES `accounts`(`account_id`),
    UNIQUE KEY `uk_college_year_degree` (`college_name`, `graduation_year`, `degree_type`),
    INDEX `idx_year` (`graduation_year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学院就业率数据表';

-- -----------------------------------------
-- 20. AI服务类型表 (ai_services)
-- -----------------------------------------
DROP TABLE IF EXISTS `ai_services`;
CREATE TABLE `ai_services` (
    `service_id` INT PRIMARY KEY AUTO_INCREMENT,
    `service_code` VARCHAR(50) NOT NULL UNIQUE COMMENT '服务代码',
    `service_name` VARCHAR(100) NOT NULL COMMENT '服务名称',
    `description` TEXT COMMENT '服务描述',
    `input_schema` TEXT COMMENT '输入参数JSON Schema',
    `output_schema` TEXT COMMENT '输出结果JSON Schema',
    `prompt_template` TEXT COMMENT 'AI提示词模板',
    `enabled` TINYINT DEFAULT 1 COMMENT '是否启用',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI服务类型表';

-- 初始化AI服务类型
INSERT INTO `ai_services` (`service_code`, `service_name`, `description`, `enabled`) VALUES
('career_match', '就业方向匹配', '根据学生档案推荐匹配的岗位和就业方向', 1),
('salary_prediction', '薪资预测', '预测学生可能的薪资范围', 1),
('skill_gap_analysis', '技能差距分析', '分析学生技能与目标岗位的差距', 1),
('resume_optimization', '简历优化建议', '优化简历提高通过率', 1),
('interview_preparation', '面试准备指导', '提供面试指导和预测问题', 1),
('job_recommendation', '智能岗位推荐', '根据企业需求推荐合适的学生', 1),
('market_trend_analysis', '市场趋势分析', '分析行业就业趋势', 1),
('warning_student', '就业困难预警', '预警潜在就业困难学生', 1),
('graduate_decision', '考研vs就业分析', '分析考研与就业的ROI', 1);

-- -----------------------------------------
-- 21. AI分析请求记录表 (ai_analysis_requests)
-- -----------------------------------------
DROP TABLE IF EXISTS `ai_analysis_requests`;
CREATE TABLE `ai_analysis_requests` (
    `request_id` INT PRIMARY KEY AUTO_INCREMENT,
    `service_id` INT NOT NULL COMMENT 'AI服务ID',
    `account_id` VARCHAR(20) NOT NULL COMMENT '请求用户账户ID',
    `input_data` TEXT NOT NULL COMMENT '输入数据(JSON)',
    `output_data` TEXT COMMENT '输出结果(JSON)',
    `status` VARCHAR(20) DEFAULT 'pending' COMMENT '状态(pending/processing/completed/failed)',
    `error_message` TEXT COMMENT '错误信息',
    `token_usage` INT COMMENT 'Token消耗',
    `cost` DECIMAL(10,2) COMMENT '费用',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `completed_at` DATETIME COMMENT '完成时间',
    FOREIGN KEY (`service_id`) REFERENCES `ai_services`(`service_id`),
    FOREIGN KEY (`account_id`) REFERENCES `accounts`(`account_id`),
    INDEX `idx_account` (`account_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI分析请求记录表';

-- -----------------------------------------
-- 22. AI推荐结果表 (ai_recommendations)
-- -----------------------------------------
DROP TABLE IF EXISTS `ai_recommendations`;
CREATE TABLE `ai_recommendations` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `request_id` INT NOT NULL COMMENT '分析请求ID',
    `recommend_type` VARCHAR(20) COMMENT '推荐类型(job/school/skill/course)',
    `target_id` VARCHAR(50) COMMENT '推荐目标ID',
    `target_name` VARCHAR(100) COMMENT '推荐目标名称',
    `match_score` DECIMAL(5,2) COMMENT '匹配度分数',
    `reason` TEXT COMMENT '推荐理由',
    `suggestions` TEXT COMMENT '建议(JSON数组)',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`request_id`) REFERENCES `ai_analysis_requests`(`request_id`) ON DELETE CASCADE,
    INDEX `idx_request` (`request_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI推荐结果表';

-- -----------------------------------------
-- 23. AI预警记录表 (ai_warnings)
-- -----------------------------------------
DROP TABLE IF EXISTS `ai_warnings`;
CREATE TABLE `ai_warnings` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `account_id` VARCHAR(20) NOT NULL COMMENT '被预警的学生账户ID',
    `warning_type` VARCHAR(50) NOT NULL COMMENT '预警类型',
    `warning_level` VARCHAR(10) NOT NULL COMMENT '预警级别(red/yellow/green)',
    `title` VARCHAR(100) COMMENT '预警标题',
    `content` TEXT COMMENT '预警内容',
    `suggestions` TEXT COMMENT '建议措施(JSON)',
    `status` TINYINT DEFAULT 0 COMMENT '状态(0=未处理 1=已处理 2=已忽略)',
    `handled_by` VARCHAR(20) COMMENT '处理人',
    `handled_at` DATETIME COMMENT '处理时间',
    `handled_remark` TEXT COMMENT '处理备注',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`account_id`) REFERENCES `accounts`(`account_id`),
    INDEX `idx_account` (`account_id`),
    INDEX `idx_level` (`warning_level`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI预警记录表';

-- -----------------------------------------
-- 24. 数据操作审计日志表 (data_audit_logs)
-- -----------------------------------------
DROP TABLE IF EXISTS `data_audit_logs`;
CREATE TABLE `data_audit_logs` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `account_id` VARCHAR(20) NOT NULL COMMENT '操作人账户ID',
    `action` VARCHAR(20) NOT NULL COMMENT '操作类型(insert/update/delete/export)',
    `table_name` VARCHAR(50) NOT NULL COMMENT '操作的表名',
    `record_id` VARCHAR(50) COMMENT '操作的记录ID',
    `old_value` TEXT COMMENT '修改前的值(JSON)',
    `new_value` TEXT COMMENT '修改后的值(JSON)',
    `ip_address` VARCHAR(50) COMMENT 'IP地址',
    `user_agent` VARCHAR(255) COMMENT 'User Agent',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`account_id`) REFERENCES `accounts`(`account_id`),
    INDEX `idx_account` (`account_id`),
    INDEX `idx_table` (`table_name`),
    INDEX `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据操作审计日志表';

-- -----------------------------------------
-- 25. 字典表初始化数据
-- -----------------------------------------

-- 学历数据
INSERT INTO `degrees` (`name`, `level`) VALUES
('中专', 1), ('大专', 2), ('本科', 3), ('硕士', 4), ('博士', 5);

-- 薪资区间数据
INSERT INTO `salary_levels` (`name`, `min_salary`, `max_salary`) VALUES
('3k以下', 0, 3000), ('3k-5k', 3000, 5000), ('5k-8k', 5000, 8000),
('8k-12k', 8000, 12000), ('12k-20k', 12000, 20000), ('20k-30k', 20000, 30000), ('30k以上', 30000, 100000);

-- 工作年限数据
INSERT INTO `work_years` (`code`, `name`, `min_years`, `max_years`) VALUES
('0', '不限', 0, 0), ('103', '1-3年', 1, 3), ('305', '3-5年', 3, 5),
('510', '5-10年', 5, 10), ('1099', '10年以上', 10, 100);

-- 行业数据
INSERT INTO `industries` (`name`, `parent_id`) VALUES
('互联网/IT', NULL), ('计算机软件', 1), ('计算机硬件', 1), ('通信/网络设备', 1),
('电子商务', NULL), ('金融', NULL), ('银行', 6), ('证券/基金', 6), ('保险', 6),
('房地产/建筑', NULL), ('教育培训', NULL), ('医疗健康', NULL), ('制造业', NULL),
('电子/半导体', 12), ('汽车/交通', NULL), ('消费品/零售', NULL), ('传媒/文化', NULL);

-- 职类数据
INSERT INTO `job_types` (`name`, `parent_id`) VALUES
('技术', NULL), ('后端开发', 1), ('前端开发', 1), ('移动端开发', 1), ('测试', 1),
('运维/DevOps', 1), ('算法', 1), ('数据', 1), ('产品', NULL), ('设计', NULL),
('运营', NULL), ('市场/销售', NULL), ('职能', NULL), ('HR', 13), ('财务', 13),
('行政', 13), ('管培生', NULL);

-- 城市数据
INSERT INTO `cities` (`name`, `province`, `level`) VALUES
('北京', '北京', 1), ('上海', '上海', 1), ('深圳', '广东', 1), ('广州', '广东', 1),
('杭州', '浙江', 1), ('南京', '江苏', 2), ('苏州', '江苏', 2), ('成都', '四川', 2),
('武汉', '湖北', 2), ('西安', '陕西', 2), ('天津', '天津', 2), ('重庆', '重庆', 2),
('长沙', '湖南', 2), ('郑州', '河南', 2), ('青岛', '山东', 2), ('大连', '辽宁', 2),
('厦门', '福建', 2), ('合肥', '安徽', 2), ('昆明', '云南', 3), ('沈阳', '辽宁', 2),
('哈尔滨', '黑龙江', 3), ('南昌', '江西', 3), ('贵阳', '贵州', 3);

SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- 数据库初始化完成 (v2.0)
-- =====================================================
