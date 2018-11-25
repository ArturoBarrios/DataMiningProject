#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
=========================================================
The Iris Dataset
=========================================================
This data sets consists of 3 different types of irises'
(Setosa, Versicolour, and Virginica) petal and sepal
length, stored in a 150x4 numpy.ndarray

The rows being the samples and the columns being:
Sepal Length, Sepal Width, Petal Length and Petal Width.

The below plot uses the first two features.
See `here <https://en.wikipedia.org/wiki/Iris_flower_data_set>`_ for more
information on this dataset.
"""
print(__doc__)


# Code source: Gaël Varoquaux
# Modified for documentation by Jaques Grobler
# License: BSD 3 clause

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets
from sklearn.decomposition import PCA
import loader


x_labels = []
f = open("t_xlabels.txt","r")
line = f.read()
for label in line.split(","):
    x_labels.append(label[1:len(label)-1])
# x_labels = {"SepalLengthCm","SepalWidthCm","PetalLengthCm","PetalWidthCm"}
X, y, type2id = loader.load_data('Iris_t.csv', y_label="Species", x_labels=x_labels)

summation_X = []
summation_Y = []
for vector in X:
    index = 1
    result = 0
    for v in vector:
        if(v>0):
            result+=(index*v)

    index+=1
    summation_X.append(result)

print(summation_X)
print(len(X[0]))

#for i in y:
    #for j in X[i]:
        #print i," ",j
    #print(X[:,i])
# for x in y:
#     print "y: ",x
#     print "x: ", X[:,x]
# import some data to play with
# iris = datasets.load_iris()
# X = iris.data[:, :3]  # we only take the first two features.
# y = iris.target

x_min, x_max = min(summation_X) , max(summation_X)
y_min, y_max = y.min(), y.max()
for i in y:
    summation_Y.append((y_min+y_max)/2)
plt.figure(2, figsize=(8, 6))
plt.clf()
print(len(summation_X)," ",len(y))
#Plot the training points
plt.scatter(summation_X,summation_Y, c=y, cmap=plt.cm.Set1,
            edgecolor='k')
print("max: ",x_max)
print("min: ",x_min)

plt.xlabel('Uncommon Word Count')
plt.ylabel(' ')

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())

# To getter a better understanding of interaction of the dimensions
# plot the first three PCA dimensions
fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
components = len(X[0])
print(components)
X_reduced = PCA(n_components=119).fit_transform(X)
ax.scatter(summation_X,0, c=y,
           cmap=plt.cm.Set1, edgecolor='k',s=40)
ax.set_title("First three PCA directions")
ax.set_xlabel("1st eigenvector")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("2nd eigenvector")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("3rd eigenvector")
ax.w_zaxis.set_ticklabels([])

plt.show()
