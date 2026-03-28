<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isMenuOpen = ref(false)

const menuItems = [
  { path: '/', label: '首页', icon: 'HomeFilled' },
  { path: '/dashboard', label: '数据看板', icon: 'DataAnalysis' }
]

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const navigateTo = (path: string) => {
  router.push(path)
  isMenuOpen.value = false
}
</script>

<template>
  <div class="main-layout">
    <!-- Navigation -->
    <nav class="navbar">
      <div class="navbar-content">
        <div class="logo">
          <el-icon :size="24" color="#667eea"><DataAnalysis /></el-icon>
          <span class="logo-text">大学生就业信息智能分析平台</span>
        </div>

        <div class="nav-links desktop-only">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-link"
            :class="{ active: route.path === item.path }"
          >
            {{ item.label }}
          </router-link>
        </div>

        <el-button class="mobile-menu-btn" @click="toggleMenu">
          <el-icon v-if="!isMenuOpen"><Expand /></el-icon>
          <el-icon v-else><Fold /></el-icon>
        </el-button>
      </div>

      <!-- Mobile Menu -->
      <div v-if="isMenuOpen" class="mobile-menu">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="mobile-nav-link"
          @click="navigateTo(item.path)"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          {{ item.label }}
        </router-link>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.main-layout {
  min-height: 100vh;
  background: #f8fafc;
}

.navbar {
  position: fixed;
  top: 16px;
  left: 16px;
  right: 16px;
  z-index: 1000;
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-text {
  color: #1e293b;
  font-size: 18px;
  font-weight: 600;
}

.nav-links {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.active {
  color: #667eea;
}

.mobile-menu-btn {
  display: none;
  background: transparent;
  border: none;
  color: #64748b;
}

.mobile-menu {
  padding: 0 24px 16px;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  color: #1e293b;
  text-decoration: none;
  border-bottom: 1px solid #e2e8f0;
}

.main-content {
  padding-top: 100px;
}

@media (max-width: 768px) {
  .desktop-only {
    display: none;
  }

  .mobile-menu-btn {
    display: block;
  }

  .logo-text {
    font-size: 16px;
  }
}
</style>
