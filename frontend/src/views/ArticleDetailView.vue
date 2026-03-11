<template>
  <div class="article-detail">
    <!-- Loading -->
    <div v-if="loading" class="state-box">加载中...</div>

    <!-- Not found -->
    <div v-else-if="!article" class="state-box empty">文章不存在或已被删除。</div>

    <!-- Content -->
    <template v-else>
      <!-- Back + Admin Actions -->
      <div class="detail-nav">
        <router-link to="/" class="link-back">← 返回列表</router-link>

        <!-- 仅管理员（解锁后）可见编辑 / 删除按钮 -->
        <div class="detail-actions">
          <button
            v-if="!isAdmin"
            type="button"
            class="btn btn-secondary btn-sm"
            @click="unlockWithKey"
          >
            管理员解锁
          </button>
          <template v-else>
            <router-link
              :to="`/article/${article.id}/edit`"
              class="btn btn-outline btn-sm"
            >
              编辑文章
            </router-link>
            <button
              type="button"
              class="btn btn-danger btn-sm"
              @click="confirmDelete"
            >
              删除文章
            </button>
          </template>
        </div>
      </div>

      <!-- Header -->
      <header class="article-header">
        <h1 class="article-header__title">{{ article.title }}</h1>
        <div class="article-header__meta">
          <span>发布于 {{ formatDate(article.created_at) }}</span>
          <span v-if="article.updated_at !== article.created_at">
            · 更新于 {{ formatDate(article.updated_at) }}
          </span>
        </div>
      </header>

      <!-- Markdown Body -->
      <section class="markdown-body" v-html="renderedContent" />

      <!-- Comments -->
      <section class="comments-section">
        <h2 class="comments-section__title">评论（{{ totalComments }}）</h2>

        <!-- Comment Form -->
        <div class="comment-form">
          <input
            v-model="commentForm.commenter"
            type="text"
            placeholder="你的昵称（可选，默认匿名）"
            class="form-input"
            maxlength="50"
          />
          <textarea
            v-model="commentForm.content"
            placeholder="写下你的评论..."
            class="form-textarea"
            rows="4"
            maxlength="1000"
          />
          <div class="comment-form__footer">
            <span class="char-count">{{ commentForm.content.length }} / 1000</span>
            <button
              class="btn btn-primary"
              :disabled="submitting"
              @click="submitComment"
            >
              {{ submitting ? '提交中...' : '发表评论' }}
            </button>
          </div>
        </div>

        <!-- Loading comments -->
        <div v-if="commentsLoading" class="state-box">加载评论中...</div>

        <!-- Empty comments -->
        <div v-else-if="comments.length === 0" class="state-box empty">
          暂无评论，来发表第一条评论吧！
        </div>

        <!-- Comments List -->
        <div v-else class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-item__header">
              <span class="comment-item__author">{{ comment.commenter }}</span>
              <span class="comment-item__time">{{ formatDate(comment.created_at) }}</span>
              <button
                v-if="isAdmin"
                type="button"
                class="btn btn-link btn-xs comment-delete-btn"
                @click="confirmDeleteComment(comment.id)"
              >
                删除
              </button>
            </div>
            <p class="comment-item__content">{{ comment.content }}</p>
          </div>
        </div>

        <!-- Comment Pagination -->
        <div v-if="commentTotalPages > 1" class="pagination">
          <button
            class="page-btn"
            :disabled="commentPage === 1"
            @click="loadComments(commentPage - 1)"
          >
            &lsaquo;
          </button>
          <button
            v-for="p in commentTotalPages"
            :key="p"
            :class="['page-btn', { active: p === commentPage }]"
            @click="loadComments(p)"
          >
            {{ p }}
          </button>
          <button
            class="page-btn"
            :disabled="commentPage === commentTotalPages"
            @click="loadComments(commentPage + 1)"
          >
            &rsaquo;
          </button>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DOMPurify from 'dompurify'
import { marked } from 'marked'
import { articleApi, commentApi } from '../api'
import type { Article, Comment } from '../types'

const route = useRoute()
const articleId = computed(() => Number(route.params.id))

