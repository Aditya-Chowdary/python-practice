import numpy as np

# array
arr = np.array([1, 2, 3])
print("array:", arr)

# arange
arr = np.arange(0, 10, 2)
print("arange:", arr)

# zeros
arr = np.zeros((2, 3))
print("zeros:\n", arr)

# ones
arr = np.ones((2, 3))
print("ones:\n", arr)

# empty
arr = np.empty((2, 3))
print("empty:\n", arr)

# eye
arr = np.eye(3)
print("eye:\n", arr)

# linspace
arr = np.linspace(0, 1, 5)
print("linspace:", arr)

# logspace
arr = np.logspace(0.1, 2, 5)
print("logspace:", arr)

# reshape
arr = np.arange(6).reshape(2, 3)
print("reshape:\n", arr)

# ravel
arr = np.array([[1,2],[3,4]]).ravel()
print("ravel:", arr)

# transpose
arr = np.array([[1,2],[3,4]]).transpose()
print("transpose:\n", arr)

# concatenate
arr = np.concatenate((np.array([1,2]), np.array([3,4])))
print("concatenate:", arr)

# stack
arr = np.stack((np.array([1,2]), np.array([3,4])))
print("stack:\n", arr)

# hstack
arr = np.hstack((np.array([1,2]), np.array([3,4])))
print("hstack:", arr)

# vstack
arr = np.vstack((np.array([1,2]), np.array([3,4])))
print("vstack:\n", arr)

# split
arr = np.split(np.array([0,1,2,3,4,5]), 3)
print("split:", arr)

# hsplit
arr = np.hsplit(np.array([[1,2,3],[4,5,6]]), 3)
print("hsplit:", arr)

# vsplit
arr = np.vsplit(np.array([[1,2,3],[4,5,6]]), 2)
print("vsplit:", arr)

# mean
result = np.mean([1, 2, 3])
print("mean:", result)

# median
result = np.median([1, 2, 3])
print("median:", result)

# std
result = np.std([1, 2, 3])
print("std:", result)

# var
result = np.var([1, 2, 3])
print("var:", result)

# sum
result = np.sum([1, 2, 3])
print("sum:", result)

# prod
result = np.prod([1, 2, 3])
print("prod:", result)

# min
result = np.min([1, 2, 3])
print("min:", result)

# max
result = np.max([1, 2, 3])
print("max:", result)

# argmin
result = np.argmin([1, 2, 3])
print("argmin:", result)

# argmax
result = np.argmax([1, 2, 3])
print("argmax:", result)

# dot
result = np.dot([1, 2], [3, 4])
print("dot:", result)

# matmul
result = np.matmul([[1, 2]], [[3], [4]])
print("matmul:\n", result)

# linalg.inv
try:
    result = np.linalg.inv(np.array([[1, 2], [3, 4]]))
    print("linalg.inv:\n", result)
except np.linalg.LinAlgError as e:
    print("linalg.inv: Error -", e)

# linalg.det
result = np.linalg.det(np.array([[1, 2], [3, 4]]))
print("linalg.det:", result)

# linalg.eig
vals, vecs = np.linalg.eig(np.array([[1, 2], [2, 1]]))
print("linalg.eig values:", vals)
print("linalg.eig vectors:\n", vecs)

# linalg.svd
U, S, V = np.linalg.svd(np.array([[1, 2], [3, 4]]))
print("linalg.svd U:\n", U)
print("linalg.svd S:", S)
print("linalg.svd V:\n", V)

# random.rand
arr = np.random.rand(2, 3)
print("random.rand:\n", arr)

# random.randn
arr = np.random.randn(2, 3)
print("random.randn:\n", arr)

# random.randint
arr = np.random.randint(0, 10, size=(2, 3))
print("random.randint:\n", arr)

# random.choice
arr = np.random.choice([1, 2, 3], size=2)
print("random.choice:", arr)

# random.seed
np.random.seed(42)
print("random.seed: Set to 42")

# where
arr = np.where(np.array([1, 2, 3]) > 1)
print("where:", arr)

# nonzero
arr = np.nonzero([0, 1, 2, 0])
print("nonzero:", arr)

# clip
arr = np.clip([1, 2, 3, 4], 1, 3)
print("clip:", arr)

# unique
arr = np.unique([1, 1, 2, 2, 3])
print("unique:", arr)

# sort
arr = np.sort([3, 1, 2])
print("sort:", arr)
