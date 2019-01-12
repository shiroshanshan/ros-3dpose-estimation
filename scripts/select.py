import math

def calculate_distance(xy1,xy2):
    return math.sqrt((xy2[0] - xy1[0]) ** 2 + (xy2[1] - xy1[1]) ** 2)

class OpenposeData(object):

    def __init__(self, data):
        self.data = data
        self.number = data.shape[0]

    def partial_distance(self):
        distances = []
        for i in range(self.number):
            xy = [data[i,j,0:2] for j in self.data[i].shape[0]]
            distance = calculate_distance(xy[0],xy[1]) + calculate_distance(xy[1],xy[2]) + calculate_distance(xy[1],xy[5])\
             + calculate_distance(xy[1],xy[11]) + calculate_distance(xy[1],xy[8])
            distances.append(distance)
        return distances

    def ishuman(self, threshold, joint_num):
        return [len([j for j in self.data[i][::2] if j > threshold]) > joint_num for i in range(self.number)]

    def openpose_select(self, threshold=0.5, joint_num=9):
        data = self.data
        number = self.number
        if not number:
            return "error: no people detected"
        else:
            size = self.partial_distance()
            ishuman = self.ishuman(threshold, joint_num)
            if not any(ishuman):
                return "error 1: people detected with low confidence"
            else:
                maximum = max([size[i] for i in range(self.number) if ishuman[i]])
                idx = size.index(maximum)
                print("opselect finish")
                return self.data[idx]
