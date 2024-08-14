import pandas as pd
import numpy as np

# 定义输入Excel文件路径
inversion_results_path = r"D:\OneDrive - zju.edu.cn\文档\MATLAB 代码\Min-inversion\new inversion 0604\反演结果.xlsx"

# 读取Excel文件以获取所有工作表的名称（basin编号）
xls = pd.ExcelFile(inversion_results_path)
sheet_names = xls.sheet_names

# 创建一个空DataFrame，其列为所有basin中出现的唯一tau值，行为basin编号
all_tau_values = set()
for sheet_name in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name, header=None, names=['tau', 'Uplift'])
    all_tau_values.update(df['tau'].unique())

all_tau_values = sorted(list(all_tau_values))
matrix_df = pd.DataFrame(columns=all_tau_values, index=sheet_names)
matrix_df.fillna(0, inplace=True)

# 填充DataFrame，使用每个basin的uplift数据
for sheet_name in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name, header=None, names=['tau', 'Uplift'])
    for _, row in df.iterrows():
        matrix_df.at[sheet_name, row['tau']] = row['Uplift']

# 将所有0值替换为NaN，以便进行插值
matrix_df.replace(0, np.nan, inplace=True)

# 对每一行应用线性插值
interpolated_df = matrix_df.apply(lambda row: row.interpolate(method='linear', limit_area='inside'), axis=1)

# 将那些插值后仍然为NaN的值替换回0（对于无法插值的行）
interpolated_df.fillna(0, inplace=True)

# 保存处理后的数据到CSV文件
interpolated_df.to_csv(r'D:\OneDrive - zju.edu.cn\文档\MATLAB 代码\Min-inversion\new inversion 0604\output.csv')
