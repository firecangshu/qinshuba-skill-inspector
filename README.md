# 🛡️ 秦叔宝 · Skill 质检员

> 隋唐门神化身 SkillHub 上架前质检员。丢给我一个 skill，79 项检查 + 5 大维度评分，30 秒告诉你能不能上架、哪里要改。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.3.0-blue.svg)](https://github.com/qinshuba-skill-inspector/releases)
[![SkillHub](https://img.shields.io/badge/SkillHub-pending-orange.svg)](https://skillhub.cloud.tencent.com)

---

## 📖 这是什么

**秦叔宝（qinshubao）** 是一个 SkillHub 平台的上架前质检 skill。它模拟 SkillHub 官方审核员视角，对一个待上架的 skill 进行**全维度质量体检**，输出带分值、带问题清单、带优化建议的结构化报告。

**为什么叫"秦叔宝"？** 取自《说唐》《隋唐演义》门神——尉迟恭与秦叔宝，寓意**守门把关、忠义执锐**，象征质检员严守 SkillHub 上架门槛。谐音"勤守宝"：勤恳守护 quality 之宝。

---

## ✨ 核心能力

- 🛡️ **秦叔宝守门**：79 项规则 + 5 维度评分，发现问题不放过
- 📊 **TRACE 五维评分**：可信任度 25% / 可靠性 20% / 适用性 20% / 规范性 15% / 有效性 20%
- 🔍 **79 项检查规则**：封装合规 22 + 安全检测 8 + Deep 扩展 6 + 五维 37 + 平台 P 6
- 🌐 **平台兼容性 P 维度（v2.0）**：Phase 0.5 确认目标平台后，按 SkillHub / WorkBuddy / Lenovo / GitHub / Claude Code 规范做 PC01-PC06 检查，最终分 × 平台系数，评分与实际发布成功率挂钩
- 🚨 **P0 一票否决**：安全红线直接判 0 分，帮你避开常见驳回
- ⏱️ **三档评测深度**：Quick 1 分钟 / Standard 3 分钟 / Deep 5 分钟
- 📝 **上架表单填写建议**：质检通过自动生成 6 字段吸睛版建议
- 🎨 **描述吸睛度评分**：钩子力 / 数字力 / 能力力 / 触发力 / 场景力 5 维度

---

## 🚀 快速开始

### 1. 安装到本地

```bash
# 解压安装包到 skills 目录
unzip qinshubao-2.3.0.zip -d ~/.workbuddy/skills/qinshubao/
```

### 2. 触发质检

**双要素模型**：触发词 + 目标定位

| 触发词 | 场景 |
|--------|------|
| `秦叔宝` | 中文专属称呼 |
| `秦叔宝帮我看看这个skill` | 自然口语化 |
| `skill质检` | 中文泛指 |
| `检查skill` | 中文动宾 |
| `上架前检查` | 上架场景 |
| `qinshubao` | 英文标识 |
| `TRACE评测` | 模型术语 |
| `评估skill质量` | 评估类 |
| `这个skill能上架吗` | 二元判定 |
| `发布前自检` | 自查场景 |
| `skill质量评测` | 质量维度 |
| `帮我填表` | 上架表单建议 |
| `上架建议` | 上架策略 |

**3 种目标定位方式**：
1. **目录路径**（推荐）：`~/.workbuddy/skills/golden-idea/`
2. **完整内容**：直接粘贴 SKILL.md 全文
3. **zip 包**：`~/Desktop/xxx.zip`

### 3. 实战示例

```
👤: 秦叔宝，帮我看看这个 skill
   路径：~/.workbuddy/skills/golden-idea/
   深度：Deep

🤖 秦叔宝: 收到，开始全维度体检...

   [2 分钟后输出]
   - 总体评分：4.50/5 · S 级优秀
   - 0 P0 / 1 P1 / 4 P2
   - 五维分项 + 安全检测
   - 优化建议 + 上架表单填写建议
```

---

## 📊 评分体系

### 综合评分公式

```
综合 = T × 0.25 + R × 0.20 + A × 0.20 + C × 0.15 + E × 0.20
```

### 等级表

| 综合分 | 等级 | 中文标签 | 建议 |
|--------|------|----------|------|
| 4.5 - 5.0 | S | 优秀 | 可直接发布 |
| 4.0 - 4.4 | A | 良好 | 可发布，建议优化 |
| 3.5 - 3.9 | B | 一般 | 修复后发布 |
| 3.0 - 3.4 | C | 较差 | 重大改进后发布 |
| < 3.0 | D | 不合格 | 必须修复 P0 问题 |

### 扣分规则

| 严重度 | 扣分 |
|--------|------|
| P0 | 每个 -0.5 分 |
| P1 | 每个 -0.2 分 |
| P2 | 每个 -0.1 分 |
| **安全 P0** | **一票否决（综合分 = 0）** |

---

## 🛡️ 安全检测 8 维

| 编号 | 项目 | 严重度 |
|------|------|--------|
| S01 | 提示词注入 | P0 |
| S02 | 敏感信息泄露 | P0 |
| S03 | 危险操作 | P0 |
| S04 | 权限最小化 | P1 |
| S05 | 外部调用安全 | P0 |
| S06 | 反爬规避 | P0 |
| S07 | 内容合规 | P0 |
| S08 | 行为可审计 | P1 |

**任一 P0 安全项不通过 → 综合分直接归 0，发布准备度强制"未通过"。**

---

## 📂 项目结构

```
qinshubao/
├── SKILL.md               # 秦叔宝核心 skill（986 行）
├── README.md              # 本文件
├── CHANGELOG.md           # 变更记录
├── CONTRIBUTING.md        # 贡献指南
├── LICENSE                # MIT 协议
├── .gitignore             # Git 忽略规则（打包时剔除）
├── references/
│   └── platforms.md       # 各平台规范参考表（SkillHub/WorkBuddy/Lenovo/GitHub/Claude Code）
└── scripts/
    ├── platform_check.py  # 平台兼容性检查脚本（PC01-PC06，纯标准库）
    ├── self_audit.py      # 模块 0 自动化自检脚本（F/D/P 共 22 项，纯标准库）
    └── package.py         # 多平台打包脚本（生成 SkillHub 嵌套 / WorkBuddy-Lenovo 根目录 zip）
```

> 注：`.git/`、`.gitignore`、`LICENSE` 等文件在上传 SkillHub 时按 §4.2.1 D04 黑名单剔除，不进入发布包。

---

## 🛠️ 开发与扩展

### 添加新的检查项

在 SKILL.md 对应模块的检查项表中追加新行：

```markdown
| 编号 | 检查项 | 判定标准 | 严重度 | 评分 |
|------|--------|----------|--------|------|
| F17 | xxx | xxx | P1 | -0.2 |
```

### 自定义触发词

在 frontmatter 的 `trigger` 数组中添加：

```yaml
trigger:
  - "秦叔宝"
  - "你的自定义触发词"
```

### 自定义评分权重

在 §12.1 综合分公式处修改权重：

```markdown
综合 = T × 0.30 + R × 0.20 + A × 0.20 + C × 0.10 + E × 0.20
```

---

## 🤝 贡献

欢迎贡献代码、报告 Bug、提出改进建议！

- **Bug 报告**：使用 [GitHub Issues](https://github.com/your-username/qinshuba-skill-inspector/issues)
- **功能建议**：使用 [GitHub Discussions](https://github.com/your-username/qinshuba-skill-inspector/discussions)
- **代码贡献**：详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📜 协议

本项目采用 [MIT 协议](LICENSE)。

---

## 🌟 致谢

- SkillHub 平台提供的 skill 生态
- 隋唐门神秦叔宝的守门把关精神
- 所有 contributor 和 user 的反馈

---

## 📮 联系方式

- GitHub Issues: 提交问题
- SkillHub: 搜索"秦叔宝"或"qinshubao"

---

> 🛡️ 秦叔宝 · 守门把关 · 忠义执锐
>
> "宁可错杀一千，不放过一个 P0。"
