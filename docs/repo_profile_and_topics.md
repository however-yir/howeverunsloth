# 仓库描述与 Topics 建议

## 推荐仓库描述

私有化模型训练、推理与数据配方平台（基于 Unsloth 二次工程化）

## 推荐 GitHub Topics

- howeverunsloth
- llm
- finetuning
- inference
- local-llm
- ollama
- rag
- tool-calling
- model-serving
- ai-platform

## 一键更新命令

```bash
gh repo edit <OWNER>/<REPO> \
  --description "私有化模型训练、推理与数据配方平台（基于 Unsloth 二次工程化）"

for topic in howeverunsloth llm finetuning inference local-llm ollama rag tool-calling model-serving ai-platform; do
  gh repo edit <OWNER>/<REPO> --add-topic "$topic"
done
```

## Logo 建议

- 默认 Logo：`docs/assets/howeverunsloth-logo.svg`
- 可在 README 顶部使用：

```markdown
![howeverunsloth logo](docs/assets/howeverunsloth-logo.svg)
```
