from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import fcluster, linkage, dendrogram


def hierarchial_cluster(clusters_kmean, center, threshold):
    linkage_matrix = linkage(center, method='ward')
    cluster_hierarchy = fcluster(linkage_matrix, threshold, criterion='distance')
    dendrogram(linkage_matrix)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Data Points')
    plt.ylabel('Distance')
    plt.show()

    positions = {label: [] for label in set(cluster_hierarchy)}
    for i, label in enumerate(cluster_hierarchy):
        positions[label].append(i)

    cluster_positions = {i: [] for i in set(cluster_hierarchy)}
    for idx, cluster_id in enumerate(cluster_hierarchy):
        for i in positions[cluster_id]:
            cluster_positions[cluster_id] += (clusters_kmean[i])
            cluster_positions[cluster_id] = list(set(cluster_positions[cluster_id]))
    print(cluster_positions)
    return cluster_positions