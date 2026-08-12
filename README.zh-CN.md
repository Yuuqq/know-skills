<p align="center">
  <img src="./docs/assets/know-skills-banner.svg" alt="Know Skills banner" width="100%">
</p>

<h1 align="center">css-professor</h1>

<p align="center">
  <strong>一个像计算社会科学教授那样回答问题的 Agent Skill ——
  先路由问题、再按深度收口、并且拒绝把平台指标当成真值。</strong>
</p>

<p align="center">
  <a href="https://github.com/Yuuqq/know-skills/actions/workflows/skill-contract.yml"><img src="https://github.com/Yuuqq/know-skills/actions/workflows/skill-contract.yml/badge.svg" alt="CI"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license"></a>
  <a href="https://github.com/Yuuqq/know-skills/releases"><img src="https://img.shields.io/github/v/release/Yuuqq/know-skills?color=blue" alt="Latest release"></a>
  <img src="https://img.shields.io/badge/language-EN%20%2F%20%E4%B8%AD%E6%96%87-orange" alt="中英双语">
</p>

<p align="center">
  <a href="./README.md">English</a> ·
  <a href="#安装">安装</a> ·
  <a href="#它做什么">它做什么</a> ·
  <a href="#beforeafter-对比">Before/After</a> ·
  <a href="#有测试不是玄学">有测试</a> ·
  <a href="#开发与维护">开发与维护</a>
</p>

---

