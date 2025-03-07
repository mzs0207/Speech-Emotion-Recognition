import os
import csv
import sys

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

from codes.model.Config import Config

'''
get_feature_opensmile(): 
    Opensmile 提取一个音频的特征

输入:
    file_path: 音频路径

输出：
    该音频的特征向量
'''


def get_feature_opensmile(filepath: str):
    # Opensmile 命令
    file_name = str(filepath).split('.')[0]
    output_file = "{0}_output.wav".format(file_name)
    convert_cmd = "ffmpeg -i {0} -acodec pcm_s16le -ac 1 -ar 16000 {1}".format(
        Config.TEST_DATA_PATH + filepath,
        Config.TEST_DATA_PATH + output_file
    )
    csv_file_path = Config.FEATURE_PATH + '{0}.csv'.format(file_name)
    print("convert cmd:{0}".format(convert_cmd))
    os.system(convert_cmd)
    cmd = 'cd ' + Config.OPENSMILE_PATH + ' && ./SMILExtract -C config/' + Config.CONFIG + '.conf -I ' +Config.TEST_DATA_PATH + output_file + ' -O ' +  csv_file_path
    print("Opensmile cmd: ", cmd)
    os.system(cmd)

    reader = csv.reader(open(csv_file_path, 'r'))
    rows = [row for row in reader]
    last_line = rows[-1]
    os.remove(csv_file_path)
    return last_line[1: Config.FEATURE_NUM[Config.CONFIG] + 1]


'''
load_feature():
    从 csv 加载特征数据

输入:
    feature_path: 特征文件路径
    train: 是否为训练数据

输出:
    训练数据、测试数据和对应的标签
'''


def load_feature(feature_path: str, train: bool):
    # 加载特征数据
    df = pd.read_csv(feature_path)
    features = [str(i) for i in range(1, Config.FEATURE_NUM[Config.CONFIG] + 1)]

    X = df.loc[:, features].values
    Y = df.loc[:, 'label'].values

    if train == True:
        # 标准化数据 
        scaler = StandardScaler().fit(X)
        # 保存标准化模型
        joblib.dump(scaler, Config.MODEL_PATH + 'SCALER_OPENSMILE.m')
        X = scaler.transform(X)

        # 划分训练集和测试集
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        return x_train, x_test, y_train, y_test
    else:
        # 标准化数据
        # 加载标准化模型
        scaler = joblib.load(Config.MODEL_PATH + 'SCALER_OPENSMILE.m')
        X = scaler.transform(X)
        return X


'''
get_data(): 
    提取所有音频的特征: 遍历所有文件夹, 读取每个文件夹中的音频, 提取每个音频的特征，把所有特征保存在 feature_path 中

输入:
    data_path: 数据集文件夹路径
    feature_path: 保存特征的路径
    train: 是否为训练数据

输出:
    train = True:
        训练数据、测试数据特征和对应的标签
    train = False:
        预测数据特征
'''


# Opensmile 提取特征
def get_data(data_path: str, feature_path: str, train: bool, delete=False):
    writer = csv.writer(open(feature_path, 'w'))
    first_row = ['label']
    for i in range(1, Config.FEATURE_NUM[Config.CONFIG] + 1):
        first_row.append(str(i))
    writer.writerow(first_row)

    writer = csv.writer(open(feature_path, 'a+'))
    print('Opensmile extracting...')

    if train == True:
        cur_dir = os.getcwd()
        sys.stderr.write('Curdir: %s\n' % cur_dir)
        os.chdir(data_path)
        # 遍历文件夹
        for i, directory in enumerate(Config.CLASS_LABELS):
            sys.stderr.write("Started reading folder %s\n" % directory)
            os.chdir(directory)

            # label_name = directory
            label = Config.CLASS_LABELS.index(directory)

            # 读取该文件夹下的音频
            for filename in os.listdir('.'):
                if not filename.endswith('wav'):
                    continue
                filepath = os.getcwd() + '/' + filename

                # 提取该音频的特征
                feature_vector = get_feature_opensmile(filepath)
                feature_vector.insert(0, label)
                # 把每个音频的特征整理到一个 csv 文件中
                writer.writerow(feature_vector)

            sys.stderr.write("Ended reading folder %s\n" % directory)
            os.chdir('..')
        os.chdir(cur_dir)

    else:
        feature_vector = get_feature_opensmile(data_path)
        feature_vector.insert(0, '-1')
        writer.writerow(feature_vector)
        if delete:
            os.remove(Config.TEST_DATA_PATH+data_path)
            os.remove("{0}{1}_output.wav".format(Config.TEST_DATA_PATH,data_path.split('.')[0]))

    print('Opensmile extract done.')

    # 一个玄学 bug 的暂时性解决方案
    # 这里无法直接加载除了 IS10_paraling 以外的其他特征集的预测数据特征，非常玄学
    if (train == True):
        return load_feature(feature_path, train=train)
