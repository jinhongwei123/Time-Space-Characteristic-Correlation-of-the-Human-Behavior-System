import pandas as pd
import transbigdata as tbd
import math
import numpy as np

# 读取原始数据
data_r_cm = pd.read_csv('C:\\论文编写程序\\第二篇论文编写程序\\回转半径\\stay_move.csv')
# 对“id”列进行去重操作
#data_r_cm['id'] = pd.factorize(data_r_cm['id'])[0]

# 定义轨迹质心函数
def r_cm(lon_sum,lat_sum,id_size):
    lon_mean = lon_sum /id_size
    lat_mean = lat_sum /id_size
    return lon_mean, lat_mean

# 定义回转半径函数
def r_g(idside, i_lon, i_lat, cm_lon, cm_lat):
    distances = [tbd.getdistance(i_lon, i_lat, cm_lon, cm_lat) for i_lon, i_lat in zip(i_lon, i_lat)]
    distances_result = [d**2 for d in distances]
    turning_radius = math.sqrt(sum(distances_result) / len(distances))
    return turning_radius

# 计算每个id的质心位置
data_r_cm['id'].fillna('null', inplace=True)
id_position_sum=data_r_cm.groupby(['id'], as_index=True)['elon', 'elat'].sum()
id_position_sum['id_count'] = data_r_cm.groupby(['id'])['elon'].size()
id_position_sum = pd.DataFrame(id_position_sum)
print(id_position_sum)

# 计算id个数
number = id_position_sum.iloc[:, 0].size

# 将数据转换为array形式
data_array_elon = np.array(id_position_sum['elon'])
data_array_elat = np.array(id_position_sum['elat'])
data_array_id_size = np.array(id_position_sum['id_count'])

# 将array转换为list形式
elon = data_array_elon.tolist()
elat = data_array_elat.tolist()
id_count = data_array_id_size.tolist()

# 计算每个id的质心位置，并增加一列id
r_cm_result = pd.DataFrame()
for x, y, z in zip(elon, elat, id_count):
    r_cm_result = r_cm_result.append(pd.DataFrame({'r_cm': [r_cm(x,y,z)], 'id': [len(r_cm_result)]}), ignore_index=True)

# 将元组拆包
for i in range(len(r_cm_result)):
    l1 = [list(j)[0] for j in r_cm_result['r_cm']]
    l2 = [list(k)[1] for k in r_cm_result['r_cm']]
r_cm_result['r_cm_lon'] = l1
r_cm_result['r_cm_lat'] = l2
print('id轨迹质心是：')
print(r_cm_result)

# 根据id将原始数据进行分组，并按照质心位置对数据进行处理
id_select = list(r_cm_result['id'])
id_select = list(set(id_select))
r_cm_loselect = list(r_cm_result['r_cm_lon'])
r_cm_laselect = list(r_cm_result['r_cm_lat'])
id_count = list(id_position_sum['id_count'])
df_end = pd.DataFrame({'id': [], 'id_side': [], 'elon': [], 'elat': [], 'cm_lon': [], 'cm_lat': []})
for i in range(len(id_select)):
    df1_data_r_cm = data_r_cm[data_r_cm['id'] == id_select[i]]
    id_side1 = id_count[id_select[i]]
    r_cm_lo,r_cm_la,id_side = [],[],[]
    for x in range(len(df1_data_r_cm)):
        r_cm_lo += [r_cm_loselect[i]]
        r_cm_la += [r_cm_laselect[i]]
        id_side += [id_side1]
    df1_data_r_cm['cm_lon'] = r_cm_lo
    df1_data_r_cm['cm_lat'] = r_cm_la
    df1_data_r_cm['id_side'] = id_side
    df_add = df1_data_r_cm[['id', 'id_side', 'elon', 'elat', 'cm_lon', 'cm_lat']]
    df_end = df_end.append(df_add)
print(df_end)

# 根据'id', 'id_side', 'cm_lon', 'cm_lat'字段进行分组
groups = df_end.groupby(['id', 'id_side', 'cm_lon', 'cm_lat'])
# 对每个分组进行遍历并计算回转半径
results = []
for name, group in groups:
    id = name[0] # 增加一列id
    idside = name[1]
    i_lon = group['elon'].values
    i_lat = group['elat'].values
    cm_lon = name[2]
    cm_lat = name[3]
    turning_radius = r_g(idside, i_lon, i_lat, cm_lon, cm_lat)
    results.append({'id': id, 'id_side': idside, 'turning_radius': turning_radius})

# 将结果输出到CSV文件
result_df = pd.DataFrame(results)
result_df.to_csv('result4.csv', index=False)