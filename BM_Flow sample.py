import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import datetime
from tqdm import tqdm

"此代码职能如下" \
"对应B，M的对应公式计算单个用户的固定时间戳样本" \
"获得B/T,M/T函数"
sample_tamp=24#样本周期(h)
id=10
#输入选用个体样本
#读取数据
file=r'C:\第二篇论文编写程序\M-r关系实验\个体动态BM值实验\data\stay_move.csv'
df=pd.read_csv(file)
outputpath=r'C:\第二篇论文编写程序\M-r关系实验\个体动态BM值实验\data\result.csv'
#样本抽取测试模块
#userid=list(df['id'])
#sample_get=list(set(userid))#提取userid
#count=[]
#for i in range(len(sample_get)):
#    df_s=df[df.id==sample_get[i]]
#    count=[len(df_s)]
#Msample_get=count.index(max(count))

#最终选用样本
df_smple=df[df['id']==id]
df_smple['stime']=pd.to_datetime(df_smple['stime'])
df_smple=df_smple.sort_values(by=['stime'])
time=list(df_smple['stime'])
time_smple=list(set(time))

#时间戳标签间隔抽样
tcel=time[0]
lis_tcel=[time[0]]#存储
while tcel<=time[len(time)-1]:
      tcel=tcel+datetime.timedelta(hours=sample_tamp)#时间+sample_tamp(h)
      lis_tcel+=[tcel]
"BM运算" \
"B=(std(ts)-avg(ts))/(std(ts)+avg(ts))" \
"M=(1/x-1)SUM_x&i=1[(ts[1]-avg[ts[2:x-1]])(ts[2]-avg[ts[2:x])/std[1~x-1]]std[2~x]"
B_LIS=[]
M_LIS=[]
lable=[]
for i in tqdm(range(1,len(lis_tcel))):
    s_date = lis_tcel[0]
    #---to
    e_date = lis_tcel[i]
    df_tsmplpe = df_smple[(df_smple['stime'] >= s_date) & (df_smple['stime'] <= e_date)]
    if len(df_tsmplpe)<2:
        continue
    lable+=[i]
    #提取元素计算时间戳
    t_s=list(df_tsmplpe['stime'])
    t_smple=[]
    for j in range(len(t_s)):
        t_smple+=[(t_s[j]-t_s[j-1]).seconds]
    #BM值计算
    B=(np.std(t_smple)-np.mean(t_smple))/(np.std(t_smple)+np.mean(t_smple))
    B_LIS+=[B]
    n=1/(len(t_smple)-1)
    M_sum=0
    for x in range(1,len(t_smple)-1):
        mode1=(t_smple[x-1]-np.mean(t_smple[0:len(t_smple)-1]))*(t_smple[x]-np.mean(t_smple[0:len(t_smple)]))
        mode2=np.std(t_smple[0:len(t_smple)-1])*np.std(t_smple[0:len(t_smple)])
        M_sum+=mode1/mode2
    M_LIS+=[n*M_sum]
#输出
df_BM=pd.DataFrame({'B':B_LIS,'M':M_LIS,'lable':lable})
df_BM.to_csv(outputpath,sep=',',index=False,header=True)
print(df_BM)
#绘图
plt.subplot(211) # 多张图绘制
plt.plot(lable,B_LIS)
plt.title('Dynamic time sample BM function')
plt.ylabel('B')
plt.subplot(212)
plt.plot(lable,M_LIS)
#plt.text(1,230,'Dynamic time sample',size=10,color='gray',alpha=0.5)
#plt.title('Dynamic time sample',loc='right',fontdict={'size':'small','color':'r','family':'Times New Roman'})
plt.ylabel('M')
plt.xlabel('time label(24h)')
plt.show()