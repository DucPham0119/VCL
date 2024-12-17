import re

import numpy as np
import openpyxl

# 5: word
# 6: pos
# 9: number_sence
# 11: example
#

import pandas as pd


def read_ver_example(filepath):
    words = []
    examples = []
    definitions = []
    df = pd.read_excel(filepath)
    word_list = list(df["sub_entry"])
    pos_list = list(df["pos"])
    example_list = list(df["example"])
    definition_list = list(df["definition"])
    # print(example_list)
    for i in range(len(example_list)):
        if pos_list[i] == 'V' and str(example_list[i]) != "nan" and str(word_list[i]) != "nan":
            ex_i = str(example_list[i]).split("~ ")

            definitions.append(str(definition_list[i]).strip())
            if len(ex_i) == 1:
                words.append(str(word_list[i]).strip())
                examples.append(str(ex_i[0]).strip())

            else:
                for k in range(len(ex_i)):
                    words.append(str(word_list[i]).strip() + "_" + str(k + 1))
                    examples.append(str(ex_i[k]).strip())
                    if k > 0:
                        definitions.append("")
    return words, examples, definitions


def write_verb_example(filepath, sheet_name, wb, words, examples, definitions, vector, cosins):
    # wb = openpyxl.Workbook()
    sheet = wb.create_sheet(title=sheet_name)
    print("======================")
    print(np.array(definitions).shape)
    print(np.array(examples).shape)
    print(np.array(words).shape)
    print(np.array(vector).shape)
    print(np.array(cosins).shape)

    mt = [list(definitions), list(examples), list(words), list(vector), list(cosins)]
    matrix = np.array(mt)
    matrix_t = np.transpose(matrix)
    head = ["definitions", "examples", "words", "vector", "cosin_max"]
    # if cosins != []:
    #     matrix_cosin = np.concatenate((matrix_t, np.array(cosins)), axis=1)
    #     head += words
    # else:
    #     matrix_cosin = matrix_t
    # data = matrix_cosin.tolist()
    data = matrix_t.tolist()
    data.insert(0, head)

    for row in data:
        sheet.append(row)

    # Lưu lại file Excel
    wb.save(filepath)

# words, examples,  definitions= read_ver_example('Verb_Pattern.xlsx')
# write_verb_example('verb_example.xlsx', words, examples, definitions)
