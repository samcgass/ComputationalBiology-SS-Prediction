import sys


def fileToList(filename):
    seqList = []    # list of char in file

    # open file and check for file not found
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        return "file not found"

    # skip first line, otherwise add all char to list except newline char
    for line in f:
        for c in line:
            if c == '>':
                break
            if c == '\n':
                continue
            seqList.append(c)
    f.close()  # close file

    return seqList


if __name__ == "__main__":
    expected = fileToList(sys.argv[1])
    actual = fileToList(sys.argv[2])
    if (len(expected) != len(actual)):
        print("different lengths!")
    else:
        correct = 0
        incorrect = 0
        accuracy = 0
        total = 0
        for i in range(len(expected)):
            total += 1
            if (expected[i] == actual[i]):
                correct += 1
                print(expected[i] + " - " + actual[i])
            else:
                incorrect += 1
                print(expected[i] + " * " + actual[i])
        accuracy = correct / total
        print("______________________________")
        print("Correct:  " + str(correct))
        print("Incorrect:  " + str(incorrect))
        print("Total:  " + str(total))
        print("______________________________")
        print("Percent correct for " +
              sys.argv[1] + ":  " + str(round(accuracy * 100, 2)) + '%')
