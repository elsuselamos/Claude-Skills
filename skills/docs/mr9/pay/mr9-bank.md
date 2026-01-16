# Claude Skills 开发指南：银行数据合并与SQL生成

## 概述

本文档描述了一个Claude Skills的开发流程，用于合并银行数据并生成SQL插入语句。

## 功能描述

该技能用于：
1. 读取固定的ot888银行数据文件
2. 合并用户提供的银行代码文件
3. 生成标准化的SQL插入语句

## 执行步骤

### 1. 准备工作

#### 固定数据文件：ot888_bank_filtered.md
```markdown
| id  | 银行名称                                        |
| :-- | :---------------------------------------------- |
| 332 | United Overseas Bank\(Thai\) PCL                |
| 333 | TMBThanachart Bank                              |
| 334 | TISCO Bank Public Company Limited               |
| 335 | Thai Credit Retail Bank                         |
| 336 | Sumitomo Mitsui Bank                            |
| 337 | Standard Chartered Bank\(Thai\)                 |
| 338 | SME Development Bank                            |
| 339 | Siam Commercial Bank                            |
| 340 | RHB Bank                                        |
| 341 | OCBC Bank                                       |
| 342 | Mizuho Bank, Ltd. Bangkok Branch                |
| 343 | Mega International Commercial Bank              |
| 344 | Land and Houses Bank                            |
| 345 | Krung Thai Bank                                 |
| 346 | Kiatnakin Phatra Bank                           |
| 347 | Kasikorn Bank                                   |
| 348 | Islamic Bank of Thailand                        |
| 349 | Industrial and Commercial Bank of China\(Thai\) |
| 350 | Indian Overseas Bank                            |
| 351 | Hongkong and Shanghai Bank                      |
| 352 | Government Savings Bank                         |
| 353 | Government Housing Bank                         |
| 354 | Deutsche Bank                                   |
| 355 | Citibank                                        |
| 356 | CIMB Thai Bank                                  |
| 357 | BNP Paribas                                     |
| 358 | Bank of China\(Thai\)                           |
| 359 | Krungsri\(Bank of Ayudhya\)                     |
| 360 | Bank for Agriculture and Agricultural           |
| 361 | BANK ABN AMRO                                   |
| 362 | Bangkok Bank                                    |
| 363 | ANZ Bank\(Thai\)                                |
| 364 | AIG Retail Bank Public Company Limited          |
```

该文件包含33家泰国银行的ID和名称信息，ID范围为332-364。此文件为固定参考数据，在技能执行时不需要用户提供。

#### 输入文件要求
- **文件名**: `${ARGS}.md`（由用户提供）
- **必需字段**:
    - 银行名称
    - 银行代码
- **格式**: Markdown表格

```
| 银行名称                                               | 银行代码                                            |
|:---------------------------------------------------|:------------------------------------------------|
| BANGKOK BANK                                       | 002                                             |
| Kasikornbank                                       | 004                                             |
| ...                                               | ...                                            |
```

### 2. 数据合并流程

#### 合并规则
创建一个新的合并文件（如 `merged_banks.md`），包含四个字段：

1. **id**
    - 来源：ot888_bank_filtered.md
    - 332-364的ID值
    - 只在SGpay中存在的银行使用"null"

2. **银行名称_ot888**
    - 来源：ot888_bank_filtered.md
    - 只在SGpay中存在的银行使用"null"

3. **银行名称_SGpay**
    - 来源：${ARGS}.md
    - 只在ot888中存在的银行使用"null"

4. **银行代码**
    - 来源：${ARGS}.md
    - 未匹配的银行代码为"null"

#### 合并策略
- 使用银行名称作为匹配键
- 模糊匹配银行名称（考虑大小写、空格、括号等差异）
- 无法匹配的记录保留为null值

### 3. SQL生成

#### 模板
```sql
INSERT INTO ${tenant}_channel_bank (channel_id, bank_id, recharge_bank_code, withdraw_bank_code, currency)
VALUES (1271, '#{id}', '#{银行代码}', '#{银行代码}', 'THB')
ON CONFLICT (channel_id, bank_id) DO NOTHING;
```

#### 参数说明
- `channel_id`: 固定值 1271
- `bank_id`: 从合并文件的id字段获取
- `recharge_bank_code`: 从合并文件的银行代码字段获取
- `withdraw_bank_code`: 同recharge_bank_code
- `currency`: 固定值 'THB'
- `${tenant}`: 租户变量，需要替换为实际值

