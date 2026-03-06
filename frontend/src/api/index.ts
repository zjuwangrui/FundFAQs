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

  update: (id: number, payload: ArticlePayload) =>
    http.put<Article>(`/articles/${id}`, payload),

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
}
