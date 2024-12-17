import numpy as np
from numpy.linalg import norm

from get_vecto import get_embed_all_word, get_embed_average
from hierarchial import hierarchial_cluster
from kmean import k_means
from read_data import read_verb, write_clusters
from shihoutte import kmeans_cluster_best, hierarchy_cluster_best


def main():
    word, word_sentence = read_verb('./get_verb_dp_3_1.txt')
    vectors = get_embed_all_word(word)
    # cluster_k = kmeans_cluster_best(vectors)
    # clusters, centers = k_means(7, vectors)
    # # best_cut = hierarchy_cluster_best(centers)
    # # hierrar_cluster = hierarchial_cluster(cluster, centers, best_cut)
    # write_clusters('./data/event', clusters, word)

    # EVENT
    class_name = {'I_ACTION': ['thử', 'gợi ý', 'hoãn', 'cố gắng', 'điều tra', 'xem xét', 'tránh', 'hủy bỏ', 'ra lệnh', 'yêu cầu', 'hứa', 'thề', 'bổ nhiệm'],
                  'REPORTING': ['nói', 'báo cáo', 'giải thích', 'phát biểu', 'kể'],
                  'PERCEPTION': ['nhìn thấy', 'xem', 'nghe', 'nghe trộm', 'chiêm ngưỡng'],
                  'ASPECTUAL': ['bắt đầu', 'cài đặt', 'khởi động', 'bắt tay vào', 'dừng', 'kết thúc', 'tiếp tục'],
                  'I_STATE': ['hy vọng', 'cảm thấy', 'nghĩ', 'muốn', 'thích', 'sợ', 'ghét', 'cần', 'háo hức', 'có thể'],
                  'STATE': ['sống', 'chết', 'chuyển đổi', 'phát triển', 'đi', 'đứng'],
                  'OCCURRENCE': ['tới', 'mượn', 'phân bố', 'có', 'đạt được', 'bùng nổ', 'tăng']}

    # class_name = {'I_ACTION': ['thử', 'đầu_tư', 'hoãn'],
    #               'REPORTING': ['nói', 'báo_cáo', 'giải_thích'],
    #               'PERCEPTION': ['nhìn_thấy', 'xem', 'nghe'],
    #               'ASPECTUAL': ['bắt_đầu', 'cài_đặt', 'khởi_động'],
    #               'I_STATE': ['hy_vọng', 'cảm_thấy', 'chuẩn_bị'],
    #               'STATE': ['sống', 'chết'],
    #               'OCCURRENCE': ['tới', 'mượn', 'phân_bố', 'có']}

    word_value = list(class_name.values())
    word_cluster = get_embed_average(word_value)
    result = {'I_ACTION': [], 'REPORTING': [], 'PERCEPTION': [],
              'ASPECTUAL': [], 'I_STATE': [], 'STATE': [], 'OCCURRENCE': []}
    for i in range(len(word)):
        cosin_similar = np.dot(word_cluster, vectors[i]) / ((norm(word_cluster, axis=1)) * norm(vectors[i]))
        sorted_indices = np.argsort(cosin_similar)[::-1][:1]
        # print(cosin_similar)
        # print(cosin_similar[sorted_indices[0]])
        key_class = list(class_name.keys())[sorted_indices[0]]
        if cosin_similar[sorted_indices[0]] < 0.5:
            key_class = 'OCCURRENCE'
        # for cluster, idx in clusters.items():
        #     if idx:
        result[key_class].append(word[i].strip())

    print(result)

    with open('event_dp.txt', 'w', encoding='utf-8') as file:
        for line in word_sentence:
            file.writelines(','.join(line) + '\n')

    with open('event_dp_word.txt', 'w', encoding='utf-8') as file:
        for line in word:
            file.writelines(line + '\n')

    with open('event_dp_cluster.txt', 'w', encoding='utf-8') as file:
        file.writelines(str(result) + '\n')


if __name__ == '__main__':
    main()
