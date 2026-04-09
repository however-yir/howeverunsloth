# 依赖升级作战手册

## 批次策略

1. 工具链（lint/test/build）
2. 前端依赖
3. 后端依赖
4. GPU 栈依赖（单独验证）

## 每次升级都必须做

- 运行 `scripts/dependency_audit.sh`
- 运行后端 smoke tests
- 记录回滚 tag

## 回滚

```bash
git checkout <rollback-tag>
```