// ---------- 管理 / 编辑权限 ----------
// 进入页面时，如果本标签页已经解锁过管理员模式，则自动恢复
const isAdmin = ref(!!sessionStorage.getItem('fund_faq_admin_secret'))

function unlockWithKey() {
  const input = window.prompt('请输入管理密钥：')
  if (!input) return

  // 不在前端校验密钥，仅在本地做一次标记，真正校验在后端接口
  sessionStorage.setItem('fund_faq_admin_secret', input)
  isAdmin.value = true
  alert('已进入管理员模式，可以编辑和删除文章。')
}

function confirmDelete() {
  if (!window.confirm('确定要删除这篇文章吗？此操作不可恢复。')) {
    return
  }
  const secret = sessionStorage.getItem('fund_faq_admin_secret') ?? ''
  if (!secret) {
    alert('当前未处于管理员模式，请先通过管理密钥解锁。')
    return
  }

  articleApi
    .remove(articleId.value, secret)
    .then(() => {
      alert('文章已删除')
      window.location.href = '/'
    })
    .catch((err: unknown) => {
      const msg =
        err && typeof err === 'object' && 'response' in err
          ? (err as { response?: { data?: { error?: string } } }).response?.data?.error
          : undefined
      alert(msg ?? '删除失败，请稍后再试')
    })
}

function confirmDeleteComment(commentId: number) {
  if (!window.confirm('确定要删除这条评论吗？此操作不可恢复。')) {
    return
  }
  const secret = sessionStorage.getItem('fund_faq_admin_secret') ?? ''
  if (!secret) {
    alert('当前未处于管理员模式，请先通过管理密钥解锁。')
    return
  }

  commentApi
    .remove(articleId.value, commentId, secret)
    .then(() => {
      alert('评论已删除')
      loadComments(commentPage.value)
    })
    .catch((err: unknown) => {
      const msg =
        err && typeof err === 'object' && 'response' in err
          ? (err as { response?: { data?: { error?: string } } }).response?.data?.error
          : undefined
      alert(msg ?? '删除评论失败，请稍后再试')
    })
}

// ---------- Article ----------
const article = ref<Article | null>(null)
const loading = ref(false)
const renderedContent = ref('')

async function loadArticle() {
  loading.value = true
  try {
    const { data } = await articleApi.getById(articleId.value)
    article.value = data
  } catch {
    article.value = null
  } finally {
    loading.value = false
  }
}

watch(
  article,
  async (a) => {
    if (!a) {
      renderedContent.value = ''
      return
    }
    const raw = await Promise.resolve(marked.parse(a.content, { async: false }))
    renderedContent.value = DOMPurify.sanitize(raw as string)
  },
  { immediate: true },
)

// ---------- Comments ----------
const comments = ref<Comment[]>([])
const commentsLoading = ref(false)
const totalComments = ref(0)
const commentPage = ref(1)
const commentTotalPages = ref(1)

const commentForm = ref({ commenter: '', content: '' })
const submitting = ref(false)

async function loadComments(page = 1) {
  commentsLoading.value = true
  try {
    const { data } = await commentApi.getByArticle(articleId.value, page, 20)
    comments.value = data.comments
    totalComments.value = data.total
    commentTotalPages.value = data.total_pages
    commentPage.value = page
  } catch {
    comments.value = []
  } finally {
    commentsLoading.value = false
  }
}

async function submitComment() {
  if (!commentForm.value.content.trim()) {
    alert('请填写评论内容')
    return
  }
  submitting.value = true
  try {
    await commentApi.create(articleId.value, {
      commenter: commentForm.value.commenter.trim() || '匿名',
      content: commentForm.value.content.trim(),
    })
    commentForm.value.content = ''
    await loadComments(1)
  } catch (err: unknown) {
    const msg =
      err && typeof err === 'object' && 'response' in err
        ? (err as { response?: { data?: { error?: string } } }).response?.data?.error
        : undefined
    alert(msg ?? '评论提交失败，请稍后再试')
  } finally {
    submitting.value = false
  }
}

// ---------- Helpers ----------
function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(() => {
  loadArticle()
  loadComments()
})
</script>
