import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import argparse
from glob import glob
import os
import pdb

parser = argparse.ArgumentParser(description='Split data into test/train')
parser.add_argument('-i', '--input', help='input path to data folder', required=True)
parser.add_argument('-o', '--output', help='output folder path for test/train csvs', required=False, default='./output')
parser.add_argument('-s', '--splitpercent', help='percentage of data to store as test', required=False, default='30')
parser.add_argument('-t', '--threshold', help='scoring threshold', required=False, default=None)
parser.add_argument('-d', '--data', help='list of column names of data to input', nargs='*', required=False, default=None)
parser.add_argument('-p', '--predictingColumn', help='name of column to predict off of', required=True)

def combine(files):
    dataframes = []
    finalData = []
    for file in files:
        df = pd.read_csv(file)
        dataframes.append(df)
    
    finalData = pd.concat(dataframes)

    return finalData

def score(treshold, column, data, name):
    data[name]=np.where(data[column]<treshold,True,False)

def split(data, labelName, percent, output, inputLabels=None):
    y = data[labelName]
    x = data.drop(labelName, axis=1)
    if inputLabels != None:
        x = data[inputLabels]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=percent/float(100), random_state=42, shuffle=True)
    os.mkdir(output)
    x_train.to_csv(os.path.join(output, 'x_train.csv'))
    print(f'x_train.csv saved to {output}!')
    y_train.to_csv(os.path.join(output, 'y_train.csv'))
    print(f'y_train.csv saved to {output}!')
    x_test.to_csv(os.path.join(output, 'x_test.csv'))
    print(f'x_test.csv saved to {output}!')
    y_test.to_csv(os.path.join(output, 'y_test.csv'))
    print(f'y_test.csv saved to {output}!')

if __name__ == '__main__':
    args = parser.parse_args()
    
    path = os.path.join(args.input, '*.csv')
    listOFiles = glob(path)
    
    df1 = combine(listOFiles)
    
    print(df1.columns)

    labelColumn = args.predictingColumn
    if args.threshold != None:
        score(float(args.threshold), labelColumn, df1, 'isFolded')
        print(df1.columns)
        df1 = df1.drop(labelColumn, axis=1)
        labelColumn = 'isFolded'

    if args.data == None:
        split(df1, labelColumn, float(args.splitpercent), args.output)
    else:
        split(df1, labelColumn, float(args.splitpercent), args.output, inputLabels=list(args.data))