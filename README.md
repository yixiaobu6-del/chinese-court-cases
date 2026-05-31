# Chinese Court Cases - 中国法院案例检索系统

> 结构化中国法院案例数据集及检索工具，适用于法律研究、AI训练、法学教育

---

## Features / 功能特点

| 功能 | 说明 |
|------|------|
| 完整数据结构 | 14个标准化字段，包含案号、法院、案件类型等 |
| 三大诉讼类型 | 覆盖民事、刑事、行政三大诉讼分类 |
| 命令行检索 | 支持关键词、案由、法院、地区多维度搜索 |
| 统计分析 | 案由分布、年份分布、地区分布统计 |
| 结构化JSON | 标准化JSON格式，便于程序化处理 |
| 脱敏处理 | 基于裁判文书网公开数据，经脱敏处理 |

## Installation / 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/chinese-court-cases.git

cd chinese-court-cases

# Python 3.6+ 即可运行
python scripts/search.py --help
```

## Usage / 使用方法

### 命令行检索

```bash
# 搜索关键词
python scripts/search.py "合同"

# 按案件类型
python scripts/search.py --type "民事"

# 按案由
python scripts/search.py --cause "买卖合同纠纷"

# 按地区
python scripts/search.py --region "广东"

# 统计分析
python scripts/stats.py

# 统计案由分布
python scripts/stats.py --type

# 统计年份分布
python scripts/stats.py --year

# 统计地区分布
python scripts/stats.py --region
```

### 数据结构说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | string | 案例编号 | "case_001" |
| title | string | 案例标题 | "张三诉李四合同纠纷案" |
| court | string | 审理法院 | "北京市朝阳区人民法院" |
| case_type | string | 案件类型 | "民事" |
| cause | string | 案由 | "买卖合同纠纷" |
| plaintiff | string | 原告/公诉机关 | "张三" |
| defendant | string | 被告 | "李四" |
| judge_date | string | 判决日期 | "2023-06-15" |
| judgment | string | 判决结果 | "被告应于本判决生效之日起十日内..." |
| reasoning | string | 法院认为（裁判理由） | "本院认为，本案争议焦点为..." |
| legal_basis | array[string] | 法律依据 | `["合同法第107条"]` |
| amount | string | 涉案金额 | "500000" |
| region | string | 地区 | "北京市" |
| summary | string | 案例摘要 | "本案系买卖合同纠纷..." |

### Python 模块使用示例

```python
import json

# 加载案例数据
with open('data/cases.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)

# 按类型筛选
civil_cases = [c for c in cases if c['case_type'] == '民事']

# 按地区搜索
guangdong_cases = [c for c in cases if c['region'] == '广东']

# 关键词搜索
contract_cases = [c for c in cases if '合同' in c['summary']]
```

## Contributing / 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)

欢迎贡献：
- 补充案例数据
- 改进检索脚本
- 添加可视化功能
- 报告数据问题

## License / 许可证

MIT License - 参见 [LICENSE](LICENSE)

---

> 版本：1.0.0 | 更新日期：2026-05-30