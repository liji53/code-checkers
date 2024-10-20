<template>
  <div class="main_div">
    <el-container>
      <el-header>
        <el-text
          >这是一个基于 clang 的静态检查工具所构建的 C++ 代码检查网站， 支持
          <el-link
            type="primary"
            target="_blank"
            href="https://clang.llvm.org/extra/clang-tidy/checks/list.html"
            >clang默认检查器</el-link
          >
          以及自定义检查器如：
          <el-tag type="primary">函数禁用</el-tag>
          <el-tag type="primary">精度丢失</el-tag>
          <el-tag type="primary">事务忘提交</el-tag>
          等
        </el-text>
      </el-header>
      <el-main>
        <el-form ref="formRef" :model="form" label-width="100px" :rules="rules">
          <el-form-item label="编程语言">
            <el-select v-model="form.language" placeholder="请选择编程语言">
              <el-option
                v-for="item in languageOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="检查器" prop="checkerName">
            <el-select v-model="form.checkerName" placeholder="请选择检查器">
              <el-option
                v-for="item in checkerOptions"
                :key="item.value"
                :label="item.name"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="代码文件">
            <el-upload
              ref="uploadRef"
              v-model:file-list="fileList"
              drag
              multiple
              show-file-list
              style="width: 100%"
              action="/api/v1/code/upload"
              :data="uploadFileName"
              :before-upload="onBeforeUpload"
              :on-remove="onFileRemove"
              :on-success="onUploadSuccess"
              :on-error="onUploadError"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">请上传代码<em>click to upload</em></div>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit(formRef)">开始检查</el-button>
            <el-button @click="onClear">清空上传文件</el-button>
          </el-form-item>
        </el-form>
        <el-text>检查结果</el-text>
        <el-input type="textarea" v-model="checkResult" autosize></el-input>
      </el-main>
      <el-footer>
        <el-text>
          如果觉得不错，请前往<el-link
            type="primary"
            href="https://gitee.com/liji1211/code-checkers"
            >项目地址</el-link
          >, 帮我点个赞 </el-text
        ><br />
        <el-text>联系方式：liji_1211@163.com</el-text>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { getCheckers, deleteFile, type checkerItem } from '@/api/codeCheck'
import { UploadFilled } from '@element-plus/icons-vue'
import type { UploadProps, FormInstance, ElUpload, UploadUserFile } from 'element-plus'
import { ElMessage } from 'element-plus'

const form = reactive({
  language: 'C++',
  checkerName: ''
})
const languageOptions = ref([
  {
    value: 'C++',
    label: 'C++'
  }
])
const checkerOptions = ref<checkerItem[]>([])

const uploadRef = ref<InstanceType<typeof ElUpload> | null>(null)
const formRef = ref<FormInstance>()
const rules = reactive({
  checkerName: [{ required: true, message: '请选择检查器', trigger: 'blur' }]
})

const fileList = ref<UploadUserFile[]>([])
const uploadFileName = reactive({ filename: '' })
const uuid = ref('')
const checkResult = ref('')
var ws = new WebSocket('ws://60.204.224.115:80/ws')
ws.onmessage = function (event) {
  ElMessage.success('检查结束，请查看检查结果!')
  checkResult.value = event.data
}

const onBeforeUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('文件大小不能超过2M!')
    return false
  }
  uploadFileName.filename = rawFile.name
  return true
}
const onFileRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
  deleteFile({
    filename: file.name,
    uuid: uuid.value
  })
}
const onUploadSuccess: UploadProps['onSuccess'] = async (response, uploadFile, uploadFiles) => {
  uuid.value = response.uuid
}
const onUploadError: UploadProps['onError'] = (error, uploadFile, uploadFiles) => {
  ElMessage.error('文件上传失败，请重试!')
}

const onSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      if (uploadRef.value?.$props.fileList?.length === 0) {
        ElMessage.error(`请先上传文件!`)
        return
      }
      ws.send(
        JSON.stringify({
          ...form,
          uuid: uuid.value
        })
      )
    }
  })
}
const onClear = () => {
  deleteFile({
    uuid: uuid.value
  })
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}

onMounted(() => {
  getCheckers({ language: 'C++' }).then((response) => {
    checkerOptions.value = response.data.data
    console.log(checkerOptions.value)
  })
})
</script>

<style scoped>
.main_div {
  background-color: #e0f2e9;
  margin: -8px;
  position: absolute;
  width: 100%;
  min-height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
