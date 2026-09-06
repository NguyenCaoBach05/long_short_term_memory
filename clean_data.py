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

#EDA
#%%
# 1. Lấy danh sách cột số
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

# 2. In trực tiếp chi tiết các mốc bất thường theo Z-score để kiểm tra
for col in ['milled_products', 'fats_oils', 'sugar', 'petroleum', 'fertilizer']:
    z_score = (df[col] - df[col].mean()) / df[col].std()
    outlier_mask = z_score.abs() > 3.0
    if outlier_mask.any():
        print(f"\n--- Chi tiết bất thường cột: {col} ---")
        print(df.loc[outlier_mask, ['Date', col]])


#%%
import matplotlib.pyplot as plt
import seaborn as sns

# Vẽ boxplot để phát hiện ngoại lai nhanh trên toàn bộ 11 cột
# Chuẩn hóa tạm thời để hiển thị chung một thang đo (vì các loại hàng có sản lượng lệch nhau)
df_normalized = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
plt.figure(figsize=(14, 6))
sns.boxplot(data=df_normalized)
plt.xticks(rotation=45)
plt.title("Phát hiện ngoại lai nhanh trên toàn bộ 11 cột (Z-score Boxplot)")
plt.tight_layout()
plt.show()


#%% Gộp cột lại thành total_bulk.
df['total_bulk'] = df[numeric_cols].sum(axis=1)

# Xem thống kê và vẽ đường xu hướng tổng
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))
plt.plot(df['Date'], df['total_bulk'], label='Total Bulk Cargo', color='navy')
plt.title('Tổng sản lượng hàng rời qua thời gian (Total Bulk Cargo)')
plt.grid(True)
plt.show()