# import os

import numpy as np
import openpyxl
import torch
from transformers import AutoModel, AutoTokenizer
from read_dtu_example import read_ver_example, write_verb_example
from token_sentence import tokenize_sentence
from sklearn.metrics.pairwise import cosine_similarity

# Tải mô hình PhoBERT và tokenizer
model_name = "vinai/phobert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


# Tách câu thành các phần văn bản nhỏ (phân đoạn)
def get_vector_by_phoBert(word, text):
    if len(word.split(" ")) > 1:
        text = tokenize_sentence(text)
        word_new = tokenize_sentence(word.strip())
        word_new = word_new.replace(" ", "_")
        if word_new not in text:
            text = text.replace(word, word_new)
        if ("chiếm_giữ_chức" in text or "đảm_nhiệm_chức" in text or "miễn_nhiệm_chức" in text
                or "tái_cử_chức" in text or "ứng_cử_chức" in text or "tranh_cử_chức" in text):
            text = text.replace("_chức", " chức")
        if "đi_tắt_" in text:
            text = text.replace("đi_tắt_", "đi_tắt ")
        if "_điều_hành" in text:
            text = text.replace("_điều_hành", " điều_hành")
        if "_tập_trung" in text:
            text = text.replace("_tập_trung", " tập_trung")
        if "bị_thương_vong" in text:
            text = text.replace("_thương_vong", " thương_vong")
        if "thì thà_thì thụt" in text:
            text = text.replace("thì thà_thì thụt", "thì_thà_thì_thụt")
        if "thì thà_thì_thầm" in text:
            text = text.replace("thì thà_thì_thầm", "thì_thà_thì_thầm")
        if "cho_qua_chuyện" in text:
            text = text.replace("cho_qua_chuyện", "cho_qua chuyện")
        if "lên_cơn_" in text:
            text = text.replace("lên_cơn_", "lên_cơn ")
        if "chị_nuôi báo_cô" in text:
            text = text.replace("chị_nuôi báo_cô", "chị nuôi_báo_cô")
        if "_sáng_chế" in text:
            text = text.replace("_sáng_chế", " sáng_chế")
        if "_sở_hữu" in text:
            text = text.replace("_sở_hữu", " sở_hữu")
        if "xây_dựng_" in text:
            text = text.replace("xây_dựng_", "xây_dựng ")
        if word_new.startswith("_"):
            word_new = word_new[1:]
        word = word_new

    token = tokenizer.encode(text)
    token_word = tokenizer.encode(word)[1]
    # print(tokenized_word)
    word_index = token.index(token_word)
    input_ids = torch.tensor([token])
    with torch.no_grad():
        outputs = model(input_ids)

    word_embedding = outputs.last_hidden_state[:, word_index, :].tolist()
    # print(len(word_embedding[0]))
    return word_embedding[0]


def get_vector(words, example):
    vectors = []
    vectors_str = []
    for i in range(len(words)):
        word = str(words[i]).split("_")[0]
        emb = get_vector_by_phoBert(word, example[i])
        vectors.append(emb)
        vectors_str.append(str(emb))
    return vectors, vectors_str


def cosin_simil(vector_a, vector_b):
    cosine_sim = cosine_similarity(np.array(vector_a).reshape(1, -1), np.array(vector_b).reshape(1, -1))[0][0]
    return cosine_sim


def get_10_max(arr):
    sorted_indices = np.argsort(np.array(arr))[::-1]

    # Chọn 10 phần tử đầu tiên
    top_10_indices = sorted_indices[1:11]
    return top_10_indices


def write_cosin_words(words, vectors, vectors_str, examples, definitions):
    sheet_idx = int(len(words) / 200) + 1
    wb = openpyxl.load_workbook("result_10_max.xlsx")
    #
    for k in range(57, sheet_idx):
        if k == 20 or k == 21:
            continue
        #     cosins = []
        start = (k - 1) * 200
        end = k * 200 if k * 200 < len(words) else len(words)
        sheet_name = "Sheet_" + str(k)
        print(sheet_name)
        #     for i in range(start, end):
        #         cosin_word = []
        #         for j in range(start, end):
        #             if i == j:
        #                 cosin_word.append(1)
        #             else:
        #                 cosin = cosin_simil(vectors[i], vectors[j])
        #                 cosin_word.append(round(cosin, 4))
        #         cosins.append(cosin_word)
        #     write_verb_example("result.xlsx", sheet_name, wb, words[start:end],
        #     examples[start:end], definitions[start:end],
        #                        vectors_str[start:end], cosins)
        #
        cosin_max = []
        for i in range(start, end):

            cosin_word = []
            for j in range(len(words)):
                if i == j:
                    cosin_word.append(1)
                else:
                    cosin = cosin_simil(vectors[i], vectors[j])
                    cosin_word.append(round(cosin, 4))
            top_10_idx = get_10_max(cosin_word)
            cosin_10_max = {}
            for k in top_10_idx:
                cosin_10_max[words[k]] = cosin_word[k]

            cosin_max.append(str(cosin_10_max))
        print(len(cosin_max))
        write_verb_example("result_10_max.xlsx", sheet_name, wb, words[start:end],
                           examples[start:end], definitions[start:end], vectors_str[start:end], cosin_max)


words, examples, definitions = read_ver_example('Verb_Pattern.xlsx')
vector, vector_str = get_vector(words, examples)
write_cosin_words(words, vector, vector_str, examples, definitions)
# wb = openpyxl.Workbook()
# write_verb_example("verb_vn_phoBert.xlsx", "Sheet1", wb, words, examples, definitions, vector_str, [])
