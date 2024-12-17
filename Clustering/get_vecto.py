import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained('keepitreal/vietnamese-sbert')
model = AutoModel.from_pretrained('keepitreal/vietnamese-sbert')


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def get_embeding(word):
    # print(word)
    encoded_input = tokenizer(word.strip(), padding=True, truncation=True, return_tensors='pt')

    with torch.no_grad():
        model_output = model(**encoded_input)

    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    return list(sentence_embeddings[0])


def get_embed_all_word(word):
    embeding = []
    for w in word:
        if w.strip():
            embeding.append(get_embeding(w))
    return embeding


def get_embed_average(word):
    embeding = []
    for w in word:
        emb = []
        for wd in w:
            if wd.strip():
                emb.append(get_embeding(wd))
        embeding.append(np.average(np.asarray(emb), axis=0))
    return embeding
