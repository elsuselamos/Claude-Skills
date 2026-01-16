# 贡献指南

感谢您对 dtg-java-skill 插件的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果您发现了 Bug 或有功能建议：

1. 检查 [Issues](https://github.com/shinpr/dtg-java-skill/issues) 确保问题未被报告
2. 创建新 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤（如果是 Bug）
   - 预期行为
   - 实际行为
   - 环境信息

### 提交代码

#### 准备工作

1. **Fork 仓库**
   ```bash
   # Fork 项目到您的 GitHub 账户
   ```

2. **克隆仓库**
   ```bash
   git clone https://github.com/your-username/dtg-java-skill.git
   cd dtg-java-skill
   ```

3. **添加上游仓库**
   ```bash
   git remote add upstream https://github.com/shinpr/dtg-java-skill.git
   ```

4. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### 开发规范

**代码风格**:
- 遵循项目现有的代码风格
- 使用 UTF-8 编码
- 添加适当的文档和注释

**提交规范**:
```bash
# 提交格式
git commit -m "type: subject"

# 类型
feat:     新功能
fix:      修复 Bug
docs:     文档更新
style:    代码格式调整
refactor: 重构
test:     测试相关
chore:    构建/工具相关

# 示例
git commit -m "feat: 添加 Redis 缓存支持"
git commit -m "fix: 修复代码审查报告生成问题"
git commit -m "docs: 更新 README 文档"
```

#### Pull Request 流程

1. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **创建 Pull Request**
   - 访问 GitHub 仓库页面
   - 点击 "New Pull Request"
   - 填写 PR 模板

3. **PR 模板**
   ```markdown
   ## 变更描述
   [简要描述您的变更]

   ## 变更类型
   - [ ] Bug 修复
   - [ ] 新功能
   - [ ] 代码重构
   - [ ] 文档更新
   - [ ] 性能优化

   ## 测试
   - [ ] 已添加单元测试
   - [ ] 已通过所有测试
   - [ ] 已手动测试

   ## 检查清单
   - [ ] 代码符合项目规范
   - [ ] 已更新相关文档
   - [ ] 无新的编译警告

   ## 相关 Issue
   Closes #(issue number)
   ```

4. **代码审查**
   - 维护者会审查您的代码
   - 根据反馈进行修改
   - 确保所有检查通过

5. **合并**
   - 审查通过后，您的 PR 会被合并
   - 您的贡献将出现在贡献者列表中

### 改进文档

文档也是项目的重要组成部分！

**文档改进方式**:
- 修正错别字和语法错误
- 补充缺失的文档
- 改进现有文档的表达
- 添加使用示例
- 翻译文档

**文档贡献流程**:
1. Fork 项目
2. 创建文档分支
3. 修改文档
4. 提交 PR

---

## 开发流程

### 环境搭建

#### 必需工具
- Python 3.8+
- Git
- Markdown 编辑器

#### 可选工具
- markdownlint (Markdown 校验)
- vale (文档风格检查)

### 项目结构

```
dtg-java-skill/
├── agents/              # AI 代理定义
├── skills/              # 技能定义
├── docs/                # 文档
│   ├── guides/         # 使用指南
│   ├── rules/          # 规范文档
│   └── templates/      # 模板文档
├── .claude-plugin/      # 插件配置
├── scripts/            # 脚本工具
└── README.md           # 项目说明
```

### 代码规范

#### Python 代码

**风格指南**: 遵循 PEP 8

**代码示例**:
```python
def format_report(report: dict) -> str:
    """格式化审查报告

    Args:
        report: 审查报告数据

    Returns:
        格式化后的报告字符串
    """
    # 实现代码
    pass
```

#### Markdown 文档

**规范**: 遵循项目文档规范

**要求**:
- 添加 UTF-8 编码声明
- 使用清晰的标题层级
- 代码示例使用正确的语言标识

### 测试要求

#### 单元测试

```python
# tests/test_formatter.py
import unittest

class TestReportFormatter(unittest.TestCase):
    def test_format_report(self):
        report = {"title": "Test"}
        result = format_report(report)
        self.assertIn("Test", result)
```

#### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_formatter.py

# 查看覆盖率
python -m pytest --cov=src tests/
```

---

## 审查标准

### 代码审查要点

#### 功能性
- [ ] 代码实现了预期功能
- [ ] 没有引入新的 Bug
- [ ] 边界情况得到处理

#### 代码质量
- [ ] 代码清晰易读
- [ ] 遵循项目规范
- [ ] 没有代码重复

#### 文档
- [ ] 更新了相关文档
- [ ] 添加了必要的注释
- [ ] 更新了 README（如需要）

#### 测试
- [ ] 添加了单元测试
- [ ] 测试覆盖率足够
- [ ] 所有测试通过

### 审查反馈

**反馈类型**:
- **必须修改**: 影响功能或质量问题
- **建议修改**: 改进代码质量
- **可选修改**: 个人偏好

**响应时间**: 维护者会在 3-7 天内给予反馈

---

## 社区规范

### 行为准则

**我们的承诺**:
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

**不允许的行为**:
- 使用性化语言或图像
- 恶意攻击或侮辱性评论
- 骚扰或恶意行为
- 未经许可发布他人隐私信息

### 沟通渠道

- **GitHub Issues**: 报告问题和功能请求
- **Pull Requests**: 代码贡献
- **Discussions**: 一般讨论

---

## 获取帮助

### 常见问题

**Q: 我该如何开始贡献？**
A: 从修复小 Bug 或改进文档开始

**Q: 我的 PR 多久会被审查？**
A: 通常 3-7 天内

**Q: 我不知道该贡献什么**
A: 查看 [Good First Issue](https://github.com/shinpr/dtg-java-skill/labels/good%20first%20issue) 标签

**Q: 可以贡献中文文档吗？**
A: 当然！我们非常欢迎中文文档贡献

### 联系方式

- **GitHub Issues**: https://github.com/shinpr/dtg-java-skill/issues
- **Email**: dubbo-microservice-support@example.com

---

## 许可证

通过贡献代码，您同意您的贡献将在与项目相同的 [MIT License](LICENSE) 下发布。

---

## 致谢

感谢所有贡献者！您的贡献让 dtg-java-skill 变得更好。

**贡献者列表**: https://github.com/shinpr/dtg-java-skill/graphs/contributors

---

**再次感谢您的贡献！**
