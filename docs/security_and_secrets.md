# 安全与密钥治理

## 目标

- 密钥不入库
- 配置可审计
- 日志自动脱敏

## 规则

1. 生产环境密钥只通过环境变量或 Secret Manager 注入。
2. 任何 `HF_TOKEN`、`OPENAI_API_KEY`、`WANDB_API_KEY` 禁止提交。
3. 启用 `detect-secrets` pre-commit 检查。
4. 日志处理器自动掩码敏感字段。

## 操作

```bash
pre-commit run --all-files
```
