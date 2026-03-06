<template>
  <div class="edit-view">
    <!-- Nav -->
    <div class="detail-nav">
      <router-link to="/" class="link-back">← 返回列表</router-link>
    </div>

    <div class="edit-card">
      <h1 class="edit-card__title">{{ isEditing ? '编辑文章' : '发布新文章' }}</h1>

      <!-- Title -->
      <input
        v-model="form.title"
        type="text"
        placeholder="请输入文章标题..."
        class="title-input"
        maxlength="200"
      />

      <!-- Markdown Editor -->
      <MdEditor
        v-model="form.content"
        language="zh-CN"
        :style="{ height: '520px' }"
        :toolbars="toolbars"
        placeholder="请使用 Markdown 格式输入文章内容..."
      />

      <!-- Actions -->
      <div class="form-actions">
        <router-link to="/" class="btn btn-outline">取消</router-link>
        <button class="btn btn-primary" :disabled="submitting" @click="handleSubmit">
          {{ submitting ? '提交中...' : isEditing ? '保存修改' : '发布文章' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdEditor } from 'md-editor-v3'
import type { ToolbarNames } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { articleApi } from '../api'

const route = useRoute()
const router = useRouter()

const isEditing = computed(() => !!route.params.id)
const articleId = computed(() => Number(route.params.id))

const form = ref({ title: '', content: '' })
const submitting = ref(false)

const toolbars: ToolbarNames[] = [
  'bold',
  'underline',
  'italic',
  'strikeThrough',
  '-',
  'title',
  'quote',
  'unorderedList',
  'orderedList',
  'task',
  '-',
  'codeRow',
  'code',
  'link',
  'image',
  'table',
  '-',
  'revoke',
  'next',
  '=',
  'preview',
  'fullscreen',
]

async function loadArticle() {
  if (!isEditing.value) return
  try {
    const { data } = await articleApi.getById(articleId.value)
    form.value.title = data.title
    form.value.content = data.content
  } catch {
    router.push('/')
  }
}

async function handleSubmit() {
  if (!form.value.title.trim()) {
    alert('请填写文章标题')
    return
  }
  if (!form.value.content.trim()) {
    alert('请填写文章内容')
    return
  }

  submitting.value = true
  try {
    if (isEditing.value) {
      await articleApi.update(articleId.value, {
        title: form.value.title.trim(),
        content: form.value.content.trim(),
      })
      router.push(`/article/${articleId.value}`)
    } else {
      const { data } = await articleApi.create({
        title: form.value.title.trim(),
        content: form.value.content.trim(),
      })
      router.push(`/article/${data.id}`)
    }
  } catch (err: unknown) {
    const msg =
      err && typeof err === 'object' && 'response' in err
        ? (err as { response?: { data?: { error?: string } } }).response?.data?.error
        : undefined
    alert(msg ?? '提交失败，请稍后再试')
  } finally {
    submitting.value = false
  }
}

onMounted(loadArticle)
</script>
