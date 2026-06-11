# Word Format Skill

一个用于中文 Word 文档排版的 Codex Skill。适用于课程论文、实验报告、作业文档、已有 `.docx` 文档整理，以及需要按中文学术规范生成可提交 Word 文件的场景。

## 功能

- 生成或整理 `.docx` 文件，而不是只给排版建议
- 设置 A4 页面、2.5 cm 等宽页边距、正文和标题字体字号
- 统一中文层级标题编号、段落缩进、两端对齐和 1.5 倍行距
- 规范表格、图片、图题、表题、公式和页码
- 对重点内容使用克制的浅蓝色标注
- 针对实验报告提供常见结构和检查清单
- 可按用户要求额外导出 PDF

## 目录结构

```text
word-format-skill/
├── README.md
├── evaluate_skill.py          # Skill 评估工具
└── word-format/
    ├── SKILL.md               # 核心说明
    ├── agents/
    │   └── openai.yaml        # Codex UI 元数据
    └── references/
        └── word-format-spec.md # 完整排版规范
```

**文件说明：**

| 文件 | 用途 |
|------|------|
| `word-format/SKILL.md` | Codex 触发和执行该技能时读取的核心说明 |
| `word-format/references/word-format-spec.md` | 完整 Word 排版规范 |
| `word-format/agents/openai.yaml` | Codex UI 中展示用的元数据 |
| `evaluate_skill.py` | 基于 writing-skills 框架的评估工具 |

## 安装

将整个 `word-format` 文件夹复制到 Codex skills 目录：

```bash
cp -R word-format ~/.codex/skills/word-format
```

安装后，Codex 可以在相关 Word 排版任务中自动触发，也可以通过显式调用使用：

```text
Use $word-format to format this document into a polished .docx file.
```

## 使用示例

```text
使用 $word-format，把这份实验报告排版成可以提交的 Word 文档。
```

```text
使用 $word-format，按照中文课程论文格式整理这个 Markdown，并生成 .docx。
```

```text
使用 $word-format，帮我把这个已有 Word 文档统一字体、标题、表格和页边距。
```

## 默认排版规范

| 类别 | 规范 |
|------|------|
| 页面 | A4，纵向，四边页边距 2.5 cm |
| 正文中文 | 宋体，五号 |
| 正文英文/数字/变量/单位 | Times New Roman |
| 一级标题 | 宋体，小三，加粗 |
| 二级标题 | 黑体，小四，不加粗 |
| 正文段落 | 首行缩进 2 个中文字符，两端对齐，1.5 倍行距 |
| 表格 | Word 原生表格，居中，不超出页边距 |
| 图片 | 居中、清晰、保持比例 |
| 公式 | 可编辑 Word 公式，不能截图化 |
| 重点标注 | 浅蓝色，且不超过全文 20% |

> **注意：** 如用户提供学校、课程或教师模板，应优先遵守用户模板。

## 评估工具

项目包含一个基于 [writing-skills](https://github.com/anthropics/claude-code/tree/main/skills/writing-skills) 框架的评估工具：

```bash
python evaluate_skill.py
```

**评估维度（满分 130 分）：**

| 维度 | 分值 | 说明 |
|------|------|------|
| YAML Frontmatter | 20 | name/description 格式 |
| Structure | 25 | 必需章节完整性 |
| CSO Optimization | 25 | 触发关键词、双语支持 |
| Content Quality | 20 | 示例、代码块、表格 |
| Testing/TDD | 20 | 测试方法论 |
| Anti-Patterns | 10 | 反模式规避 |
| Token Efficiency | 10 | 行数/词数效率 |

**当前评分：107/130 (82.3%)**

## 相关资源

- [agentskills.io/specification](https://agentskills.io/specification) - Skill 规范
- [writing-skills](https://github.com/anthropics/claude-code/tree/main/skills/writing-skills) - 评估框架

## 许可证

MIT License