直接问大模型一个社科问题，它默认会犯三类错：百科式堆砌、把简单问题升级成综述、
把平台痕迹自信地读成因果。`css-professor` 是一个
[SKILL.md 格式](https://agentskills.io)的 Agent Skill，在模型前面装上三道纪律：

1. **路由** —— 先选姿态：课堂科普老师 / 研究型导师 / 方法论审稿人。
2. **深度门控** —— 一句话的问题给一句话的答案；只有设计和审稿任务才解锁完整脚手架。
3. **真值来源纪律** —— 每个实证断言必须点名真值来源；转发量、话题标签、主题分数、
   LLM 打分在验证之前都只是测量产物（measurement artifacts）。

为计算社会科学、传播学、平台研究、AI-in-society 方向的学生、研究者和写作者而做，
中英双语，内置中文学术语域（论文、基金、开题、审稿）。

## 适合谁

| 你是 | 它替你拦住的毛病 |
| --- | --- |
| 学生 / 自学者 | 解释停在百科铺陈，没有一句话判断和直觉例子 |
| 正在选题 / 开题 / 写基金的人 | 把泛泛题目当研究问题，构念没拆，机制没分 |
| 做实证 / 审稿的人 | 因果过度自信，把转发量、话题标签、LLM 分数当成真值 |

## 安装

任何支持 Agent Skills 格式的宿主都可用（Claude Code、Cursor、Codex、Copilot 等）。

```bash
npx skills add Yuuqq/know-skills
```

或手动安装：

```bash
git clone https://github.com/Yuuqq/know-skills.git
cp -r know-skills/skills/css-professor ~/.claude/skills/   # 或 ~/.agents/skills、.cursor/skills
```

Windows PowerShell（仓库自带同步脚本，默认装到 `%USERPROFILE%\.agents\skills`）：

```powershell
git clone https://github.com/Yuuqq/know-skills.git; Set-Location know-skills
.\scripts\sync-skills.ps1        # -DryRun 预览；-Symlink 用符号链接代替拷贝
```

装好后直接调用（按宿主用 `$css-professor` 或 `/css-professor`），或者直接问
社科问题——解释 / 研究设计 / 方法审稿类的问题会自动触发。

## 它做什么

每个问题独立选择 **Mode**（姿态）和 **Depth**（输出天花板）：

| Mode | 触发信号 | 输出重点 |
| --- | --- | --- |
| 课堂科普老师 | 解释 / 什么是 / 例子 / explain | 先给判断，再给直觉例子、概念、一个常见误区 |
| 研究型导师 | 选题 / 开题 / 基金 / proposal | 研究问题、理论机制、构念、数据、方法、下一步研究 |
| 方法论审稿人 | 审稿 / 有什么问题 / 因果 / critique | 最致命缺陷先行，然后是识别策略、测量问题、修复路径 |

| Depth | 触发信号 | 天花板 |
| --- | --- | --- |
| Flash | 一句话 / briefly | 直接回答 + 至多一句限定 |
| Class | 帮我理解 / teach | 判断 → 例子 → 概念 → 误区 → 复盘 |
| Studio | 设计研究 / 框架 | 按需使用研究设计模板的部分章节 |
| Review | 审稿 / validity | 缺陷先行的审稿意见，不写客套开场 |

**Hard Load Table** 控制上下文：方法分支、质量清单、中文学术风格、校准示例
只在任务需要时加载，绝不整包预载。

审稿人模式内置八个方法分支——文本/语料、质性编码、网络、因果推断、调查/实验、
模拟、平台痕迹、混合方法——每个分支都钉死"真值来源 vs 测量产物"的区分。

## Before/After 对比

同一个提问，装与不装的差别。三组完整对比（课堂解释 / 研究设计 / 方法审稿）见
[docs/before-after-demos.md](./docs/before-after-demos.md)。最短版本：

> **提问**："我用微博转发网络证明谣言扩散导致社会信任下降，这个设计有什么问题？"
>
> **裸模型**：夸"设计整体合理"，建议补充控制变量、多跑几个回归，因果结论原样保留。
>
> **装上 css-professor**：第一句就指出致命伤（仅凭转发网络无法识别社会信任的变化），
> 区分扩散数据测到的东西和信任测量需要的东西，降级因果结论，给出最小修复路径
> （面板调查、事件研究或自然实验）。

它改变的不是模型"知道多少"，而是**回答的纪律**：判断先行、深度收口、点名真值来源。

## 有测试，不是玄学

大部分 skill 是一段没有版本的 prompt。这个仓库按软件的标准发布：

- **48 个离线契约测试**钉住路由表、深度天花板、反触发条件和资源路径——
  纯标准库、不调模型，每次 push 在 Ubuntu 和 Windows 上都跑。
- **12 条黄金提示词**定义每个 fixture 的预期 Mode + Depth。
- **真模型评测脚本**（`scripts/eval_css_professor.py`）把黄金提示词发给任意
  OpenAI 兼容端点并给路由准确率打分；没有 API key 时安全跳过，CI 不依赖任何密钥。

```powershell
python .\skills\css-professor\scripts\validate.py
python -m unittest skills.css-professor.tests.test_skill_contract skills.css-professor.tests.test_eval_fixtures
```

## 仓库结构

```text
know-skills
├─ skills/
│  ├─ css-professor/     # 产品本体：SKILL.md + references + assets + tests
│  └─ agent-loop/        # 已弃用的兼容别名，转发到 css-professor
├─ scripts/
│  ├─ sync-skills.ps1    # 本机安装/更新（Windows）
│  ├─ sync-skills.sh     # 本机安装/更新（macOS/Linux）
│  └─ eval_css_professor.py  # 可选的真模型评测脚本
└─ docs/before-after-demos.md
```

把书和课程转成 skill 的两个配套工具——曾经 vendored 在本仓库、现改为链接引用：
[book-to-skill](https://github.com/virgiliojr94/book-to-skill)（MIT）、
[lineage-skill](https://github.com/JuneYaooo/lineage-skill)（PolyForm
Noncommercial，禁商用）。详见 [NOTICES.md](./NOTICES.md)。

## 开发与维护

修改技能后的检查顺序：

```powershell
# 结构：frontmatter + 资源路径
python .\skills\css-professor\scripts\validate.py

# 行为：契约 + 黄金题（48 个测试）
python -m unittest skills.css-professor.tests.test_skill_contract skills.css-professor.tests.test_eval_fixtures

# 评测脚本自身的离线冒烟测试
python -m unittest discover -s scripts -p "test_*.py"

# 同步到本机技能目录
.\scripts\sync-skills.ps1
```

欢迎贡献——见 [CONTRIBUTING.md](./CONTRIBUTING.md)。适合上手的方向：
新增黄金提示词、新增方法分支、补英文 fixture。

## 许可

仓库内全部内容为 MIT 协议——见 [LICENSE](./LICENSE)；上游来源与历史说明见
[NOTICES.md](./NOTICES.md)。
