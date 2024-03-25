import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 1. 读取CSV文件
df = pd.read_csv('data.csv')


# 2. 定义函数
def calculate_cost(row, e, alpha, b, c, d, g, mu):
    #tau = 2592000
    tau = 2592000
    A = row['Vm_ENS']
    r = row['distance']
    B = row['Rg']
    f = row['f']
    C = row['mean_Vm']

    cost = (1 / e) * (A ** alpha + b * (c * np.log(r) + d) + B) * tau + g * f + mu * C
    return cost


# 3. 计算函数值并添加到新列
e = 30000000000 # 可调参数
alpha = 2  # 可调参数
b = 1.3*10000  # 可调参数
c = 10**3  # 可调参数
d = 1  # 可调参数
g = 0  # 可调参数
mu = 2*1000  # 可调参数

df['pedestrian_cost'] = df.apply(calculate_cost, args=(e, alpha, b, c, d, g, mu), axis=1)

# 4. 显示函数值计算进度
total_rows = len(df)
for i, row in df.iterrows():
    progress = (i + 1) / total_rows * 100
    print(f"Calculating costs: {progress:.2f}% complete")

#df.to_csv('TSCH.csv', index=False)
# 5. 散点图可视化
plt.scatter(df['pedestrian_cost'], (10**30)/df['grid_attraction'], facecolors='none', edgecolors='b')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('pedestrian_cost')
plt.ylabel('β/μ')
plt.show()
