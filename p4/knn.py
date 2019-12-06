import csv
import math
import operator


# loads train file and casts them from String to float
def loadData(file_name):
    with open(file_name, 'r') as csvFile:
        lines = csv.reader(csvFile)
        data_set = list(lines)
        for column in range(len(data_set)):
            for row in range(len(data_set[0])):
                data_set[column][row] = float(data_set[column][row])
    return data_set


def euclideanDistance(instance1, instance2, number_of_columns):
    distance = 0
    for x in range(number_of_columns):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, test_row, k):
    distances = []
    number_of_columns = len(test_row) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(test_row, trainingSet[x], number_of_columns)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for i in range(k):
        neighbors.append(distances[i][0])
    return neighbors


def getResponse(neighbors):
    class_votes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in class_votes:
            class_votes[response] += 1
        else:
            class_votes[response] = 1
    sorted_votes = sorted(class_votes.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_votes[0][0]


def getAccuracy(test_set, predictions):
    correct = 0
    for x in range(len(test_set)):
        if test_set[x][-1] == predictions[x]:
            correct += 1
    print("correct: ", correct)
    return (correct / float(len(test_set))) * 100


def main():
    # Prepare data
    train_file = 'train.csv'
    test_file = 'test.csv'
    training_set = loadData(train_file)
    test_set = loadData(test_file)
    print("Train set: ", len(training_set))
    print("Test set: ", len(test_set))
    # Generate Predictions
    predictions = []
    k = 12
    for x in range(len(test_set)):
        neighbors = getNeighbors(training_set, test_set[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        print('Predicted: ' + str(result) + "  >>  ", "Actual: " + str(test_set[x][-1]))
    accuracy = getAccuracy(test_set, predictions)
    print("Accuracy: " + str(accuracy) + "%")


main()
