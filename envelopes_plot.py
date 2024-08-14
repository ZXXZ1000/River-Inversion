import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import ScalarFormatter

# Load the data
data_path = r"D:\OneDrive - zju.edu.cn\文档\MATLAB 代码\Min-inversion\new inversion 0604\output.csv"  # 修改为您的文件路径
data = pd.read_csv(data_path)

# Convert column names to numeric values, except for 'basin'
data.columns = ['basin'] + [float(col) for col in data.columns[1:]]

# Extract basin numbers
data['basin_number'] = data['basin'].apply(lambda x: int(x.split('_')[1]))

# Define groups
group1 = data[data['basin_number'].isin([ 22,2,13,18])]
group2 = data[data['basin_number'].isin([ 21,19,6])]

# Select time points between 0 and 2
time_points_selected = [col for col in group1.columns[1:-1] if 0 <= float(col) <= 3]

# Function to plot envelopes and mean trends
def plot_combined_envelopes_only(group1, group2, time_points, title):
    time_points_float = np.array([float(time) for time in time_points])
    
    plt.figure(figsize=(8, 6))
    inset_axes = plt.gca().inset_axes([0.65, 0.65, 0.3, 0.3])

    # Process and plot Group 1, ignoring zeros
    values_g1 = group1[time_points].replace(0, np.nan).values.astype(float)
    mean_values_g1 = np.nanmean(values_g1, axis=0)
    std_dev_g1 = np.nanstd(values_g1, axis=0)
    plt.fill_between(time_points_float, mean_values_g1 - std_dev_g1, mean_values_g1 + std_dev_g1, alpha=0.4, color='#A3C1D9', label='Standard Deviation')
    plt.step(time_points_float, mean_values_g1, '#1A65A0', linewidth=2, label='Beheaded Fujiang (basin 1,6,8,11)')
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    for value in values_g1:
        #平滑曲线
        value = np.convolve(value, np.ones(5)/5, mode='same')
        mask = value != 0
        inset_axes.step(time_points_float[mask], value[mask], alpha=0.8, color='#1A65A0', zorder=2)

    # Process and plot Group 2
    values_g2 = group2[time_points].replace(0, np.nan).values.astype(float)
    mean_values_g2 = np.nanmean(values_g2, axis=0)
    std_dev_g2 = np.nanstd(values_g2, axis=0)
    for value in values_g2:
        value = np.convolve(value, np.ones(5)/5, mode='same')
        mask = value != 0
        inset_axes.step(time_points_float[mask], value[mask], alpha=0.8, color='#B32626', zorder=2)
    plt.fill_between(time_points_float, mean_values_g2 - std_dev_g2, mean_values_g2 + std_dev_g2, alpha=0.4, color='#FDD4C2', label='Standard Deviation')
    plt.plot(time_points_float, mean_values_g2, '#B32626', linewidth=2, label='Mordern Minjiang (basin 2,3,4,5,7)')

    #绘制两组数据的峰值垂线, y值不超过max(mean_values_g1)
    #plt.axvline(x= max(time_points_float[mean_values_g1 == max(mean_values_g1)]), color='#1A65A0', linestyle='--', linewidth=1.5)
    #plt.axvline(x= max(time_points_float[mean_values_g2 == max(mean_values_g2)]), color='#B32626', linestyle='--', linewidth=1.5)
    #标注垂线x坐标值
    x1= max(time_points_float[mean_values_g1 == (max(mean_values_g1))] )
    plt.text(x1 , max(mean_values_g1), f"{x1:.2f}", color='#1A65A0',fontsize=12, weight='bold', fontstyle='italic',)
    #plt.scatter(x1, max(mean_values_g1), marker='*', color='black', s=80, zorder=3)
    x2= max(time_points_float[mean_values_g2 == max(mean_values_g2)])
    plt.text(x2 , max(mean_values_g2)+0.01, f"{x2:.2f}", color='#B32626',fontsize=12, weight='bold', fontstyle='italic',)
    plt.scatter(x2, max(mean_values_g2), marker='*', color='#B32626', s=100, zorder=3)
    #绘图
    plt.title('Envelope Plot of Tribu Inversed', fontsize=16, weight='bold')
    plt.xlabel('Time (Myr)', fontsize=14, weight='bold', fontstyle='italic')
    plt.ylabel('Uplift Rate (mm/yr)', fontsize=14, weight='bold')
    plt.xlim(0, 3)
    plt.ylim(0, 0.8)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.4)
    inset_axes.grid(True, linestyle='--', alpha=0.4)
    inset_axes.set_xlim(0, 3)
    inset_axes.set_ylim(0, 1.0)
    inset_axes.set_xlabel('Time (Myr)', fontsize=8)
    inset_axes.set_ylabel('Uplift Rate (mm/yr)', fontsize=8)
   
    plt.show()

# Plot envelopes only for both groups
plot_combined_envelopes_only(group1, group2, time_points_selected, 'Envelope Plot')
