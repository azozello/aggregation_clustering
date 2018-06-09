import math
import random
import matplotlib.pyplot as plt
import numpy as np


def start(points_count=100, max_width=50.0, clusters_count=5):
    points = generate_sample(points_count, max_width)
    clusters = [[i] for i in range(points_count)]
    distances = np.array([[get_point_distance(points[i], points[j]) for j in range(points_count)]
                          for i in range(points_count)])

    while len(clusters) > clusters_count:
        clusters = average_join(clusters, distances)
        draw_clusters(clusters, points)

    return


def generate_sample(points_count, max_width):
    points = [[random.uniform(0.0, max_width), random.uniform(0.0, max_width)] for i in range(points_count)]
    return np.array(points)


def draw_points_2d(points):
    for point in points:
        plt.plot(point[0], point[1], 'r+')
    plt.show()
    plt.clf()


def draw_clusters(clusters, points):
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    for index in range(len(clusters)):
        for i in clusters[index]:
            if index < 6:
                plt.plot(points[i][0], points[i][1], colors[index] + '+')
            else:
                plt.plot(points[i][0], points[i][1], 'k+')
    plt.show()
    plt.clf()


def get_point_distance(point_1, point_2):
    distance = 0.0
    if len(point_1) == len(point_2):
        for i in range(len(point_2)):
            distance += math.pow(point_1[i] - point_2[i], 2)
    return math.sqrt(distance)


def get_cluster_distance(cluster_1, cluster_2, distances):
    connects_number = len(cluster_1) * len(cluster_2)
    distance = 0.0
    for i in range(len(cluster_1)):
        for j in range(len(cluster_2)):
            distance += distances[cluster_1[i]][cluster_2[j]]
    return distance / connects_number


def average_join(clusters, distances):
    used = []
    new_clusters = []
    for index in range(len(clusters)):
        if not used.__contains__(index):
            lowest_distance = 0.0
            nearest_cluster = 0

            for j in range(len(clusters)):
                if not j == index and not used.__contains__(j):
                    if lowest_distance == 0.0:
                        lowest_distance = get_cluster_distance(clusters[index], clusters[j], distances)
                        nearest_cluster = j
                    else:
                        if get_cluster_distance(clusters[index], clusters[j], distances) < lowest_distance:
                            lowest_distance = get_cluster_distance(clusters[index], clusters[j], distances)
                            nearest_cluster = j

            used += [index, nearest_cluster]
            new_clusters.append(clusters[index] + clusters[nearest_cluster])

    return new_clusters
