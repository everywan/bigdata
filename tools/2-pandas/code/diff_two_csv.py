#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, getopt
import pandas as pd
from typing import List

'''
cmd 示例: python diff_two_csv.py -s result.csv --df1=df1.csv --df2=df2.csv

该代码实现如下功能
1. 从命令行参数读取配置, 
2. 从csv中读取数据, 创建 df.
'''

def data_clearing(df):
    '清洗数据, 将 keys 重复的行删除'
    df.drop_duplicates(['date', 'name'], inplace=True)
    return df

def diff_two_df(df1, df2):
    'merge然后filter'
    df = df1.merge(df2, on=['date', 'name'], how='outer', suffixes=('_d1', '_d2'))
    df = df[df.score_d1!=df.score_d2]
    return df

def output(df, save_path):
    df = df.sort_values(['date','merchant_id'])
    df = df[['date','name','score_d1','score_d2',]]
    if (save_path==None) | (len(save_path) == 0):
        print('共有%d条数据存在差异'%(df.shape[0]))
        print(df.head())
    else:
        df.to_csv(save_path, index=False)

def do(df1_path, df2_path, save_path):
    df1 = pd.read_csv(df1_path)
    df2 = pd.read_csv(df2_path).rename(columns={'Name':'name'})
    df1 = data_clearing(df1)
    df2 = data_clearing(df2)
    df1['source'] = 1
    df2['source'] = 2
    df = diff_two_df(df1, df2)
    output(df, save_path)

if __name__=="__main__":
    arg = getopt.getopt(sys.argv[1:],'s:',['df1=', 'df2='])
    df1_path = ''
    df2_path = ''
    save_path = ''
    for k,v in arg[0]:
        if k == '--df1':
            df1_path = v
        if k == '--df2':
            df2_path = v
        if k == '-s':
            save_path = v
    do(df1_path, df2_path, save_path) 
