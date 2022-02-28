import numpy as np
from tqdm import tqdm

def auto_labeling(data_list, timestamp_list, w):
    labels = np.zeros(len(data_list))
    FP = data_list[0]
    x_H = data_list[0]
    HT = timestamp_list[0]
    x_L = data_list[0]
    LT = timestamp_list[0]
    Cid = 0
    FP_N = 0
    for i in range(len(data_list)):
        if data_list[i] > FP + data_list[0] * w:
            x_H = data_list[i]
            HT = timestamp_list[i]
            FP_N = i
            Cid = 1
            break
        if data_list[i] < FP - data_list[0] * w:
            x_L = data_list[i]
            LT = timestamp_list[i]
            FP_N = i
            Cid = -1
            break
    for i in tqdm(range(FP_N, len(data_list))):
        if Cid > 0:
            if data_list[i] > x_H:
                x_H = data_list[i]
                HT = timestamp_list[i]
            if data_list[i] < x_H - x_H * w and LT < HT:
                for j in range(len(data_list)):
                    if timestamp_list[j] > LT and timestamp_list[j] <= HT:
                        labels[j] = 1
                x_L = data_list[i]
                LT = timestamp_list[i]
                Cid = -1
        if Cid < 0:
            if data_list[i] < x_L:
                x_L = data_list[i]
                LT = timestamp_list[i]
            if data_list[i] > x_L + x_L * w and HT <= LT:
                for j in range(len(data_list)):
                    if timestamp_list[j] > HT and timestamp_list[j] <= LT:
                        labels[j] = -1
                x_H = data_list[i]
                HT = timestamp_list[i]
                Cid = 1
    # Post-processing
    labels[0] = labels[1]
    labels = np.where(labels == 0, Cid, labels)
    assert len(labels) == len(timestamp_list)
    timestamp2label_dict = {timestamp_list[i]: labels[i] for i in range(len(timestamp_list))}
    return labels, timestamp2label_dict