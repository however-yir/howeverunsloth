# 版本与发布策略

## 语义化版本

- MAJOR：不兼容 API/配置变更
- MINOR：向后兼容功能新增
- PATCH：向后兼容修复

## 发布流程

1. 更新 CHANGELOG
2. 执行测试矩阵
3. 创建 tag：`scripts/create_release_tag.sh <version>`
4. 发布 release note
