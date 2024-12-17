from vncorenlp import VnCoreNLP

vncorenlp = VnCoreNLP("VnCoreNLP/VnCoreNLP-1.2.jar", )


def tokenize_sentence(text):
    sentences = vncorenlp.tokenize(text)
    data = []
    for sentence in sentences:
        data.append(" ".join(sentence))
    print(sentences)
    return data[0]

print(tokenize_sentence("Nhà Tống bại vong"))