from sklearn.cluster import KMeans


def k_means(clusters_nm, vector):
    kmeans = KMeans(n_clusters=clusters_nm)
    kmeans.fit(vector)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    clusters_km = {i: [] for i in range(clusters_nm)}
    for i, label in enumerate(labels):
        clusters_km[label].append(i)
    return clusters_km, centroids

