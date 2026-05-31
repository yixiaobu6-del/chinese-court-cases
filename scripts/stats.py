#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国法院案例统计分析工具

用法:
    python stats.py                     # 显示完整统计
    python stats.py --type              # 案由分布
    python stats.py --year              # 年份分布
    python stats.py --region            # 地区分布
"""

import json
import argparse
import sys
import os
from collections import Counter
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


def print_bar(value: int, max_value: int, width: int = 30) -> str:
    """生成文本进度条"""
    filled = int(width * value / max_value) if max_value > 0 else 0
    return '█' * filled + '░' * (width - filled)


def parse_amount(amount_str: str) -> float:
    """解析涉案金额"""
    if not amount_str:
        return 0
    amount_str = amount_str.replace('万元', '')
    try:
        if '万' in amount_str:
            return float(amount_str.replace('万', '')) * 10000
        return float(amount_str)
    except ValueError:
        return 0


def print_overall_stats(cases: List[Dict]):
    """打印总体统计"""
    print("\n" + "=" * 60)
    print("          中国法院案例 统计分析")
    print("=" * 60)

    print(f"\n📊 总体数据:")
    print(f"   案例总数: {len(cases)}")

    # 案件类型分布
    type_counter = Counter(c.get('case_type', '未知') for c in cases)
    print(f"\n📂 案件类型分布:")
    max_count = max(type_counter.values())
    for t, count in sorted(type_counter.items(), key=lambda x: -x[1]):
        bar = print_bar(count, max_count)
        print(f"   {t}: {bar} {count} ({count/len(cases)*100:.1f}%)")

    # 案由分布
    cause_counter = Counter(c.get('cause', '未知') for c in cases)
    print(f"\n🏷️  热门案由 (Top 10):")
    max_count = max(count for _, count in cause_counter.most_common(10)) if cause_counter else 1
    for cause, count in cause_counter.most_common(10):
        bar = print_bar(count, max_count)
        print(f"   {cause[:16]:16s} {bar} {count}")

    # 地区分布
    region_counter = Counter(c.get('region', '未知') for c in cases)
    print(f"\n📍 地区分布:")
    for region, count in sorted(region_counter.items(), key=lambda x: -x[1]):
        print(f"   {region}: {count}")

    # 月份分布（基于判决日期）
    year_counter = Counter(c.get('judge_date', '')[:7] for c in cases if c.get('judge_date'))
    print(f"\n📅 判决月份分布:")
    for ym, count in sorted(year_counter.items()):
        print(f"   {ym}: {'█' * count} {count}")

    # 涉案金额统计
    amounts = [parse_amount(c.get('amount', '')) for c in cases]
    amounts = [a for a in amounts if a > 0]
    if amounts:
        print(f"\n💰 涉案金额统计:")
        print(f"   最高: {max(amounts):,.0f}元")
        print(f"   最低: {min(amounts):,.0f}元")
        print(f"   平均: {sum(amounts)/len(amounts):,.0f}元")
        print(f"   中位数: {sorted(amounts)[len(amounts)//2]:,.0f}元")

    print("\n" + "=" * 60)


def print_type_distribution(cases: List[Dict]):
    """打印案由分布"""
    print("\n" + "=" * 60)
    print("           案由分布")
    print("=" * 60 + "\n")

    cause_counter = Counter(c.get('cause', '未知') for c in cases)
    total = len(cases)

    for cause, count in sorted(cause_counter.items(), key=lambda x: -x[1]):
        percentage = count / total * 100
        bar = '█' * int(percentage) + '░' * (50 - int(percentage))
        print(f"  {cause[:20]:20s} {bar} {count}条 ({percentage:.1f}%)")

    print(f"\n  共计 {len(cause_counter)} 个案由")
    print("=" * 60 + "\n")


def print_year_distribution(cases: List[Dict]):
    """打印年份分布"""
    print("\n" + "=" * 60)
    print("           判决年份分布")
    print("=" * 60 + "\n")

    year_counter = Counter(c.get('judge_date', '')[:4] for c in cases if c.get('judge_date'))
    total = sum(year_counter.values())
    max_count = max(year_counter.values())

    for year in sorted(year_counter.keys()):
        count = year_counter[year]
        percentage = count / total * 100 if total else 0
        bar = print_bar(count, max_count)
        print(f"  {year}: {bar} {count}条 ({percentage:.1f}%)")

    print("=" * 60 + "\n")


def print_region_distribution(cases: List[Dict]):
    """打印地区分布"""
    print("\n" + "=" * 60)
    print("           地区分布")
    print("=" * 60 + "\n")

    region_counter = Counter(c.get('region', '未知') for c in cases)
    total = len(cases)
    max_count = max(region_counter.values())

    for region, count in sorted(region_counter.items(), key=lambda x: -x[1]):
        percentage = count / total * 100
        bar = print_bar(count, max_count)
        print(f"  {region[:8]:8s} {bar} {count}条 ({percentage:.1f}%)")

    print(f"\n  覆盖 {len(region_counter)} 个地区")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='中国法院案例统计分析工具'
    )

    parser.add_argument('--type', '-t', action='store_true', help='案由分布')
    parser.add_argument('--year', '-y', action='store_true', help='年份分布')
    parser.add_argument('--region', '-r', action='store_true', help='地区分布')

    args = parser.parse_args()

    cases = load_data('cases_sample.json')
    if not cases:
        sys.exit(1)

    if args.type:
        print_type_distribution(cases)
    elif args.year:
        print_year_distribution(cases)
    elif args.region:
        print_region_distribution(cases)
    else:
        print_overall_stats(cases)


if __name__ == '__main__':
    main()