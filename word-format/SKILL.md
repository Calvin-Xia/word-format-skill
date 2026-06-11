---
name: word-format
description: Format or produce Chinese Word documents (.docx) according to academic/report layout rules, including A4 margins, Chinese/English fonts, heading levels, paragraph spacing, tables, figures, editable equations, highlights, page numbers, and final QA. Use when Codex is asked to do Word 排版, format a DOCX, polish a report/实验报告/course document, apply Chinese academic formatting, or generate a submission-ready .docx file, with optional PDF export.
---

# Word Format

## Overview

Use this skill to turn user-provided text, notes, Markdown, or existing documents into a polished, submission-ready `.docx` file that follows Chinese academic Word formatting conventions.

Always produce an actual Word document. Do not stop at formatting advice.

## Core Workflow

1. Read the source content or existing document and identify whether it is a general document, course paper, lab report, code-heavy document, or template-based assignment.
2. If the user provides a school, course, teacher, or department template, follow that template first and use this skill only for unspecified details.
3. Read `references/word-format-spec.md` before applying detailed formatting rules.
4. Preserve the original core content, paragraph logic, and writing tone. Do not add process text such as “根据用户要求”, “AI 生成”, “以下是整理后的内容”, or placeholder instructions.
5. Create or edit a `.docx` file with real Word structures: native tables, editable formulas when formulas are present, normal paragraphs and headings, inserted images, and proper page settings.
6. Render or otherwise inspect the finished document when possible, then fix visible layout problems before delivery.
7. Deliver the final `.docx` file. Export PDF as well only when the user requests it.

## Formatting Priorities

Apply these defaults unless the user or template says otherwise:

- A4 portrait pages with 2.5 cm margins on all sides and no gutter.
- Chinese body text in Songti/宋体, five-point size; English, digits, variables, and units in Times New Roman at the surrounding size.
- First-level headings in Songti/宋体, 小三, bold; second-level headings in Heiti/黑体, 小四, not bold; lower headings in Heiti/黑体, 五号, not bold.
- Body paragraphs with first-line indent of 2 Chinese characters, justified alignment, and 1.5 line spacing.
- Chinese hierarchical numbering by default: `一、`, `（一）`, `1.`, `（1）`. Preserve an existing complete numbering system if it is already consistent.
- Light blue highlight or text color only for genuinely important content, never more than 20% of the document, and never combined with bold.
- Tables as Word native tables, centered, within margins, with table titles above.
- Figures centered, proportional, clear, and paired with captions below.
- Equations as editable Word equations, not screenshots.

## Document-Type Handling

For lab reports, prefer this structure when the source content does not already provide a better complete structure:

```text
一、实验目的
二、实验仪器
三、实验原理
四、实验内容与步骤
五、数据记录与处理
六、误差分析
七、思考题
八、实验总结
```

Keep original questions, data, calculations, code, and important conclusions intact. Improve organization and formatting, but do not invent missing experimental results.

## Quality Gate

Before final delivery, check the document against `references/word-format-spec.md`, especially:

- Page size, margins, fonts, heading levels, paragraph indentation, and line spacing.
- Whether an extra full-document title was accidentally added.
- Whether tables, figures, formulas, captions, and page numbers are visible and correctly placed.
- Whether highlights are light blue, restrained, and not bold.
- Whether there are extra blank pages, excessive empty lines, broken captions, or AI/process wording.

## Reference

Read `references/word-format-spec.md` for the complete formatting standard copied from the source specification.
