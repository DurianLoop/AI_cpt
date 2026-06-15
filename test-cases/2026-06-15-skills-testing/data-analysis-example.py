import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 生成模拟的电商销售数据
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', end='2024-06-15', freq='D')

data = {
    'date': dates,
    'revenue': np.random.normal(50000, 10000, len(dates)) + \
               np.sin(np.arange(len(dates)) * 2 * np.pi / 7) * 5000,  # 周期性
    'orders': np.random.poisson(500, len(dates)),
    'new_customers': np.random.poisson(100, len(dates)),
    'returning_customers': np.random.poisson(400, len(dates))
}

df = pd.DataFrame(data)
df['revenue'] = df['revenue'].clip(lower=20000)
df['avg_order_value'] = df['revenue'] / df['orders']

# 基础统计分析
print("=== 销售数据统计摘要 ===\n")
print(f"数据时间范围: {df['date'].min().date()} 至 {df['date'].max().date()}")
print(f"总订单数: {df['orders'].sum():,}")
print(f"总收入: ${df['revenue'].sum():,.2f}")
print(f"平均客单价: ${df['avg_order_value'].mean():.2f}")
print(f"客户总数: {(df['new_customers'].sum() + df['returning_customers'].sum()):,}")
print(f"回头客占比: {(df['returning_customers'].sum() / (df['new_customers'].sum() + df['returning_customers'].sum()) * 100):.1f}%")

# 趋势分析
print("\n=== 月度趋势分析 ===\n")
df['month'] = df['date'].dt.to_period('M')
monthly = df.groupby('month').agg({
    'revenue': 'sum',
    'orders': 'sum',
    'new_customers': 'sum',
    'returning_customers': 'sum'
})

for month in monthly.index:
    print(f"{month}: 收入 ${monthly.loc[month, 'revenue']:,.0f}, "
          f"订单 {monthly.loc[month, 'orders']:,}, "
          f"新客 {monthly.loc[month, 'new_customers']:,}, "
          f"回客 {monthly.loc[month, 'returning_customers']:,}")

# 保存结果
df.to_csv('sales_data.csv', index=False)
print("\n数据已保存到 sales_data.csv")

# 可视化建议
print("\n=== 可视化建议 ===")
print("1. 时序图: 展示每日收入和订单量趋势")
print("2. 柱状图: 对比各月的收入和客户增长")
print("3. 饼图: 新客vs回客占比")
print("4. 散点图: 订单量与收入的相关性")
