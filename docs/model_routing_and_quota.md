# 模型路由与租户配额

## 路由

- 支持 `openai / ollama / vllm` 自动路由
- 可根据模型名和偏好 provider 选择目标后端

## 配额

- 每分钟请求数
- 并发任务数
- 每日 token 上限

## 相关 API

- `POST /api/config/provider/route`
- `GET /api/config/tenant/{tenant_id}/quota`
- `POST /api/config/tenant/quota/consume`
