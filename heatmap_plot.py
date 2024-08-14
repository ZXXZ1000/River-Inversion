import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import ScalarFormatter

# 加载数据，这里我们使用了相对路径，假设该脚本和CSV文件位于同一目录下
file_path =r"D:\OneDrive - zju.edu.cn\文档\MATLAB 代码\Min-inversion\new inversion 0604\output.csv"  # 修改为实际的相对路径或绝对路径
df = pd.read_csv(file_path, index_col=0)

# 定义感兴趣的盆地编号
basin_numbers = ['basin_6','basin_19','basin_21','basin_20','basin_2','basin_17','basin_13','basin_18','basin_16','basin_3']

# 由于原代码逻辑不适用于盆地编号作为行索引的情况，我们直接使用行索引来筛选数据
df_filtered = df.loc[basin_numbers]

# 应用对数变换
log_norm = mcolors.LogNorm(vmin=0.08, vmax=0.8)

# 转换列名为浮点数，以便比较（如果它们还不是浮点数）
df_filtered.columns = df_filtered.columns.astype(float)
# 选择时间范围，例如从0到5.0
start_time = 0.0
end_time = 5
# 选择这个范围内的列
df_limited = df_filtered.loc[:, (df_filtered.columns >= start_time) & (df_filtered.columns <= end_time)]

# 绘制热力图
fig, ax = plt.subplots(figsize=(12, 8))
ax = sns.heatmap(df_limited, norm=log_norm, cmap='coolwarm', cbar_kws={'label': 'Log(Uplift rate (mm/yr))'})
plt.title('Uplift Rate Heatmap')
plt.xlabel('Time (Myr)')
plt.ylabel('Basins')

# 减少x轴刻度数量
# 计算要显示的刻度数量，例如，只显示10个刻度
num_ticks = 10
tick_positions = np.linspace(0, len(df_limited.columns) - 1, num_ticks, dtype=int)  # 生成等间隔的刻度位置
tick_labels = [f"{float(df_limited.columns[pos]):.2f}" for pos in tick_positions]  # 根据刻度位置生成刻度标签

# 设置新的刻度标签
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=0)  # 同时可以调整标签的旋转角度

plt.gca().invert_yaxis()  # 可选：倒置y轴以符合常见的地质时间表示
# Set the colorbar with the logarithmic scale
cbar = ax.collections[0].colorbar
cbar.set_label('Log(Uplift rate (mm/yr))')
#设置colorbar的刻度格式为非科学计数法,小数保留两位
cbar.formatter= ScalarFormatter(useMathText=True)
cbar.update_ticks()
plt.tight_layout()
plt.show()
