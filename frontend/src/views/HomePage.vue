<script setup lang="ts">
import { } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const features = [
  {
    icon: 'DataAnalysis',
    title: '数据可视化',
    description: '多维度图表展示就业数据，洞察趋势变化'
  },
  {
    icon: 'Cpu',
    title: 'AI智能分析',
    description: '人工智能算法精准分析就业竞争力'
  },
  {
    icon: 'Star',
    title: '个性化推荐',
    description: '智能匹配岗位与人才，提升就业效率'
  },
  {
    icon: 'TrendCharts',
    title: '趋势分析',
    description: '实时追踪就业市场动态，把握就业风向'
  },
  {
    icon: 'OfficeBuilding',
    title: '企业入驻',
    description: '知名企业平台入驻，寻找优秀人才'
  },
  {
    icon: 'Tracking',
    title: '就业追踪',
    description: '全程追踪就业状态，服务触手可及'
  }
]

const roles = [
  {
    icon: 'User',
    title: '学生入口',
    description: '管理个人档案，获取岗位推荐',
    path: '/login',
    color: '#667eea'
  },
  {
    icon: 'School',
    title: '学校入口',
    description: '管理学生就业，查看统计分析',
    path: '/login',
    color: '#22c55e'
  },
  {
    icon: 'OfficeBuilding',
    title: '企业入口',
    description: '发布岗位信息，筛选优秀人才',
    path: '/login',
    color: '#f59e0b'
  }
]

const techStack = [
  { name: 'Vue 3', icon: '👨‍💻' },
  { name: 'TypeScript', icon: '📘' },
  { name: 'Element Plus', icon: '🎨' },
  { name: 'ECharts', icon: '📊' },
  { name: 'Pinia', icon: '📦' }
]

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">大学生就业信息智能分析平台</h1>
        <p class="hero-subtitle">
          汇聚AI智能分析、数据可视化、个性化推荐，为大学生就业提供全方位服务
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" class="cta-button" @click="goToLogin">
            立即登录
          </el-button>
          <el-button size="large" class="cta-button secondary" @click="goToRegister">
            免费注册
          </el-button>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <h2 class="section-title">功能特色</h2>
      <div class="features-grid">
        <div
          v-for="feature in features"
          :key="feature.title"
          class="feature-card"
        >
          <el-icon :size="48" class="feature-icon">
            <component :is="feature.icon" />
          </el-icon>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- Role Entry Section -->
    <section class="roles-section">
      <h2 class="section-title">角色入口</h2>
      <div class="roles-grid">
        <div
          v-for="role in roles"
          :key="role.title"
          class="role-card"
          :style="{ '--role-color': role.color }"
          @click="router.push(role.path)"
        >
          <el-icon :size="56" class="role-icon">
            <component :is="role.icon" />
          </el-icon>
          <h3 class="role-title">{{ role.title }}</h3>
          <p class="role-description">{{ role.description }}</p>
        </div>
      </div>
    </section>

    <!-- Tech Stack Section -->
    <section class="tech-section">
      <h2 class="section-title">技术亮点</h2>
      <div class="tech-badges">
        <div v-for="tech in techStack" :key="tech.name" class="tech-badge">
          <span class="tech-icon">{{ tech.icon }}</span>
          <span class="tech-name">{{ tech.name }}</span>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <p>© 2024 大学生就业信息智能分析平台. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Hero Section */
.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: 60px 24px;
  text-align: center;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  color: white;
  line-height: 1.2;
  margin-bottom: 24px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 40px;
  line-height: 1.6;
  max-width: 600px;
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.cta-button {
  padding: 16px 32px;
  font-size: 16px;
  border-radius: 12px;
  font-weight: 600;
}

.cta-button.secondary {
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  backdrop-filter: blur(10px);
}

.cta-button.secondary:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Sections */
.features-section,
.roles-section,
.tech-section {
  background: #f8fafc;
  padding: 80px 24px;
}

.section-title {
  text-align: center;
  font-size: 36px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 48px;
}

/* Features Grid */
.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  color: #667eea;
  margin-bottom: 20px;
}

.feature-title {
  color: #1e293b;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
}

.feature-description {
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
}

/* Roles Grid */
.roles-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  max-width: 1000px;
  margin: 0 auto;
}

.role-card {
  background: white;
  border-radius: 20px;
  padding: 40px 32px;
  text-align: center;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.role-card:hover {
  border-color: var(--role-color);
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.1);
}

.role-icon {
  color: var(--role-color);
  margin-bottom: 20px;
}

.role-title {
  color: #1e293b;
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 12px;
}

.role-description {
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
}

/* Tech Stack */
.tech-badges {
  display: flex;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap;
}

.tech-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 12px 24px;
  border-radius: 100px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.tech-icon {
  font-size: 20px;
}

.tech-name {
  color: #1e293b;
  font-weight: 600;
  font-size: 14px;
}

/* Footer */
.footer {
  background: #1e293b;
  padding: 32px 24px;
  text-align: center;
}

.footer p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

/* Responsive */
@media (max-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .hero-title {
    font-size: 42px;
  }
}

@media (max-width: 768px) {
  .features-grid,
  .roles-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-actions {
    flex-direction: column;
  }
}
</style>
