<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const dialogVisible = ref(false)
const editMode = ref(false)

const formRef = ref<FormInstance>()

const filters = reactive({
  name: '',
  college: '',
  status: ''
})

const studentList = ref([
  {
    id: 1,
    name: '张三',
    studentId: '2020010001',
    college: '计算机学院',
    major: '计算机科学与技术',
    class: '计科2020-1班',
    phone: '13800138001',
    status: '已签约',
    company: '阿里巴巴',
    salary: 25000
  },
  {
    id: 2,
    name: '李四',
    studentId: '2020010002',
    college: '软件学院',
    major: '软件工程',
    class: '软工2020-1班',
    phone: '13800138002',
    status: '已签约',
    company: '字节跳动',
    salary: 30000
  },
  {
    id: 3,
    name: '王五',
    studentId: '2020010003',
    college: '信息工程学院',
    major: '电子信息工程',
    class: '电信2020-1班',
    phone: '13800138003',
    status: '求职中',
    company: '-',
    salary: 0
  },
  {
    id: 4,
    name: '赵六',
    studentId: '2020010004',
    college: '机械工程学院',
    major: '机械设计',
    class: '机械2020-1班',
    phone: '13800138004',
    status: '未签约',
    company: '-',
    salary: 0
  }
])

const formData = reactive({
  name: '',
  studentId: '',
  college: '',
  major: '',
  class: '',
  phone: '',
  status: '',
  company: '',
  salary: 0
})

const statusOptions = [
  { value: '已签约', label: '已签约' },
  { value: '求职中', label: '求职中' },
  { value: '未签约', label: '未签约' },
  { value: '考研', label: '考研' },
  { value: '出国', label: '出国' }
]

const collegeOptions = [
  { value: '计算机学院', label: '计算机学院' },
  { value: '软件学院', label: '软件学院' },
  { value: '信息工程学院', label: '信息工程学院' },
  { value: '机械工程学院', label: '机械工程学院' },
  { value: '经济管理学院', label: '经济管理学院' }
]

const rules: FormRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  studentId: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  college: [{ required: true, message: '请选择学院', trigger: 'change' }]
}

const handleSearch = () => {
  ElMessage.success('搜索功能开发中')
}

const handleReset = () => {
  filters.name = ''
  filters.college = ''
  filters.status = ''
}

const handleAdd = () => {
  editMode.value = false
  formData.name = ''
  formData.studentId = ''
  formData.college = ''
  formData.major = ''
  formData.class = ''
  formData.phone = ''
  formData.status = ''
  formData.company = ''
  formData.salary = 0
  dialogVisible.value = true
}

const handleEdit = (row: typeof studentList.value[0]) => {
  editMode.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

const handleDelete = (_row: typeof studentList.value[0]) => {
  ElMessageBox.confirm('确定要删除该学生信息吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
  })
}

const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate((valid) => {
    if (valid) {
      ElMessage.success(editMode.value ? '修改成功' : '添加成功')
      dialogVisible.value = false
    }
  })
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}
</script>

<template>
  <div class="students-page">
    <div class="page-header">
      <h2>学生管理</h2>
      <p class="page-desc">管理学校学生的就业信息</p>
    </div>

    <!-- Filters -->
    <div class="filters-card">
      <el-form :model="filters" inline>
        <el-form-item label="姓名">
          <el-input v-model="filters.name" placeholder="请输入姓名" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="学院">
          <el-select v-model="filters.college" placeholder="请选择" clearable style="width: 150px">
            <el-option
              v-for="opt in collegeOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="请选择" clearable style="width: 120px">
            <el-option
              v-for="opt in statusOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div class="table-header">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          添加学生
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>

      <el-table :data="studentList" stripe>
        <el-table-column prop="name" label="姓名" width="80" />
        <el-table-column prop="studentId" label="学号" width="120" />
        <el-table-column prop="college" label="学院" width="120" />
        <el-table-column prop="major" label="专业" />
        <el-table-column prop="class" label="班级" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag
              :type="row.status === '已签约' ? 'success' : row.status === '未签约' ? 'danger' : 'warning'"
              size="small"
            >
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="company" label="签约公司" />
        <el-table-column prop="salary" label="薪资" width="100" align="center">
          <template #default="{ row }">
            {{ row.salary > 0 ? row.salary.toLocaleString() : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" text @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" text @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :total="100"
          :page-size="10"
        />
      </div>
    </div>

    <!-- Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="editMode ? '编辑学生' : '添加学生'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="formData.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="学号" prop="studentId">
          <el-input v-model="formData.studentId" placeholder="请输入学号" />
        </el-form-item>
        <el-form-item label="学院" prop="college">
          <el-select v-model="formData.college" placeholder="请选择" style="width: 100%">
            <el-option
              v-for="opt in collegeOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="专业" prop="major">
          <el-input v-model="formData.major" placeholder="请输入专业" />
        </el-form-item>
        <el-form-item label="班级" prop="class">
          <el-input v-model="formData.class" placeholder="请输入班级" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" placeholder="请选择" style="width: 100%">
            <el-option
              v-for="opt in statusOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="签约公司">
          <el-input v-model="formData.company" placeholder="请输入签约公司" />
        </el-form-item>
        <el-form-item label="薪资">
          <el-input-number v-model="formData.salary" :min="0" :step="1000" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.students-page {
  max-width: 1400px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.page-desc {
  color: #64748b;
  font-size: 14px;
}

.filters-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.table-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.table-header {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
