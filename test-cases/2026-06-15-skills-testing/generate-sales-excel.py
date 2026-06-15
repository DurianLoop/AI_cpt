import pandas as pd
from datetime import datetime, timedelta
import random

# 生成产品销售数据
products = ['笔记本电脑', '台式机', '显示器', '键盘', '鼠标', '耳机', '充电器', 'USB线', '移动硬盘', '内存条']
regions = ['华北', '华东', '华南', '西南', '东北']
sales_channels = ['线上', '线下', '代理商']

data = []
start_date = datetime(2024, 1, 1)

for i in range(200):
    date = start_date + timedelta(days=random.randint(0, 165))
    product = random.choice(products)

    # 不同产品不同价格范围
    if product in ['笔记本电脑', '台式机']:
        price = random.randint(4000, 12000)
    elif product == '显示器':
        price = random.randint(1000, 5000)
    elif product in ['键盘', '鼠标']:
        price = random.randint(100, 500)
    elif product == '耳机':
        price = random.randint(200, 1500)
    else:
        price = random.randint(50, 300)

    quantity = random.randint(1, 50)

    data.append({
        '日期': date.strftime('%Y-%m-%d'),
        '产品': product,
        '地区': random.choice(regions),
        '销售渠道': random.choice(sales_channels),
        '单价': price,
        '数量': quantity,
        '销售额': price * quantity,
        '销售人员': f'员工{random.randint(1, 20):02d}'
    })

df = pd.DataFrame(data)
df = df.sort_values('日期')

# 保存为 Excel
with pd.ExcelWriter('sales_report.xlsx', engine='openpyxl') as writer:
    # 原始数据
    df.to_excel(writer, sheet_name='原始数据', index=False)

    # 产品统计
    product_summary = df.groupby('产品').agg({
        '销售额': 'sum',
        '数量': 'sum',
        '日期': 'count'
    }).rename(columns={'日期': '订单数'})
    product_summary['平均单价'] = product_summary['销售额'] / product_summary['数量']
    product_summary = product_summary.sort_values('销售额', ascending=False)
    product_summary.to_excel(writer, sheet_name='产品统计')

    # 地区统计
    region_summary = df.groupby('地区').agg({
        '销售额': 'sum',
        '数量': 'sum'
    }).sort_values('销售额', ascending=False)
    region_summary.to_excel(writer, sheet_name='地区统计')

    # 月度趋势
    df['月份'] = pd.to_datetime(df['日期']).dt.to_period('M')
    monthly = df.groupby('月份').agg({
        '销售额': 'sum',
        '数量': 'sum',
        '日期': 'count'
    }).rename(columns={'日期': '订单数'})
    monthly.to_excel(writer, sheet_name='月度趋势')

print("✅ Excel 文件已生成：sales_report.xlsx")
print(f"📊 总记录数：{len(df)}")
print(f"💰 总销售额：¥{df['销售额'].sum():,.2f}")
print(f"📦 总销售量：{df['数量'].sum():,} 件")
print(f"🏆 最畅销产品：{df.groupby('产品')['销售额'].sum().idxmax()}")
