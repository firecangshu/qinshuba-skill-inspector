# 贡献指南

欢迎为秦叔宝（qinshubao）贡献代码！🛡️

## 提交流程

1. **Fork 本仓库**
2. **创建 feature 分支**：`git checkout -b feature/your-feature`
3. **提交变更**：`git commit -m "feat: 你的功能"`
4. **推送到 fork**：`git push origin feature/your-feature`
5. **创建 Pull Request**

## 提交信息规范

本项目遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat: 新增功能
fix: 修复 bug
docs: 仅文档变更
style: 代码格式变更（不影响功能）
refactor: 重构（非新增功能、非修复 bug）
test: 增加/修改测试
chore: 构建/工具变更
```

**示例**：
- `feat: 新增模块 6 上架合规性检查`
- `fix: F10 中文字符数判定错误`
- `docs: 补充 README 触发词说明`

## 代码规范

### Markdown 规范

- 一级标题：每个文件最多 1 个（H1）
- 标题层级：不跳级（H1 → H2 → H3）
- 代码块：必须带语言标签（```markdown）
- 表格：列数 ≤ 6，超过时拆表
- 中英混排：避免整段堆叠

### SKILL.md 修改规范

1. **新增检查项**：在对应模块的检查项表中追加新行
   - 编号必须唯一（F01-F99 / T01-T99 / R01-R99 / A01-A99 / C01-C99 / E01-E99 / S01-S99 / Q01-Q99）
   - 判定标准必须"可执行可判定"，不能有"可能/或许"等模糊词
   - 严重度必须明确（P0/P1/P2）

2. **修改触发词**：同步更新 frontmatter `trigger`、§2.2 表格、附录 Q05 触发词数

3. **修改评分公式**：在 §12.1 同步更新，并在 CHANGELOG.md 记录

## Pull Request 检查清单

提交 PR 前请确认：

- [ ] 代码遵循现有风格
- [ ] 自查通过（综合分 ≥ 4.5）
- [ ] 0 P0 问题
- [ ] CHANGELOG.md 已更新
- [ ] 文档（如 README）已同步更新
- [ ] 没有引入新的警告
- [ ] 描述清楚变更内容

## 报告 Bug

发现 Bug？请使用 [GitHub Issues](../../issues) 报告，包含：

1. **问题描述**：简明扼要
2. **复现步骤**：详细步骤
3. **期望行为**：应该发生什么
4. **实际行为**：实际发生了什么
5. **环境信息**：WorkBuddy 版本、操作系统等
6. **截图/日志**（如适用）

## 提出功能建议

使用 [GitHub Discussions](../../discussions) 提出，包含：

1. **使用场景**：解决什么问题
2. **建议方案**：怎么实现
3. **替代方案**：其他可选方案
4. **优先级**：紧急 / 重要 / 一般

## 行为准则

- 尊重他人
- 接受建设性批评
- 关注对社区最有利的事
- 体现同理心

---

感谢你的贡献！🛡️
