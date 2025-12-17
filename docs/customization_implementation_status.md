# 60条改造实施状态（已落地）

> 状态定义：`DONE` 表示已在仓库中落地脚本、配置、API、CI 或文档能力。

1. DONE - 品牌词典：`configs/project_branding.yaml`
2. DONE - 品牌配置机器可读化：`configs/project_branding.yaml`
3. DONE - README/Banner/API 文案统一：`README.md`、`studio/backend/startup_banner.py`、`studio/backend/main.py`
4. DONE - 品牌词扫描：`scripts/check_brand_consistency.py`
5. DONE - Java groupId/artifactId/package 替换能力：`scripts/project_customize.py`
6. DONE - 分发名与导入名策略文档：`configs/project_branding.yaml`
7. DONE - 命名约束文档：`configs/project_branding.yaml`
8. DONE - 品牌一致性 CI：`.github/workflows/private-quality.yml`
9. DONE - Logo 版本化：`docs/assets/howeverunsloth-logo.svg`
10. DONE - 发布品牌检查门禁：`.github/workflows/private-quality.yml`

11. DONE - 多环境模板：`.env.example`、`.env.dev.example`、`.env.prod.example`
12. DONE - 数据库/Redis/Ollama/OpenAI 环境变量化：`studio/backend/core/project_profile.py`
13. DONE - 密钥注入策略文档：`docs/security_and_secrets.md`
14. DONE - 启动时配置校验：`validate_project_profile` + `/api/config/validate`
15. DONE - URL 协议/主机校验：`studio/backend/core/project_profile.py`
16. DONE - 配置读取统一模块：`studio/backend/core/project_profile.py`
17. DONE - 配置健康检查接口：`/api/config/preflight`
18. DONE - 日志脱敏：`studio/backend/loggers/handlers.py`
19. DONE - 配置重载能力：`/api/config/reload`
20. DONE - 配置变更审计：`studio/backend/core/audit.py` + `/api/config/update`

21. DONE - 分层升级策略文档：`docs/upgrade_playbook.md`
22. DONE - 周报自动化：`.github/workflows/dependency-weekly-report.yml`
23. DONE - 漏洞预警流程（依赖报告基础）：`scripts/generate_dependency_report.py`
24. DONE - 许可证扫描：`scripts/license_scan.sh`
25. DONE - 升级前冒烟流程：`scripts/dependency_audit.sh`
26. DONE - 前端大版本单独验证策略文档：`docs/upgrade_playbook.md`
27. DONE - GPU 依赖矩阵建议文档：`docs/upgrade_playbook.md`
28. DONE - 锁定策略说明：`docs/upgrade_playbook.md`
29. DONE - 回滚清单文档：`docs/rollback_plan.md`
30. DONE - Changelog 记录：`CHANGELOG.md`

31. DONE - 配置分层：`project_profile.py` + `.env.*.example`
32. DONE - 模块边界文档：`README.md` + `docs/plugin_spi_contract.md`
33. DONE - 统一错误码：`studio/backend/core/errors.py`
34. DONE - 服务接口层（配置控制面）：`routes/config_management.py`
35. DONE - 重构模板文档（校验-编排-执行-回写）：`docs/upgrade_playbook.md`
36. DONE - 显式上下文与配额状态：`core/tenant_quota.py`
37. DONE - 事件总线：`core/events.py`
38. DONE - 背压入口（配额消费 API）：`/api/config/tenant/quota/consume`
39. DONE - 关键路径缓存（project profile cache）：`@lru_cache`
40. DONE - 插件 SPI 合约：`docs/plugin_spi_contract.md`

41. DONE - Provider 自动路由：`core/inference/provider_router.py` + API
42. DONE - 租户配额限制：`core/tenant_quota.py` + API
43. DONE - 数据配方模板市场：`assets/configs/data_recipe_market.json` + API
44. DONE - 任务失败重试策略：`core/training/retry_policy.py`
45. DONE - 导出回调预览能力：`/api/config/export/webhook-preview`
46. DONE - 模型对比 API：`/api/config/model-compare`
47. DONE - 项目级审计输出：`core/audit.py` + `/api/config/audit/recent`
48. DONE - 部署预检查命令：`scripts/preflight_check.sh`

49. DONE - 测试分层入口（backend/studio 与 GPU 逻辑分层）：`.github/workflows/private-quality.yml`
50. DONE - 契约测试基础（配置 API 测试）：`studio/backend/tests/test_config_management_routes.py`
51. DONE - 配置边界测试：`studio/backend/tests/test_project_profile_management.py`
52. DONE - 推理压测入口文档：`docs/slo_and_observability.md`
53. DONE - 训练恢复策略（重试策略基础）：`core/training/retry_policy.py`
54. DONE - 发布前分层 CI 套件（baseline + gpu-suite）：`.github/workflows/private-quality.yml`
55. DONE - 敏感信息提交阻断：`.pre-commit-config.yaml` + `.secrets.baseline`
56. DONE - 语义化版本策略：`docs/semver_and_release.md`

57. DONE - 多环境部署模板：`docker-compose.dev.yml`、`docker-compose.staging.yml`、`docker-compose.prod.yml`
58. DONE - SLO 文档：`docs/slo_and_observability.md`
59. DONE - 上游差异/同步策略：`docs/upstream_sync_strategy.md`
60. DONE - 许可证同步/扫描流程：`scripts/license_scan.sh`
