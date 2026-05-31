#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国法院案例检索工具

用法:
    python search.py "合同"                # 搜索关键词
    python search.py --type "民事"         # 按案件类型
    python search.py --cause "买卖合同"     # 按案由
    python search.py --region "北京"       # 按地区
    python search.py --amount-min 100000   # 按最低涉案金额
"""

import json
import argparse
import sys
import os
from typing import List, Dict, Any


def load_data(filename: str) -> List[Dict[str, Any]]:
    """加载数据文件"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到数据文件 {data_path}")
        return []
    except json.JSONDecodeError:
        print(f"错误: 数据文件格式错误 {data_path}")
        return []


def parse_amount(amount_str: str) -> float:
    """解析涉案金额为数字"""
    if not amount_str:
        return 0
    amount_str = amount_str.replace('万元', '').replace('元', '').replace('房产一套', '500').replace(' ', '')
    try:
        return float(amount_str) * 10000 if '万' not in amount_str else float(amount_str.strip()) * 10000
    except ValueError:
        return 0


def print_case(case: Dict):
    """格式化打印案例"""
    print("=" * 60)
    print(f"  📋 {case['title']}")
    print(f"  🏛️  法院: {case['court']}")
    print(f"  📂 类型: {case['case_type']}  |  案由: {case['cause']}")
    print(f"  👤 原告: {case['plaintiff']}")
    print(f"  👤 被告: {case['defendant']}")
    print(f"  📅 日期: {case['judge_date']}  |  地区: {case['region']}")

    if case.get('amount'):
        print(f"  💰 涉案金额: {case['amount']}")

    print(f"\n  📝 裁判理由:")
    print(f"     {case['reasoning']}")

    print(f"\n  ⚖️  判决结果:")
    print(f"     {case['judgment']}")

    if case.get('legal_basis'):
        print(f"\n  📚 法律依据:")
        for basis in case['legal_basis']:
            print(f"     - {basis}")

    print("=" * 60)
    print()


def main():
    parser = argparse.ArgumentParser(
        description='中国法院案例检索工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python search.py "合同"                  # 关键词搜索
    python search.py --type "民事"           # 按类型
    python search.py --cause "买卖合同纠纷"   # 按案由
    python search.py --region "广东"         # 按地区
    python search.py --amount-min 100000     # 按金额
        """
    )

    parser.add_argument('keyword', nargs='?', help='搜索关键词')
    parser.add_argument('--type', '-t', choices=['民事', '刑事', '行政'], help='案件类型过滤')
    parser.add_argument('--cause', '-c', help='案由过滤')
    parser.add_argument('--region', '-r', help='地区过滤')
    parser.add_argument('--amount-min', type=int, help='最低涉案金额（元）')
    parser.add_argument('--limit', '-l', type=int, default=20, help='结果数量限制')

    args = parser.parse_args()

    cases = load_data('cases_sample.json')
    if not cases:
        sys.exit(1)

    results = cases.copy()

    # 关键词搜索
    if args.keyword:
        kw = args.keyword.lower()
        results = [
            c for c in results
            if kw in c.get('title', '').lower()
            or kw in c.get('reasoning', '').lower()
            or kw in c.get('judgment', '').lower()
            or kw in c.get('summary', '').lower()
            or kw in c.get('cause', '').lower()
        ]

    # 过滤
    if args.type:
        results = [c for c in results if c.get('case_type') == args.type]
    if args.cause:
        results = [c for c in results if args.cause in c.get('cause', '')]
    if args.region:
        results = [c for c in results if args.region in c.get('region', '')]
    if args.amount_min:
        results = [c for c in results if parse_amount(c.get('amount', '')) >= args.amount_min]

    if not results:
        print("未找到匹配的案例。")
        sys.exit(0)

    print(f"\n找到 {len(results)} 条结果:\n")
    for case in results[:args.limit]:
        print_case(case)

    if len(results) > args.limit:
        print(f"... (还有 {len(results) - args.limit} 条未显示)")


if __name__ == '__main__':
    main()