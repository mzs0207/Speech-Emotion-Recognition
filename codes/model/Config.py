#!/usr/bin/env python
# coding:utf8
"""
参数配置
"""
import os


class Config(object):
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # 数据集路径
    DATA_PATH = project_path+'/Datasets/CASIA/6'
    # 情感标签
    CLASS_LABELS = ("angry", "fear", "happy", "neutral", "sad", "surprise")
    # CLASS_LABELS = ("positive", "negative", "neutral")
    # CLASS_LABELS = ("angry", "boredom", "disgust", "fear", "happy", "neutral", "sad")

    # LSTM 的训练 epoch 数
    epochs = 20

    # Opensmile 标准特征集
    CONFIG = 'IS10_paraling'
    # Opensmile 安装路径
    OPENSMILE_PATH = '/Users/mengzengshan/Downloads/opensmile-2.3.0'
    # 每个特征集的特征数量
    FEATURE_NUM = {
        'IS09_emotion': 384,
        'IS10_paraling': 1582,
        'IS11_speaker_state': 4368,
        'IS12_speaker_trait': 6125,
        'IS13_ComParE': 6373,
        'ComParE_2016': 6373
    }

    # 特征存储路径
    FEATURE_PATH = project_path+'/Features/6-category/'
    # 训练特征存储路径（Opensmile）
    TRAIN_FEATURE_PATH_OPENSMILE = FEATURE_PATH + 'train_opensmile_casia.csv'
    # 预测特征存储路径（Opensmile）
    PREDICT_FEATURE_PATH_OPENSMILE = FEATURE_PATH
    #PREDICT_FEATURE_PATH_OPENSMILE = FEATURE_PATH + 'test_opensmile_casia.csv'

    # 训练特征存储路径（librosa）
    TRAIN_FEATURE_PATH_LIBROSA = FEATURE_PATH + 'train_librosa_casia.p'
    # 预测特征存储路径（librosa）
    PREDICT_FEATURE_PATH_LIBROSA = FEATURE_PATH + 'test_librosa_casia.p'
    # 测试集的存储目录
    TEST_DATA_PATH = project_path + '/Test/'

    # 模型存储路径
    MODEL_PATH = project_path+'/Models/'
