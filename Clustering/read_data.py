import os

import openpyxl
import pandas as pd


def read_verb(filepath):
    # df = pd.read_excel(filepath)
    # word_list = list(df["sub_entry"])
    # # pos_list = list(df["pos"])
    # # print(set(pos_list))
    # # example_list = list(df["example"])
    # # definition_list = list(df["definition"])
    # return list(set(word_list))

    result = []
    result_sentence = []
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.readlines()
        for dt in data:
            line = list(set(dt.split(',')))
            for i in range(len(line)):
                line[i] = line[i].strip()
            result_sentence.append(line)
            result += line
    return list(set(result)), result_sentence



def write_clusters(pathFile, clusters, verbs):
    for cluster, idx in clusters.items():
        filename = os.path.join(pathFile, "cluster" + str(cluster) + ".txt")

        if idx:
            with open(filename, 'w', encoding="utf-8") as file:
                for i in idx:
                    file.write(verbs[i]+"\n")
                file.write("\n")
