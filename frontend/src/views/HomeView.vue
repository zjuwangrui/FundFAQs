<template>
  <div class="home-view">
    <!-- Hero -->
    <div class="page-hero">
      <h1 class="site-title">资助政策答疑</h1>
      <p class="site-subtitle">汇集资助政策相关问题与解答，帮助您快速找到答案</p>
    </div>

    <!-- Search Bar -->
    <div class="search-section">
      <div class="search-wrapper">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索文章标题或内容..."
          class="search-input"
          @keyup.enter="handleSearch"
        />
        <button class="btn btn-primary" @click="handleSearch">搜索</button>
        <button v-if="isSearching" class="btn btn-secondary" @click="clearSearch">清除</button>
      </div>
    </div>

    <!-- Action Bar -->
    <div class="action-bar">
      <span class="result-hint">
        <template v-if="isSearching">
          搜索「{{ activeQuery }}」共找到 <strong>{{ total }}</strong> 篇文章
        </template>
        <template v-else>
          共 <strong>{{ total }}</strong> 篇文章
        </template>
      </span>
      <router-link to="/article/new" class="btn btn-primary publish-btn">+ 发布文章</router-link>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="state-box">加载中...</div>

    <!-- Empty -->
    <div v-else-if="articles.length === 0" class="state-box empty">
      {{ isSearching ? '未找到相关文章，试试其他关键词？' : '暂无文章，点击「发布文章」开始创作吧！' }}
    </div>

    <!-- Article Cards -->
    <div v-else class="article-list">
      <article
        v-for="article in articles"
        :key="article.id"
        class="article-card"
        @click="goToArticle(article.id)"
      >
        <h2 class="article-card__title">{{ article.title }}</h2>
        <p class="article-card__excerpt">{{ getExcerpt(article.content) }}</p>
        <div class="article-card__meta">
          <span>{{ formatDate(article.created_at) }}</span>
        </div>
      </article>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button
        class="page-btn"
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        &lsaquo;
      </button>
      <button
        v-for="p in totalPages"
        :key="p"
        :class="['page-btn', { active: p === currentPage }]"
        @click="changePage(p)"
      >
        {{ p }}
      </button>
      <button
        class="page-btn"
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        &rsaquo;
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { articleApi } from '../api'
import type { Article } from '../types'

const router = useRouter()

const articles = ref<Article[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const totalPages = ref(1)

const searchQuery = ref('')
const activeQuery = ref('')
const isSearching = ref(false)

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

function getExcerpt(content: string): string {
  const stripped = content.replace(/[#*`_[\]!>]/g, '').replace(/\n+/g, ' ').trim()
  return stripped.length > 160 ? stripped.slice(0, 160) + '…' : stripped
}

async function loadArticles(page = 1) {
  loading.value = true
  try {
    const { data } = await articleApi.getAll(page, 10)
    articles.value = data.articles
    total.value = data.total
    totalPages.value = data.total_pages
    currentPage.value = page
  } catch {
    articles.value = []
  } finally {
    loading.value = false
  }
}

async function doSearch(page = 1) {
  loading.value = true
  try {
    const { data } = await articleApi.search(activeQuery.value, page, 10)
    articles.value = data.articles
    total.value = data.total
    totalPages.value = data.total_pages
    currentPage.value = page
  } catch {
    articles.value = []
  } finally {
    loading.value = false
  }
}

async function handleSearch() {
  const q = searchQuery.value.trim()
  if (!q) {
    clearSearch()
    return
  }
  activeQuery.value = q
  isSearching.value = true
  await doSearch(1)
}

function clearSearch() {
  searchQuery.value = ''
  activeQuery.value = ''
  isSearching.value = false
  loadArticles(1)
}

function changePage(page: number) {
  if (isSearching.value) {
    doSearch(page)
  } else {
    loadArticles(page)
  }
}

function goToArticle(id: number) {
  router.push(`/article/${id}`)
}

onMounted(() => loadArticles())
</script>
