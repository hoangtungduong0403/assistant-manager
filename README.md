<!-- agents/: Calendar, Email, Meeting, Task...
tools/: Gmail, Calendar, Drive, Teams, Slack...
planner/: lập kế hoạch khi nhận yêu cầu.
evaluator/: tự kiểm tra kết quả trước khi trả lời.
memory/: lưu trạng thái, sở thích, ngữ cảnh công việc.
knowledge/: RAG từ tài liệu doanh nghiệp.
workflows/: các quy trình nhiều bước (chuẩn bị họp, báo cáo tuần...). -->


# Executive Assistant Platform

## Giới thiệu

Executive Assistant Platform là hệ thống AI Agent hỗ trợ Ban Giám đốc trong các nghiệp vụ hằng ngày.

Hệ thống được xây dựng theo kiến trúc Mission-based, trong đó mỗi Mission giải quyết một nghiệp vụ độc lập.

---

## Mục tiêu

- Chuẩn hóa quy trình làm việc
- Tự động hóa nghiệp vụ
- Giảm thao tác thủ công
- Lưu trữ tri thức doanh nghiệp
- Hỗ trợ ra quyết định

---

## Kiến trúc

profiles/
missions/
templates/
artifacts/
knowledge/
shared/

---

## Cấu trúc Mission

Mỗi Mission bao gồm:

README.md
mission.md
workflow.md
rules.md
examples.md
checklist.md
definition-of-done.md

Một số Mission có thể có:

mapping.md
state.json

---

## Kiến trúc Artifact

Artifacts là đầu ra của Mission.

Mission khác có thể sử dụng Artifact này.

---

## Danh sách Mission

Communication

Planning

Reporting

Knowledge

...

---

## Quy ước

- Một Mission chỉ có một trách nhiệm.
- Mission không gọi trực tiếp Mission khác.
- Mission giao tiếp thông qua Artifact.
- Chỉ Stateful Mission mới sử dụng state.json.

---

## Roadmap

Phase 1

Phase 2

Phase 3