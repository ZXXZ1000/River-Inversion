import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the data
data_path = r'D:\OneDrive - zju.edu.cn\文档\MATLAB 代码\河流反演\test4\output_refit.csv'  # 修改为您的文件路径
data = pd.read_csv(data_path)

# Convert column names to numeric values, except for 'basin'
data.columns = ['basin'] + [float(col) for col in data.columns[1:]]

# Extract basin numbers
data['basin_number'] = data['basin'].apply(lambda x: int(x.split('_')[1]))

# Define groups
group1 = data[data['basin_number'].isin([1,4])]
group2 = data[data['basin_number'].isin([7,5])]
group3 = data[data['basin_number'].isin([6, 10])]
group4 = data[data['basin_number'].isin([3])]

# Select time points between 0 and 2
time_points_selected = [col for col in group1.columns[1:-1] if 0 <= float(col) <= 2]

# Function to plot envelopes and mean trends
def plot_combined_envelopes_only(group1, group2, time_points, title):
    time_points_float = np.array([float(time) for time in time_points])
    
    plt.figure(figsize=(9, 6))

    # Process and plot Group 1, ignoring zeros
    values_g1 = group1[time_points].replace(0, np.nan).values.astype(float)
    mean_values_g1 = np.nanmean(values_g1, axis=0)
    std_dev_g1 = np.nanstd(values_g1, axis=0)
    #for value in values_g1:
        #mask = value != 0
        #plt.scatter(time_points_float[mask], value[mask], alpha=0.4, color='blue', s=1, zorder=2)
    plt.fill_between(time_points_float, mean_values_g1 - std_dev_g1, mean_values_g1 + std_dev_g1, alpha=0.2, color='blue')
    plt.plot(time_points_float, mean_values_g1, 'b-', linewidth=2, label='Northen Tribu1 (basin1)')

    # Process and plot Group 2
    values_g2 = group2[time_points].replace(0, np.nan).values.astype(float)
    mean_values_g2 = np.nanmean(values_g2, axis=0)
    std_dev_g2 = np.nanstd(values_g2, axis=0)
    #for value in values_g2:
        #mask = value != 0
        #plt.scatter(time_points_float[mask], value[mask], alpha=0.4, color='orange', s=1, zorder=2)
    plt.fill_between(time_points_float, mean_values_g2 - std_dev_g2, mean_values_g2 + std_dev_g2, alpha=0.2, color='orange')
    plt.plot(time_points_float, mean_values_g2, 'r-', linewidth=2, label='Northen Tribu2 (basin7,5,8)')

    # Process and plot Group 3
    values_g3 = group3[time_points].replace(0, np.nan).values.astype(float)
    mean_values_g3 = np.nanmean(values_g3, axis=0)
    std_dev_g3 = np.nanstd(values_g3, axis=0)
    #for value in values_g3:
        #mask = value != 0
        #plt.scatter(time_points_float[mask], value[mask], alpha=0.4, color='green', s=1, zorder=2)
    plt.fill_between(time_points_float, mean_values_g3 - std_dev_g3, mean_values_g3 + std_dev_g3, alpha=0.2, color='green')
    plt.plot(time_points_float, mean_values_g3, 'g-', linewidth=2, label='Northen Tribu3 (basin6,10)')
    
    # Process and plot Group 4
    values_g4 = group4[time_points].replace(0, np.nan).values.astype(float)
    mean_values_g4 = np.nanmean(values_g4, axis=0)
    std_dev_g4 = np.nanstd(values_g4, axis=0)
    #for value in values_g4:
        #mask = value != 0
        #plt.scatter(time_points_float[mask], value[mask], alpha=0.4, color='purple', s=1, zorder=2)
    plt.fill_between(time_points_float, mean_values_g4 - std_dev_g4, mean_values_g4 + std_dev_g4, alpha=0.2, color='purple')
    plt.plot(time_points_float, mean_values_g4, 'm-', linewidth=2, label='Northen Tribu4 (basin3,9)')
    
    #绘制两组数据的峰值垂线, y值不超过max(mean_values_g1)
    #plt.axvline(x= max(time_points_float[mean_values_g1 == max(mean_values_g1)]), color='blue', linestyle='--', linewidth=1.5)
    #plt.axvline(x= max(time_points_float[mean_values_g2 == max(mean_values_g2)]), color='red', linestyle='--', linewidth=1.5)
    #标注垂线x坐标值
    #x1= max(time_points_float[mean_values_g1 == max(mean_values_g1)])
    #plt.text(x1 , 0.1, f"{x1:.2f}", color='blue')
    #x2= max(time_points_float[mean_values_g2 == max(mean_values_g2)])
    #plt.text(x2 , 0.1, f"{x2:.2f}", color='red')
    #绘图
    plt.title(title)
    plt.xlabel('Time (Myr)')
    plt.ylabel('Uplift Rate (mm/yr)')
    plt.xlim(0, 2)
    plt.ylim(0, 2.5)
    plt.legend()
    plt.grid(False)
    plt.show()

# Plot envelopes only for both groups
plot_combined_envelopes_only(group1, group2, time_points_selected, 'Envelope Plot')
