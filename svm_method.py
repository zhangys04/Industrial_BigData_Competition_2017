#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# pickle写入方法：
# 1. pickle.dump()
#
# with open('test.txt', 'wb') as f:
#     pickle.dump(sth, f)
#
# 2. pickle.dumps()
#
# s = pickle.dumps(sth)
# with open('test.txt', 'wb') as f:
#     f.write(s)

# 可优化方向：
# 1. 数据归一化处理(done)
# 2. 网格搜索寻找SVM最优参数(C&gamma)
# 3. 绘制roc曲线以评价模型

import pickle
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# batch-训练集；minutes-平均分钟数；elementList-所选特征；norm-是否归一化处理
def SVM_Method(batch, minutes, elementList, norm):
    # 效果较好的特征有：wind_speed与power；pitch%NUM%_angle与power；
    # pitch%NUM%_speed与power；yaw_speed与power；
    # pitch1_ng5_DC，pitch2_ng5_DC，pitch3_ng5_DC与power
    elementList = sorted(elementList)

    data = pd.read_csv('./processed/%s_avg%s_lowPower_data.csv' %(batch, str(minutes)))
    X = data[elementList]
    if norm:
        X_min = X.min()
        X_max = X.max()
        X = (X - X_min) / (X_max - X_min)
    y = data['frozen']

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=5000, random_state=1)

    model = SVC(kernel='rbf', C=1E10)
    model.fit(X_train, y_train)
    ymodel = model.predict(X_test)
    print('验证集准确率：%0.3f\n\n' %accuracy_score(ymodel, y_test))

    if norm:
        with open('models/svm_model_%s_norm+%s.pkl' %(batch, '+'.join(elementList)), 'wb') as f:
            pickle.dump([model, [X_min, X_max]], f)
    else:
        with open('models/svm_model_%s+%s.pkl' %(batch, '+'.join(elementList)), 'wb') as f:
            pickle.dump(model, f)


if __name__ == '__main__':
    SVM_Method(batch=str(15), minutes=1, 
        elementList=['wind_speed', 'pitch1_angle', 'pitch1_speed', 'power'], norm=True)