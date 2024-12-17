
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster


def kmeans_cluster_best(X):
    best_k = 0
    best_silhouette = -1

    for k in range(3, len(X)//2, 30):  # Chọn khoảng giá trị k
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        labels = kmeans.labels_
        silhouette_avg = silhouette_score(X, labels)

        if silhouette_avg > best_silhouette:
            best_silhouette = silhouette_avg
            best_k = k

    print(f"Best number of clusters (K-means): {best_k}")
    return best_k


def hierarchy_cluster_best(X):
    linkage_matrix = linkage(X, method='ward')
    dendrogram(linkage_matrix)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Data Points')
    plt.ylabel('Distance')
    plt.show()
    best_silhouette = -1
    best_cut = None
    # 80,
    for height in range(3, len(X)-5):
        labels = fcluster(linkage_matrix, height, criterion='distance')
        # print(labels)
        if 1 < len(list(set(labels))) < len(X):
            silhouette_avg = silhouette_score(X, labels)
            print(silhouette_avg)

            if silhouette_avg > best_silhouette:
                best_silhouette = silhouette_avg
                best_cut = height

    print(f"Best cut height (Hierarchical): {best_cut}")
    return best_cut


