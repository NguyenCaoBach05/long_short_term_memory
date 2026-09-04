#%%
import pandas as pd

df = pd.read_excel('Master_Data.xlsx', sheet_name='master_data')

df.info()
df.drop(columns=['Measures'], inplace=True)

# Convert 'Year' and 'Month' columns to a single 'Date' column
month_num = df['Month'].astype(str).str.extract(r'(\d+)')[0]
df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + month_num + '-01')
df.drop(columns=['Year', 'Month'], inplace=True)

#%%
df.head()
print(df.isnull().sum())
df.describe()

pd.set_option('display.float_format', lambda x: '%.2f' % x)
df.describe()


# Lấy tháng xảy ra giá trị max
peak_month = df.loc[df['milled_products'].idxmax(), 'Date'].month

# Lọc tất cả các năm có cùng tháng đó để so sánh
same_months = df[df['Date'].dt.month == peak_month][['Date', 'milled_products']]
print(same_months)

# nhận thấy năm 2019 có giá trị là cao gấp 10 lần so với các năm khác, nên cho rằng
# đây là lỗi nhập liệu nên chia cho 10 để đưa về mức bình thường
import numpy as np

df.loc[43, 'milled_products'] = np.nan
df['milled_products'] = df['milled_products'].interpolate(method='linear')

# %%
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

# Đảm bảo index là Date và có tần suất tháng
df_ts = df.set_index('Date')['milled_products']
decomp = seasonal_decompose(df_ts, model='additive', period=12)

decomp.plot()
plt.tight_layout()
plt.show()

# %%
