# -*- coding = utf-8 -*-
# @Time : 2022/4/2 1:11
# @Author : 华定
# @File : challenge_2.py
# @Software: PyCharm
import pandas as pd
import numpy as np
import os


filePath = 'C:\编程+数据分析\data pain pals\challenge2'
filename=os.listdir(filePath)
print(filename)

#读取三个excel文件，合并到一起
df1=pd.read_excel(r'C:\编程+数据分析\data pain pals\challenge2/fasdfrewrweeaesrdawee.xlsx')
df2=pd.read_excel(r'C:\编程+数据分析\data pain pals\challenge2/fasdfsdffgbdsgdfsgesrtewraqre.xlsx')
# df2=df2.drop(index=0)
df3=pd.read_excel(r'C:\编程+数据分析\data pain pals\challenge2/fsdafdsagdrfgartretwrttfsdagafdgfsgdsa.xlsx')
# df3=df3.drop(index=0)
df=pd.concat([df1,df2,df3])
df=df.reset_index()
df=df.drop(columns='index')

#把million和billion单位统一
df.loc[df['Scale']=='Millions',1980:2026]*=1000000
df.loc[df['Scale']=='Billions',1980:2026]*=1000000000
df=df.drop(columns="Scale")


#对四个变量rgdp,ngdp,population,employment分别进行宽转长转换
df_rgdp=df[df["Subject Descriptor"]=="rgdp"]
df_rgdp.drop(columns='Subject Descriptor',inplace=True)
df_rgdp1=df_rgdp.melt(id_vars="Country",var_name="Year",value_name="rgdp")

df_ngdp=df[df["Subject Descriptor"]=="ngdp"]
df_ngdp.drop(columns='Subject Descriptor',inplace=True)
df_ngdp1=df_ngdp.melt(id_vars="Country",var_name="Year",value_name="ngdp")

df_employment=df[df["Subject Descriptor"]=="employment"]
df_employment.drop(columns='Subject Descriptor',inplace=True)
df_employment1=df_employment.melt(id_vars="Country",var_name="Year",value_name="employment")

df_population=df[df["Subject Descriptor"]=="population"]
df_population.drop(columns='Subject Descriptor',inplace=True)
df_population1=df_population.melt(id_vars="Country",var_name="Year",value_name="population")

#把上面四个子表合并到一起
df_f=df_ngdp1.merge(df_rgdp1,on=["Country",'Year'],how="inner").merge(df_employment1,on=["Country",'Year'],how="inner").merge(df_population1,on=["Country",'Year'],how="inner")
df_f.sort_values(by=['Country','Year'],inplace=True)
# df_z=pd.merge(df_rgdp1,df_ngdp1,df_employment1,df_population1,on=["Country",'Year'],how="inner") 为啥这样merge不行？

#新建通胀率、就业率和通胀率哑变量，一共三列
df_f["gdp_deplator"]=df_f["ngdp"]/df_f["rgdp"]
df_f["employment_rate"]=df_f["employment"]/df_f["population"]*100
df_f["deflator_larger_than_1"]=df_f["gdp_deplator"].apply(lambda x: "Yes" if x>=1 else 'No')
df_f[['rgdp','ngdp','employment','population']].round() #一直显示小数点后四个0？

#把日期转为当年最后一天
df_f['Year']=df_f['Year'].astype('str')  #？？我看了一下本来Year这一列之前已经是字符串格式，但是还得重新转一次，不然日期都变为1970
df_f['Year']=pd.to_datetime(df_f['Year'],format='%Y-%m-%d')+ pd.offsets.YearEnd()




'''
之前的尝试记录，先不删了吧
df_t=df.T
df_t.set_axis(df_t.iloc[0],axis=1,inplace=True)
df_t.drop(index='Country',inplace=True)
df_m=df_t.melt(value_name='rgdp')
# id_vars=['Year','rgdp','ngdp','employment','population']
df1=df.melt(id_vars='Country')
# ,var_name='year',value_name='rgdp'
'''


# mydata1=mydata.melt(
# id_vars=["Name","Conpany"],   #要保留的主字段
# var_name="Year",                     #拉长的分类变量
# value_name="Sale"                  #拉长的度量值名称
#         )
