# Sam Gass
# scg0040
# Computational Biology
# Project 3
# python3 coded in Microsoft Visual Studio Code
# Last Modified: March 11, 2020
#
# This python code uses guassian naive bayes to predict secondary structures of proteins


from math import sqrt
from math import pi
from math import exp
from os import listdir
from random import shuffle
from pickle import Pickler

#   The path to the directory with all the ss files.
ssPath = "C:\\Users\\bamas\\Documents\\2020 Spring Semester\\Computational Biology\\Project 3\\ss"

#   This object represents the feature matrix for each protein given.
#   It has the name, the protein sequence as a tuple, the secondary structure, as
#   a tuple, the feature matrix as a tuple of tuples, and the mean and std deviation
#   for each column.


class Matrix:
    def __init__(self, name):
        self.name = name
        self.fasta = self.fillFasta(self.name)
        self.ss = self.fillSS(self.name)
        self.features = self.fillFeatures(self.name)

    #   access the given filename and returns a tuple for the protein sequence.
    def fillFasta(self, filename):
        path = '.\\fasta\\' + filename + '.fasta'
        seqList = []
        fastaFile = open(path, 'r')
        for line in fastaFile:
            for c in line:
                if c == '>':
                    break
                if c == '\n':
                    continue
                seqList.append(c)
        fastaFile.close()
        return tuple(seqList)

    #   Access the given filename and returns a tuple for the secordary sturcture.
    #   H = 0, E = 1, C = 2
    def fillSS(self, filename):
        path = '.\\ss\\' + filename + '.ss'
        seqList = []
        ssFile = open(path, 'r')
        for line in ssFile:
            for c in line:
                if c == '>':
                    break
                if c == '\n':
                    continue
                if c == 'H':
                    seqList.append(0)
                elif c == 'E':
                    seqList.append(1)
                elif c == 'C':
                    seqList.append(2)
                else:
                    print("ss unrecognized character")
                    continue
        ssFile.close()
        return tuple(seqList)

    #   Accesses the filename and returns a tuple of tuple of the features.
    def fillFeatures(self, filename):
        path = '.\\pssm\\' + filename + '.pssm'
        features = []
        pssmFile = open(path, 'r')
        lines = pssmFile.readlines()
        for i in range(3):
            lines.pop(0)
        for i in range(6):
            lines.pop(-1)
        for i in range(len(lines)):
            lines[i] = lines[i].split()

        empty = [-1] * 20
        for i in range(len(lines)):
            row = []
            if i - 2 < 0:
                row += empty
            else:
                for j in range(2, 22):
                    row.append(int(lines[i-2][j]))
            if i - 1 < 0:
                row += empty
            else:
                for j in range(2, 22):
                    row.append(int(lines[i-1][j]))
            for j in range(2, 22):
                row.append(int(lines[i][j]))
            if i + 1 >= len(lines):
                row += empty
            else:
                for j in range(2, 22):
                    row.append(int(lines[i+1][j]))
            if i + 2 >= len(lines):
                row += empty
            else:
                for j in range(2, 22):
                    row.append(int(lines[i+2][j]))
            features.append(tuple(row))
        return tuple(features)

#   creates a feature matrix for all files in the directory specified at ssPath and
#   returns a list of all the objects created


def getData(path):
    filenames = listdir(ssPath)
    data = []
    for name in filenames:
        name = name[0:-3]
        m = Matrix(name)
        data.append(m)
    return data


def splitData(data, percent):
    shuffle(data)
    data1 = list(data)
    data2 = []
    length = percent * len(data1)
    while length > 0:
        data2.append(data1.pop())
        length -= 1
    return data1, data2


def CalculateClassPrior(data):
    prob = {0: 0.0, 1: 0.0, 2: 0.0}
    for k in range(0, 3):
        prob[k] = _yk(data, k)
    return prob


def CalculateAttributeMean(data):
    means = {0: [], 1: [], 2: []}
    for k in range(0, 3):
        for i in range(0, 100):
            means[k].append(_uik(i, k, data))
    return means


def CalculateAttributeVariance(data, means):
    stdv = {0: [], 1: [], 2: []}
    for k in range(0, 3):
        for i in range(0, 100):
            stdv[k].append(_sigma2ik(i, k, means[k][i], data))
    return stdv


def _yk(data, k):
    count = 0
    total = 0
    for d in data:
        for j in range(len(d.features)):
            total += 1
            if d.ss[j] == k:
                count += 1
    return (count / total)


def _uik(i, k, data):
    sum = 0
    count = 0
    for d in data:
        for j in range(len(d.features)):
            if d.ss[j] == k:
                sum += d.features[j][i]
                count += 1
    return (sum / count)


def _sigma2ik(i, k, u, data):
    sum = 0
    count = 0
    for d in data:
        for j in range(len(d.features)):
            if d.ss[j] == k:
                sum += (d.features[j][i] - u)**2
                count += 1
    return (sum / count)


def gaussian(x, u, s):
    c = sqrt(2 * pi * s)
    c = 1/c
    e = exp(-((x - u)**2 / (2 * s)))
    return (c * e)


def pickleModel(modelname, y, m, s):
    with open(modelname, "wb") as f:
        p = Pickler(f)
        p.dump(y)
        p.dump(m)
        p.dump(s)


def testModel(data, y, m, s):
    correct = 0
    incorrect = 0
    total = 0
    for d in data:
        for j in range(len(d.features)):
            argMax = [0, 0, 0]
            pick = -1
            for k in range(0, 3):
                product = 1
                for i in range(100):
                    product *= gaussian(d.features[j][i], m[k][i], s[k][i])
                argMax[k] = (y[k] * product)
            pick = argMax.index(max(argMax))
            if (pick == d.ss[j]):
                correct += 1
            else:
                incorrect += 1
            total += 1
    accuracy = (correct / total)

    print("Model Complete")
    print("______________________________")
    print("Correct:  " + str(correct))
    print("Incorrect:  " + str(incorrect))
    print("Total:  " + str(total))
    print("______________________________")
    print("Model Accuracy:  " + str(accuracy))


if __name__ == "__main__":

    dataSet = getData(ssPath)
    percent = 0.25
    trainingData, testingData = splitData(dataSet, percent)

    priors = CalculateClassPrior(trainingData)
    means = CalculateAttributeMean(trainingData)
    variances = CalculateAttributeVariance(trainingData, means)

    modelname = "SSmodel.pkl"
    pickleModel(modelname, priors, means, variances)

    testModel(testingData, priors, means, variances)
