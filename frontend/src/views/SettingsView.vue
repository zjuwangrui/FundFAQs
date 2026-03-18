<template>
  <div class="settings-view">
    <!-- Nav -->
    <div class="detail-nav">
      <router-link to="/" class="link-back">← 返回首页</router-link>
    </div>

    <div class="settings-card">
      <h1 class="settings-card__title">邮箱配置 (管理员)</h1>
      <p class="hint">配置用于发送评论提醒邮件的发件箱。目前支持 QQ、163、Gmail 等常见邮箱。</p>

      <div class="form-group">
        <label>管理员密钥 (Secret)</label>
        <input v-model="secret" type="password" placeholder="请输入管理员密钥" class="input-field" />
      </div>

      <div class="form-group">
        <label>邮箱地址</label>
        <input v-model="email" type="email" placeholder="例如: example@163.com" class="input-field" />
      </div>

      <div class="form-group">
        <label>
          授权码 / 密码
          <span class="small-hint">(请使用邮箱生成的专用授权码，非登录密码)</span>
        </label>
        <input v-model="authCode" type="password" placeholder="请输入 SMTP 授权码" class="input-field" />
      </div>
      
      <div v-if="message" :class="['message-box', isError ? 'error' : 'success']">
        {{ message }}
      </div>

      <div class="form-actions">
        <button class="btn btn-primary" :disabled="submitting" @click="handleSave">
          {{ submitting ? '验证并保存...' : '保存配置' }}
        </button>
      </div>

      <div class="help-links">
        <p>如何获取授权码？</p>
        <ul>
          <li><a href="https://service.mail.qq.com/detail/0/75" target="_blank">QQ邮箱获取授权码帮助</a></li>
          <li><a href="https://help.mail.163.com/faqDetail.do?code=d7a5dc8471cd0c0e8b4b8f4f8e4f9b1e" target="_blank">163邮箱获取授权码帮助</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { systemApi } from '../api'

const secret = ref('')
const email = ref('')
const authCode = ref('')
const submitting = ref(false)
const message = ref('')
const isError = ref(false)

async function handleSave() {
  if (!secret.value) {
    message.value = '请输入管理员密钥'
    isError.value = true
    return
  }
  if (!email.value || !authCode.value) {
    message.value = '请完整填写邮箱和授权码'
    isError.value = true
    return
  }

  submitting.value = true
  message.value = ''
  isError.value = false

  try {
    const { data } = await systemApi.updateEmailConfig(email.value, authCode.value, secret.value)
    message.value = data.message || '配置成功！'
    isError.value = false
  } catch (err: any) {
    console.error(err)
    isError.value = true
    message.value = err.response?.data?.error || '配置失败，请检查密钥或网络'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.settings-view {
  max-width: 600px;
  margin: 40px auto;
  padding: 0 20px;
}

.detail-nav {
  margin-bottom: 20px;
}

.link-back {
  color: #666;
  text-decoration: none;
  font-size: 0.95rem;
}

.link-back:hover {
  text-decoration: underline;
  color: #1a73e8;
}

.settings-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.settings-card__title {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1.5rem;
  color: #333;
}

.hint {
  color: #666;
  margin-bottom: 30px;
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.small-hint {
  font-weight: normal;
  font-size: 0.85rem;
  color: #888;
  margin-left: 5px;
}

.input-field {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.input-field:focus {
  border-color: #1a73e8;
}

.form-actions {
  margin-top: 30px;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-primary {
  background-color: #1a73e8;
  color: white;
  width: 100%;
}

.btn-primary:disabled {
  background-color: #a0c3ff;
  cursor: not-allowed;
}

.message-box {
  margin-top: 20px;
  padding: 10px;
  border-radius: 6px;
  font-size: 0.95rem;
}

.message-box.success {
  background-color: #e6f4ea;
  color: #137333;
}

.message-box.error {
  background-color: #fce8e6;
  color: #c5221f;
}

.help-links {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.help-links p {
  font-weight: bold;
  color: #555;
  margin-bottom: 10px;
}

.help-links ul {
  padding-left: 20px;
  margin: 0;
}

.help-links li {
  margin-bottom: 5px;
}

.help-links a {
  color: #1a73e8;
  text-decoration: none;
}

.help-links a:hover {
  text-decoration: underline;
}
</style>