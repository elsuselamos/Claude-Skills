# Translation Quality Guidelines

## Translation Principles

### 1. Technical Accuracy First
- Preserve all technical terms and concepts accurately
- Maintain precision in mathematical and algorithmic descriptions
- Ensure code examples remain functional
- Keep all programming language syntax intact

### 2. Natural Chinese Flow
- Use idiomatic Chinese expressions for technical concepts
- Avoid overly literal translations that sound unnatural
- Maintain professional and formal tone
- Ensure smooth readability for Chinese-speaking developers

### 3. Context Awareness
- Consider the target audience (developers, technical users)
- Adapt terminology to Chinese technical community standards
- Maintain consistency with existing Chinese technical documentation
- Consider cultural and linguistic nuances

## Common Translation Patterns

### Technical Instructions
**Pattern:** Imperative statements
- "Create a function..." → "创建一个函数..."
- "Implement the algorithm..." → "实现该算法..."
- "Ensure proper error handling..." → "确保适当的错误处理..."

### Explanations and Descriptions
**Pattern:** Declarative statements
- "This function calculates..." → "此函数计算..."
- "The algorithm uses..." → "该算法使用..."
- "The result shows..." → "结果显示..."

### Questions in Documentation
**Pattern:** Maintain question format
- "Why use iteration over recursion?" → "为什么使用迭代而非递归？"
- "What are the performance implications?" → "性能影响是什么？"

## Terminology Consistency

### Programming Concepts
| English | Chinese | Notes |
|---------|---------|-------|
| function | 函数 | 保留英文术语在括号中: `函数 (function)` |
| variable | 变量 | |
| method | 方法 | |
| class | 类 | |
| object | 对象 | |
| interface | 接口 | |
| parameter | 参数 | |
| argument | 实参 | 与 parameter 区分 |
| return value | 返回值 | |

### Performance and Analysis
| English | Chinese | Notes |
|---------|---------|-------|
| time complexity | 时间复杂度 | |
| space complexity | 空间复杂度 | |
| optimization | 优化 | |
| performance | 性能 | |
| efficiency | 效率 | |
| scalability | 可扩展性 | |

### Development Practices
| English | Chinese | Notes |
|---------|---------|-------|
| debugging | 调试 | |
| testing | 测试 | |
| deployment | 部署 | |
| version control | 版本控制 | |

## Formatting Guidelines

### Code Blocks
- Never translate code within ``` blocks
- Translate only comments within code
- Maintain proper indentation and syntax highlighting

### Mathematical Expressions
- Preserve all LaTeX expressions unchanged
- Translate surrounding explanatory text
- Maintain mathematical notation consistency

### Links and References
- Keep URLs unchanged
- Translate link text while maintaining the link target
- Preserve reference formatting

## Quality Checklist

Before finalizing translation, verify:

- [ ] All code blocks are unchanged
- [ ] Technical terms are correctly translated
- [ ] Mathematical expressions are preserved
- [ ] URLs and links remain functional
- [ ] Markdown formatting is maintained
- [ ] Chinese text flows naturally
- [ ] Technical concepts are accurately conveyed
- [ ] Terminology is consistent throughout
- [ ] Professional tone is maintained

## Common Pitfalls to Avoid

### 1. Over-literal Translation
❌ Bad: "执行这个函数"
✅ Good: "调用此函数" or "执行此函数"

### 2. Inconsistent Terminology
❌ Bad: Sometimes "函数", sometimes "功能" for the same concept
✅ Good: Consistently use "函数" for programming functions

### 3. Losing Technical Precision
❌ Bad: "快速" for "O(1) time complexity"
✅ Good: "常数时间复杂度" or "O(1) 时间复杂度"

### 4. Ignoring Context
❌ Bad: Translating "handle" as "处理" in all contexts
✅ Good: "处理" (process), "处理" (handle), "句柄" (handle as noun) based on context

## Style Guide

### Tone and Voice
- Use formal, professional language
- Avoid colloquialisms and slang
- Maintain objective, technical tone
- Use active voice where appropriate

### Sentence Structure
- Keep sentences clear and concise
- Use appropriate technical Chinese grammar
- Avoid overly complex sentence structures
- Maintain logical flow

### Punctuation and Formatting
- Use Chinese punctuation where appropriate (，。！？)
- Maintain code-related punctuation in English style
- Ensure consistent spacing around code elements
- Preserve original emphasis (bold, italic)