#### 输出要求
- 生成文件名：`bank_inserts.sql`
- 按照id字段升序排序（null值放在最后）
- 每行一条INSERT语句

## 实现示例

### Python代码实现

```python
import re
import pandas as pd
from pathlib import Path

class BankDataMerger:
    def __init__(self, input_file):
        # 固定的ot888数据直接硬编码
        self.ot888_data = [
            ["332", "United Overseas Bank(Thai) PCL"],
            ["333", "TMBThanachart Bank"],
            ["334", "TISCO Bank Public Company Limited"],
            ["335", "Thai Credit Retail Bank"],
            ["336", "Sumitomo Mitsui Bank"],
            ["337", "Standard Chartered Bank(Thai)"],
            ["338", "SME Development Bank"],
            ["339", "Siam Commercial Bank"],
            ["340", "RHB Bank"],
            ["341", "OCBC Bank"],
            ["342", "Mizuho Bank, Ltd. Bangkok Branch"],
            ["343", "Mega International Commercial Bank"],
            ["344", "Land and Houses Bank"],
            ["345", "Krung Thai Bank"],
            ["346", "Kiatnakin Phatra Bank"],
            ["347", "Kasikorn Bank"],
            ["348", "Islamic Bank of Thailand"],
            ["349", "Industrial and Commercial Bank of China(Thai)"],
            ["350", "Indian Overseas Bank"],
            ["351", "Hongkong and Shanghai Bank"],
            ["352", "Government Savings Bank"],
            ["353", "Government Housing Bank"],
            ["354", "Deutsche Bank"],
            ["355", "Citibank"],
            ["356", "CIMB Thai Bank"],
            ["357", "BNP Paribas"],
            ["358", "Bank of China(Thai)"],
            ["359", "Krungsri(Bank of Ayudhya)"],
            ["360", "Bank for Agriculture and Agricultural"],
            ["361", "BANK ABN AMRO"],
            ["362", "Bangkok Bank"],
            ["363", "ANZ Bank(Thai)"],
            ["364", "AIG Retail Bank Public Company Limited"]
        ]

        self.input_file = input_file
        self.output_file = "merged_banks.md"
        self.sql_file = "bank_inserts.sql"

    def read_markdown_table(self, file_path):
        """读取Markdown表格文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 跳过表头和分隔行
        data_lines = [line.strip() for line in lines[3:] if line.strip() and not line.startswith('| :--')]

        data = []
        for line in data_lines:
            # 提取表格内容
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            data.append(cells)

        return data

    def normalize_bank_name(self, name):
        """标准化银行名称以便匹配"""
        # 移除特殊字符和空格
        name = re.sub(r'[\\()\\-\\s]', '', name.lower())
        # 统一常见银行名称
        name = name.replace('thai', 'thailand')
        name = name.replace('bankofchina', 'bankofchina(thai)')
        return name

    def merge_data(self):
        """合并银行数据"""
        # 创建ot888 DataFrame
        ot888_df = pd.DataFrame(self.ot888_data, columns=['id', 'bank_name_ot888'])

        # 读取输入数据
        input_data = self.read_markdown_table(self.input_file)
        input_df = pd.DataFrame(input_data, columns=['bank_name_sgpay', 'bank_code'])

        # 创建匹配字典
        ot888_dict = {}
        for _, row in ot888_df.iterrows():
            normalized = self.normalize_bank_name(row['bank_name_ot888'])
            ot888_dict[normalized] = {
                'id': row['id'],
                'bank_name_ot888': row['bank_name_ot888']
            }

        # 合并数据
        merged = []
        used_ids = set()

        # 处理ot888中的银行
        for _, row in ot888_df.iterrows():
            normalized = self.normalize_bank_name(row['bank_name_ot888'])
            match = input_df[
                input_df['bank_name_sgpay'].apply(lambda x: self.normalize_bank_name(x)) == normalized
            ]

            if not match.empty:
                match_row = match.iloc[0]
                merged.append({
                    'id': row['id'],
                    'bank_name_ot888': row['bank_name_ot888'],
                    'bank_name_sgpay': match_row['bank_name_sgpay'],
                    'bank_code': match_row['bank_code']
                })
                used_ids.add(match_row['bank_name_sgpay'])
            else:
                merged.append({
                    'id': row['id'],
                    'bank_name_ot888': row['bank_name_ot888'],
                    'bank_name_sgpay': 'null',
                    'bank_code': 'null'
                })

        # 处理只在输入文件中的银行
        for _, row in input_df.iterrows():
            if row['bank_name_sgpay'] not in used_ids:
                merged.append({
                    'id': 'null',
                    'bank_name_ot888': 'null',
                    'bank_name_sgpay': row['bank_name_sgpay'],
                    'bank_code': row['bank_code']
                })

        # 创建DataFrame并排序
        merged_df = pd.DataFrame(merged)
        merged_df['id_sort'] = merged_df['id'].apply(lambda x: 999999 if x == 'null' else int(x))
        merged_df = merged_df.sort_values('id_sort').drop('id_sort', axis=1)

        return merged_df

    def save_merged_data(self, df):
        """保存合并后的数据"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write("| id  | 银行名称_ot888                                 | 银行名称_SGpay                                 | 银行代码                                           |\n")
            f.write("| :-- | :-------------------------------------------- | :-------------------------------------------- | :----------------------------------------------- |\n")

            for _, row in df.iterrows():
                f.write(f"| {row['id']} | {row['bank_name_ot888']} | {row['bank_name_sgpay']} | {row['bank_code']} |\n")

    def generate_sql(self, df):
        """生成SQL语句"""
        with open(self.sql_file, 'w', encoding='utf-8') as f:
            for _, row in df.iterrows():
                sql = f"""INSERT INTO ${{tenant}}_channel_bank (channel_id, bank_id, recharge_bank_code, withdraw_bank_code, currency) VALUES (1271, '{row['id']}', '{row['bank_code']}', '{row['bank_code']}', 'THB') ON CONFLICT (channel_id, bank_id) DO NOTHING;\n"""
                f.write(sql)

    def process(self):
        """执行完整流程"""
        print("开始合并数据...")
        merged_df = self.merge_data()

        print("保存合并数据...")
        self.save_merged_data(merged_df)

        print("生成SQL语句...")
        self.generate_sql(merged_df)

        print(f"处理完成！输出文件：{self.output_file} 和 {self.sql_file}")

# 使用示例
if __name__ == "__main__":
    merger = BankDataMerger("input_bank_codes.md")
    merger.process()
```

