"""검색된 FAQ만 근거로 최종 답변을 생성하는 Vercel Function."""

from api._handler import ApiHandler


class handler(ApiHandler):
    operation = "answer"
