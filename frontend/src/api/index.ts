import axios from 'axios'
import type {
  Article,
  ArticlePayload,
  Comment,
  CommentPayload,
  PaginatedArticles,
  PaginatedComments,
} from '../types'

const http = axios.create({ baseURL: '/api' })

// ---------- Articles ----------

export const articleApi = {
  getAll: (page = 1, perPage = 10) =>
    http.get<PaginatedArticles>('/articles', {
      params: { page, per_page: perPage },
    }),

  getById: (id: number) => http.get<Article>(`/articles/${id}`),

  create: (payload: ArticlePayload) => http.post<Article>('/articles', payload),

  // 仅管理员可编辑：需要附带 secret
  update: (id: number, payload: ArticlePayload & { secret: string }) =>
    http.put<Article>(`/articles/${id}`, payload),

  // 仅管理员可删除：需要附带 secret
  remove: (id: number, secret: string) =>
    http.delete<{ message: string }>(`/articles/${id}`, {
      data: { secret },
    }),

  search: (q: string, page = 1, perPage = 10) =>
    http.get<PaginatedArticles>('/articles/search', {
      params: { q, page, per_page: perPage },
    }),
}

// ---------- Comments ----------

export const commentApi = {
  getByArticle: (articleId: number, page = 1, perPage = 20) =>
    http.get<PaginatedComments>(`/articles/${articleId}/comments`, {
      params: { page, per_page: perPage },
    }),

  create: (articleId: number, payload: CommentPayload) =>
    http.post<Comment>(`/articles/${articleId}/comments`, payload),

  remove: (articleId: number, commentId: number, secret: string) =>
    http.delete<{ message: string }>(`/articles/${articleId}/comments/${commentId}`, {
      data: { secret },
    }),
}
