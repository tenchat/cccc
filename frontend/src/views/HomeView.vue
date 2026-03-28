<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Hero section chart ref
const heroChartRef = ref<any>(null)

// Real-time chart options
const heroChartOptions = {
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
    axisLine: { lineStyle: { color: '#e2e8f0' } },
    axisLabel: { color: '#64748b' }
  },
  yAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: '#e2e8f0' } },
    axisLabel: { color: '#64748b' },
    splitLine: { lineStyle: { color: '#f1f5f9' } }
  },
  series: [
    {
      name: '活跃用户',
      type: 'line',
      smooth: true,
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
            { offset: 1, color: 'rgba(102, 126, 234, 0)' }
          ]
        }
      },
      lineStyle: { color: '#667eea', width: 3 },
      itemStyle: { color: '#667eea' },
      data: [120, 200, 150, 80, 300, 250, 400]
    }
  ]
}

// Features data
const features = [
  {
    icon: 'Odometer',
    title: '实时监控',
    description: '毫秒级数据更新，实时掌握业务动态'
  },
  {
    icon: 'DataAnalysis',
    title: '智能分析',
    description: 'AI驱动的数据分析，洞察隐藏趋势'
  },
  {
    icon: 'Monitor',
    title: '可视化大屏',
    description: '多种图表类型，灵活定制展示效果'
  },
  {
    icon: 'Setting',
    title: '简易配置',
    description: '拖拽式配置，快速搭建数据看板'
  }
]

// Trust badges
const trustBadges = [
  { text: 'SOC 2认证' },
  { text: 'ISO 27001' },
  { text: 'GDPR合规' },
  { text: '99.9%可用性' }
]

onMounted(() => {
  if (heroChartRef.value) {
    heroChartRef.value.resize()
  }
})
</script>

<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">新一代数据分析平台</h1>
        <p class="hero-subtitle">
          实时可视化、智能分析、轻松洞察业务价值
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" class="cta-button">
            免费试用
          </el-button>
          <el-button size="large" class="cta-button secondary">
            观看演示
          </el-button>
        </div>
      </div>

      <!-- Hero Chart -->
      <div class="hero-chart-container">
        <div class="card">
          <div class="chart-header">
            <span class="chart-title">实时活跃用户</span>
            <span class="chart-live">
              <span class="live-dot"></span>
              LIVE
            </span>
          </div>
          <v-chart
            ref="heroChartRef"
            class="hero-chart"
            :option="heroChartOptions"
            autoresize
          />
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <h2 class="section-title">核心功能</h2>
      <div class="features-grid">
        <div
          v-for="feature in features"
          :key="feature.title"
          class="feature-card card"
        >
          <el-icon :size="48" class="feature-icon">
            <component :is="feature.icon" />
          </el-icon>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- Trust Section -->
    <section class="trust-section">
      <div class="trust-badges">
        <span v-for="badge in trustBadges" :key="badge.text" class="trust-badge">
          <el-icon><Lock /></el-icon>
          {{ badge.text }}
        </span>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  min-height: 100vh;
  padding: 0 24px 80px;
}

/* Hero Section */
.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 0;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
  margin-bottom: 24px;
}

.hero-subtitle {
  font-size: 20px;
  color: #64748b;
  margin-bottom: 40px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.cta-button {
  padding: 16px 32px;
  font-size: 16px;
  border-radius: 12px;
}

.cta-button.secondary {
  background: white;
  border: 1px solid #e2e8f0;
  color: #1e293b;
}

.cta-button.secondary:hover {
  background: #f8fafc;
}

/* Hero Chart */
.hero-chart-container {
  perspective: 1000px;
}

.card {
  background: white;
  border-radius: 24px;
  border: 1px solid #e2e8f0;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-title {
  color: #1e293b;
  font-weight: 600;
  font-size: 16px;
}

.chart-live {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #22c55e;
  font-size: 12px;
  font-weight: 600;
}

.live-dot {
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.hero-chart {
  height: 280px;
}

/* Features Section */
.features-section {
  max-width: 1200px;
  margin: 80px auto;
}

.section-title {
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 48px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.feature-card {
  text-align: center;
  padding: 32px 24px;
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
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

/* Trust Section */
.trust-section {
  max-width: 800px;
  margin: 80px auto;
}

.trust-badges {
  display: flex;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
}

.trust-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
}

.trust-badge .el-icon {
  color: #64748b;
}

/* Responsive */
@media (max-width: 1024px) {
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-title {
    font-size: 42px;
  }

  .hero-actions {
    justify-content: center;
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 32px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .trust-badges {
    flex-direction: column;
    align-items: center;
  }
}
</style>
