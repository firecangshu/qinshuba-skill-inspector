# 平台规范参考表（Platform Specs）

> 秦叔宝 v2.0 新增「模块 P：平台兼容性」的参考资料。
> 用于在 Phase 0.5 确认目标平台后，逐项核对 PC01-PC06。
> 本表以**已验证事实**为准：SkillHub 接受任意合法 semver（johari-prompt-coach 以 `1.3.2` 成功上架），且上架表单未强制 `category` / `platforms`。凡未经验证的"传闻"均标注 ⚠️ 待复核。

---

## A. SkillHub（国内 · 默认目标平台）

**定位**：腾讯云 SkillHub 上架前质检的目标平台。
**审核机制**：三线并行 —— ① 内容合规 ② 科恩实验室漏洞扫描 ③ 云鼎实验室 AI 安全评估。

### 文件建议清单（允许打包，非强制）

> 实际采用**黑名单拦截制**（见 PC01）：命中 §4.2.1 D04 黑名单即 FAIL；白名单仅为建议，多带非黑名单文件（如 `CHANGELOG.md`）不强制否决。

| 文件 / 目录 | 必需 | 说明 |
|------------|------|------|
| `SKILL.md` | ⭐ 必需 | skill 核心定义，缺失直接拒收 |
| `README.md` | 推荐 | 说明文档，提升可发现性 |
| `references/` | 可选 | 参考文档目录 |
| `scripts/` | 可选 | 辅助脚本目录 |

### 文件黑名单（平台不允许，必须剔除 —— 命中即 P0）

与 §4.2.1 一致：`.git/`、`.gitignore`、`LICENSE`、`.DS_Store`、`node_modules/`、`Thumbs.db` / `desktop.ini`、`*.tmp` / `*.log` / `*.bak`、`__pycache__/` / `*.pyc`。

> 💡 额外零散 `.md`（如 `CHANGELOG.md`、`CONTRIBUTING.md`、规划文档）**非黑名单**，可保留；但建议保持包最小化（仅 `SKILL.md` + `README.md` + 必要 `references/` / `scripts/`）以降低被额外规则误伤的概率。

### 元数据必填字段

| 字段 | 要求 | 秦叔宝处理 |
|------|------|-----------|
| `name` | 必需（kebab-case）| PC02 硬检查 |
| `version` | 必需（semver `X.Y.Z`）| PC02 + PC03 硬检查 |
| `description` | 必需（含触发词与场景）| PC02 硬检查 |
| `category` | ⚠️ 推荐（非硬性拒收）| PC02 建议项 |
| `platforms` | ⚠️ 推荐（非硬性拒收）| PC02 建议项 |

### 版本号格式

- ✅ 任意合法 semver：`1.0.0` / `1.3.2` / `2.0.0` 均可
- ❌ 非三段：`1.0` / `1.0.0.0`
- ❌ 含前缀：`v1.0.0`
- ⚠️ 不强制 `1.0.0` 占位符（旧传闻已被 johari 实战推翻）

### 大小限制

- 推荐 < 1 MB（硬上限以平台实时公示为准）
- 超过时 PC05 标记 P2 警告

### zip 根目录结构

- ✅ 解压后根目录 = skill 名（如 `qinshubao/`）
- ❌ 嵌套目录 / 文件散落根目录（PC04 标记 P1）

---

## B. GitHub

**文件**：自由，无白/黑名单限制。
**必填字段**：无。
**版本号**：任意。
**启用检查**：仅 PC01（最宽松，白名单 = 全部）。

---

## C. Claude Code / Cursor

**官方协议**：Anthropic Agent Skills（`SKILL.md` 必需）。
**必填字段**：`name` + `description`；`version` 可选。
**允许文件**：`SKILL.md`（可附加 `references/` / `scripts/` / `assets/`）。
**启用检查**：PC01（仅 `SKILL.md` 必需）+ PC02 子集（name/description）。

---

## E. WorkBuddy（含连接器 / 技能市场）

> 实证来源：用户上传 skill zip 时，WorkBuddy 明确报错「SKILL.md 必须位于 ZIP 包的根目录下，不能放在子目录中」。此为该平台硬性要件，与 SkillHub（根目录 = skill 名文件夹）正好相反。

**zip 根目录结构（关键差异）**：
- ✅ zip 根目录下**直接**包含 `SKILL.md`（顶层，不在任何子目录中）
- ❌ `SKILL.md` 被嵌套在文件夹中（如 `qinshubao/SKILL.md`）—— PC04 标记 P1
- 其他文件 / 子目录（如 `references/`、`scripts/`）通常允许，但 `SKILL.md` 必须在根

**文件白名单 / 必填 / 版本号**：参考 SkillHub 同类规则（PC01-PC03 同套）。
**启用检查**：PC01-PC06 全套（其中 PC04 按「SKILL.md 在根」判定）。

---

## F. Lenovo 开放平台（open.lenovomm.com）

> 实证来源：用户在 `open.lenovomm.com/developer/skillcreate` 上传 skill zip 时，平台明确报错「SKILL.md 必须位于 ZIP 包的根目录下，不能放在子目录中」。此为该平台硬性要件，与 SkillHub（根目录 = skill 名文件夹）正好相反，与 WorkBuddy 一致。

**zip 根目录结构（关键差异）**：
- ✅ zip 根目录下**直接**包含 `SKILL.md`（顶层，不在任何子目录中）
- ❌ `SKILL.md` 被嵌套在文件夹中（如 `qinshubao/SKILL.md`）—— PC04 标记 P1
- 其他文件 / 子目录（如 `references/`、`scripts/`）通常允许，但 `SKILL.md` 必须在根

**文件白名单 / 必填 / 版本号**：参考 SkillHub 同类规则（PC01-PC03 同套）。
**启用检查**：PC01-PC06 全套（其中 PC04 按「SKILL.md 在根」判定）。

---

## D. 其他平台

用户提供平台规范后，秦叔宝按用户提供的白名单 / 必填字段 / 版本规则执行 PC01-PC06，不在本表范围内。

---

## 发布预检清单模板（PC06）

### 发布到 SkillHub 前

- [ ] 文件全部在 SkillHub 白名单内，无黑名单文件
- [ ] 元数据必填齐全：`name` / `version` / `description`
- [ ] `category` / `platforms` 已填写（推荐项，建议补全）
- [ ] 版本号格式为合法 `X.Y.Z`
- [ ] zip 解压后根目录 = skill 名
- [ ] 包大小 < 1 MB
- [ ] 触发词明确，不与同类 skill 冲突
- [ ] 通过安全 8 维（S01-S08）

### 发布到 GitHub 前

- [ ] 文件自由，无敏感信息泄露
- [ ] 通过安全 8 维

### 发布到 Claude Code / Cursor 前

- [ ] 含 `SKILL.md`
- [ ] `name` / `description` 齐全
- [ ] 通过安全 8 维
