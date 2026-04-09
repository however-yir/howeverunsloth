# 与上游同步策略

## 分支建议

- `main`：私有化稳定分支
- `upstream-sync/*`：上游同步分支
- `feature/*`：改造功能分支

## 同步流程

1. 拉取上游
2. 在 `upstream-sync/*` 解决冲突
3. 执行回归测试
4. 合并到 `main`