### Claude Skills实现

使用Claude的Skill工具，可以简化上述流程：

```python
# skill.py
from typing import Dict, List
import pandas as pd

def process_bank_merge(args: Dict) -> Dict:
    """
    处理银行数据合并任务

    Args:
        args: 包含输入文件路径的字典
              - input_file: 输入文件路径

    Returns:
        Dict: 包含输出文件路径的字典
    """
    input_file = args.get("input_file")

    # 使用Claude的工具链执行流程
    # 1. 读取固定文件
    # 2. 读取输入文件
    # 3. 合并数据
    # 4. 生成SQL

    return {
        "status": "success",
        "merged_file": "merged_banks.md",
        "sql_file": "bank_inserts.sql"
    }
```

## 使用说明

### 命令行使用
```bash
# 调用技能
/skill bank-merge-processor --input-file=your_bank_data.md
```

### 参数说明
- `--input-file`: 必需，包含银行名称和银行代码的Markdown文件路径
- `--channel-id`: 可选，默认为1271
- `--currency`: 可选，默认为'THB'
- `--tenant`: 可选，SQL中的租户变量

### 输出文件
1. `merged_banks.md` - 合并后的银行数据
2. `bank_inserts.sql` - 生成的SQL插入语句

## 测试用例

### 测试数据1
```markdown
# test_input.md
| 银行名称 | 银行代码 |
|:---------|:---------|
| Bangkok Bank | 002 |
| Kasikornbank | 004 |
| Test Bank | 999 |
```

### 预期输出
- 合并文件应包含所有ot888银行和Test Bank
- SQL文件应按id排序生成
- Test Bank的id应为'null'

## 注意事项

1. **文件编码**: 所有文件应使用UTF-8编码
2. **数据清洗**: 银行名称需要标准化处理
3. **错误处理**: 缺少必需字段时应给出明确错误提示
4. **性能**: 大量数据时应考虑批处理
5. **日志**: 记录合并统计信息（匹配数、未匹配数等）

## 扩展功能

1. **支持更多字段**: 可扩展支持更多银行属性
2. **批量处理**: 支持处理多个输入文件
3. **自定义模板**: 允许用户自定义SQL模板
4. **数据验证**: 添加银行代码格式验证
5. **导出格式**: 支持CSV、JSON等多种导出格式