import math
import random
import matplotlib.pyplot as plt
import numpy as np

from operator import itemgetter


def start(points_count=100, max_width=50.0, clusters_count=5):
    """

    :param points_count:
    :param max_width:
    :param clusters_count:

    """
    points = generate_sample(points_count, max_width)
    points_distances = np.array([[get_point_distance(points[i], points[j]) for j in range(points_count)]
                                 for i in range(points_count)])
    clusters_numbers = [[i] for i in range(points_count)]

    while len(clusters_numbers) > clusters_count:
        clusters_numbers = average_distance_join(points_distances, clusters_numbers)
        draw_clusters(clusters_numbers, points)
    print()


def average_distance_join(points_distances, clusters_numbers):
    new_clusters_numbers = []
    cluster_distances = np.array([[get_cluster_distance(clusters_numbers[i], clusters_numbers[j], points_distances)
                                   for j in range(len(clusters_numbers))] for i in range(len(clusters_numbers))])
    closest_clusters = get_closest_clusters(cluster_distances)
    used = []
    available = 0
    for i in range(len(clusters_numbers)):
        for j in range(len(clusters_numbers[i])):
            available += 1

    for i in range(len(closest_clusters)):
        can_add = True
        for point in clusters_numbers[int(closest_clusters[i][1])]:
            if used.__contains__(point):
                can_add = False
                break
        for point in clusters_numbers[int(closest_clusters[i][2])]:
            if used.__contains__(point):
                can_add = False
                break

        if can_add:
            new_clusters_numbers.append(clusters_numbers[int(closest_clusters[i][1])] +
                                        clusters_numbers[int(closest_clusters[i][2])])
            for number in clusters_numbers[int(closest_clusters[i][1])] + clusters_numbers[int(closest_clusters[i][2])]:
                if number not in used:
                    used.append(number)

        if len(clusters_numbers) - (len(new_clusters_numbers) * 2) == 1:
            for l in range(len(clusters_numbers)):
                for j in range(len(clusters_numbers[l])):
                    if clusters_numbers[l][j] not in used:
                        new_clusters_numbers.append([clusters_numbers[l][j]])
                        used.append(clusters_numbers[l][j])

        if len(used) == available:
            break

    return new_clusters_numbers


def generate_sample(points_count, max_width):
    return np.array([[random.uniform(0.0, max_width), random.uniform(0.0, max_width)] for i in range(points_count)])


def get_closest_clusters(cluster_distances):
    closest_clusters = []

    for i in range(len(cluster_distances)):
        for j in range(len(cluster_distances[0])):
            if j > i:
                closest_clusters.append([cluster_distances[i][j], i, j])

    return np.array(sorted(closest_clusters, key=itemgetter(0)))


def get_cluster_distance(cluster_1, cluster_2, distances):
    connects_number = len(cluster_1) * len(cluster_2)
    distance = 0.0
    for i in range(len(cluster_1)):
        for j in range(len(cluster_2)):
            distance += distances[cluster_1[i]][cluster_2[j]]
    return distance / connects_number


def get_point_distance(point_1, point_2):
    distance = 0.0
    if len(point_1) == len(point_2):
        for i in range(len(point_2)):
            distance += math.pow(point_1[i] - point_2[i], 2)
    return math.sqrt(distance)


def draw_points_2d(points):
    for point in points:
        plt.plot(point[0], point[1], 'r+')
    plt.show()
    plt.clf()


def draw_clusters(clusters, points, iter=-1):
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    for index in range(len(clusters)):
        for i in clusters[index]:
            if index < 6:
                plt.plot(points[i][0], points[i][1], colors[index] + '+')
            else:
                plt.plot(points[i][0], points[i][1], 'k+')
    plt.show()
    # plt.savefig('files/iter_' + str(iter) + '.png')
    plt.clf()
