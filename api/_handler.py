"""Vercel Python Functions가 공유하는 민원 FAQ 요청 처리기."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from typing import Any

from server import ConfigurationError, SearchService, has_sensitive_data


class ApiHandler(BaseHTTPRequestHandler):
    operation = "answer"
    _service: SearchService | None = None

    def log_message(self, format: str, *args: Any) -> None:
        # 질문·인증 정보가 Vercel 런타임 로그에 남지 않도록 요청 로그를 비활성화한다.
        return

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @classmethod
    def service(cls) -> SearchService:
        if cls._service is None:
            cls._service = SearchService()
        return cls._service

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Allow", "POST, OPTIONS")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def do_GET(self) -> None:
        self.send_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "POST 요청만 지원합니다."})

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 4096:
                raise ValueError("요청 크기가 올바르지 않습니다.")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            question = str(payload.get("question", "")).strip()
            if not 10 <= len(question) <= 300:
                raise ValueError("질문을 10~300자로 입력해 주세요.")
            if has_sensitive_data(question):
                raise ValueError("개인정보로 보이는 숫자를 지운 뒤 다시 질문해 주세요.")

            service = self.service()
            result = (
                service.answer(question)
                if self.operation == "answer"
                else service.search(question)
            )
            self.send_json(HTTPStatus.OK, result)
        except (ValueError, json.JSONDecodeError) as error:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except ConfigurationError:
            self.send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {"error": "검색 서비스 설정을 확인해 주세요."},
            )
        except RuntimeError:
            self.send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {"error": "잠시 후 다시 시도해 주세요"},
            )
        except Exception:
            self.send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "잠시 후 다시 시도해 주세요"},
            )
