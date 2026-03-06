// ---------- Domain types ----------

export interface Article {
  id: number
  title: string
  content: string
  created_at: string
  updated_at: string
}

export interface Comment {
  id: number
  article_id: number
  commenter: string
  content: string
  created_at: string
}

// ---------- Paginated response wrappers ----------

export interface PaginatedArticles {
  articles: Article[]
  total: number
  page: number
  per_page: number
  total_pages: number
}

export interface PaginatedComments {
  comments: Comment[]
  total: number
  page: number
  per_page: number
  total_pages: number
}

// ---------- Request payloads ----------

export interface ArticlePayload {
  title: string
  content: string
}

export interface CommentPayload {
  commenter: string
  content: string
}
