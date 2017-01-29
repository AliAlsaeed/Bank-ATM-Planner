import numpy as np
import math
from sklearn.cluster import DBSCAN

def unreachable_cluster(centers, eps, min_sample, distance_function):

    db = DBSCAN(eps=eps, min_samples=min_sample, n_jobs=-1, metric= distance_function).fit(centers)
    labels = db.labels_
    result = []
    for _ in range(0, max(labels) + 1):
        result.append([])

    for i in range(len(labels)):
        if labels[i] != -1:
            result[labels[i]].append(centers[i])

    finalResult = []
    for cluster in result:
        for coordinate in cluster:
            tuple = coordinate.tolist()
            tuple.append(len(cluster))
            finalResult.append(tuple)

    return finalResult

def distance_function(x, y):
    R = 3959 # miles, the radius of the Earth
    lat1, lon1 = x[0], x[1]
    lat2, lon2 = y[0], y[1]
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow((math.sin(dlon / 2)), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

centers = np.loadtxt('part1_result.csv', delimiter=',')
clusters = unreachable_cluster(centers, 100, 3, distance_function)
np.savetxt('part2_result.csv', clusters, delimiter=',')
