"""카테고리 우선·전체 폴백 FAQ 검색을 제공하는 Vercel Function."""

from api._handler import ApiHandler


class handler(ApiHandler):
    operation = "search"
