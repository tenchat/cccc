# Analytics Dashboard Frontend

Vue 3 + Vite + TypeScript 前端项目，用于数据分析和可视化展示。

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | ^3.4.21 | 渐进式JavaScript框架 |
| Vite | ^5.2.0 | 下一代前端构建工具 |
| TypeScript | ~5.4.0 | JavaScript超集 |
| Element Plus | ^2.6.1 | Vue 3 UI组件库 |
| ECharts | ^5.5.0 | 数据可视化图表库 |
| vue-echarts | ^6.6.8 | ECharts的Vue组件封装 |
| Pinia | ^2.1.7 | Vue状态管理 |
| Vue Router | ^4.3.0 | Vue路由管理 |
| Axios | ^1.6.7 | HTTP客户端 |

## 项目结构

```
frontend/
├── src/
│   ├── api/                 # API请求模块
│   │   ├── index.ts         # Axios实例配置 & 类型定义
│   │   ├── auth.ts          # 认证相关API
│   │   └── dashboard.ts     # 看板数据API
│   ├── assets/              # 静态资源
│   ├── components/          # 通用组件
│   ├── composables/         # 组合式函数
│   ├── layouts/             # 布局组件
│   │   └── MainLayout.vue   # 主布局
│   ├── router/              # 路由配置
│   ├── stores/              # Pinia状态管理
│   ├── types/               # TypeScript类型定义
│   ├── utils/               # 工具函数
│   ├── views/               # 页面视图
│   │   ├── HomeView.vue     # 首页/落地页
│   │   └── DashboardView.vue # 数据看板
│   ├── App.vue
│   ├── main.ts              # 应用入口
│   └── env.d.ts
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

## 快速开始

### 环境要求

- Node.js >= 18.0.0
- npm >= 9.0.0

### 安装依赖

```bash
cd frontend
npm install
```

### 开发模式启动

```bash
npm run dev
```

访问 http://localhost:5173

### 生产构建

```bash
npm run build
```

构建产物将输出到 `dist/` 目录。

### 预览构建结果

```bash
npm run preview
```

## API 接口预留

### 基础配置

- **Base URL**: `/api`
- **代理目标**: `http://localhost:8000`
- **超时时间**: 10000ms
- **认证方式**: Bearer Token

### 接口列表

#### 认证模块 `/api/auth`

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/auth/login` | 用户登录 |
| POST | `/auth/logout` | 用户登出 |
| GET | `/auth/user` | 获取用户信息 |
| POST | `/auth/refresh` | 刷新Token |

**登录请求示例:**
```json
POST /api/auth/login
{
  "username": "admin",
  "password": "password"
}
```

**登录响应示例:**
```json
{
  "code": 0,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com"
    }
  },
  "message": "success"
}
```

#### 看板模块 `/api/dashboard`

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/dashboard/data` | 获取完整看板数据 |
| GET | `/dashboard/stats` | 获取统计指标 |
| GET | `/dashboard/visit-trend` | 获取访问趋势 |
| GET | `/dashboard/region` | 获取地区分布 |
| GET | `/dashboard/traffic-sources` | 获取流量来源 |
| GET | `/dashboard/realtime` | 获取实时数据 |

**获取完整看板数据响应示例:**
```json
{
  "code": 0,
  "data": {
    "stats": {
      "totalVisits": 128956,
      "activeUsers": 8846,
      "avgDuration": "3分42秒",
      "conversionRate": 3.28,
      "trends": {
        "visitsTrend": "+12.5%",
        "usersTrend": "+8.2%",
        "durationTrend": "+2.1%",
        "conversionTrend": "-0.3%"
      }
    },
    "visitTrend": [
      { "date": "Mon", "value": 820 },
      { "date": "Tue", "value": 932 }
    ],
    "regionDistribution": [
      { "region": "北京", "value": 1200 },
      { "region": "上海", "value": 1800 }
    ],
    "trafficSources": [
      { "name": "搜索引擎", "value": 1048 },
      { "name": "直接访问", "value": 735 }
    ],
    "realTimeUsers": [
      { "date": "00:00", "value": 120 },
      { "date": "04:00", "value": 200 }
    ]
  },
  "message": "success"
}
```

## 代理配置

Vite 开发服务器配置了代理，将 `/api` 请求转发到后端服务器：

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

生产环境需要配置 Nginx 或其他反向代理服务器。

## 路径别名

项目配置了 `@` 指向 `src` 目录：

```typescript
// vite.config.ts
resolve: {
  alias: {
    '@': resolve(__dirname, 'src')
  }
}
```

使用示例：
```typescript
import HomeView from '@/views/HomeView.vue'
import { getUserInfo } from '@/api/user'
```

## 全局组件注册

### Element Plus 图标

所有 Element Plus 图标已全局注册，可直接使用：

```vue
<el-icon><DataAnalysis /></el-icon>
<el-icon><User /></el-icon>
<el-icon><Clock /></el-icon>
```

### ECharts 组件

`v-chart` 组件已全局注册：

```vue
<v-chart :option="chartOptions" autoresize />
```

## 状态管理 (Pinia)

### 创建 Store

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const increment = () => count.value++
  return { count, increment }
})
```

### 使用 Store

```typescript
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()
counter.increment()
```

## 路由配置

路由定义在 `src/router/index.ts`：

```typescript
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue')
  }
]
```

## 样式说明

项目使用朴素白色主题：

| 元素 | 颜色 |
|------|------|
| 背景 | `#f8fafc` |
| 卡片 | `white` |
| 边框 | `#e2e8f0` |
| 主文字 | `#1e293b` |
| 次要文字 | `#64748b` |
| 主题色 | `#667eea` |

## 构建说明

### 1. 安装依赖

```bash
npm install
```

### 2. 配置后端API

确保后端服务运行在 http://localhost:8000，或修改 `vite.config.ts` 中的代理配置。

### 3. 启动开发服务器

```bash
npm run dev
```

### 4. 生产构建

```bash
npm run build
```

### 5. 预览生产构建

```bash
npm run preview
```

## 生产部署注意事项

1. **API 代理**: 生产环境需要配置 Nginx 反向代理：

```nginx
location /api {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

2. **构建产物**: `dist/` 目录可部署到任何静态文件服务器

3. **SPA fallback**: Vue Router 使用 history 模式时，需要配置 Nginx 指向 index.html

## 许可证

MIT
