<template>
  <div id="app-root">
    <header class="site-header">
      <div class="header-inner">
        <router-link to="/" class="site-name">资助政策答疑</router-link>
      </div>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="site-footer">
      <p>© 2026 资助政策答疑 · 所有文章均欢迎评论</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Global shell — no local state needed
</script>
