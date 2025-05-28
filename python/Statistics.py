import python.numpy as numpy

# mean,median,mode

speed = [99,86,87,88,111,86,103,87,94,78,77,85,86]

# Use the NumPy mean() method to find the average speed:
x = numpy.mean(speed)

# Use the NumPy median() method to find the middle value:
# x = numpy.median(speed)

# Use the SciPy mode() method to find the number that appears the most:

# from scipy import stats

# speed = [99,86,87,88,111,86,103,87,94,78,77,85,86]

# x = stats.mode(speed)



print(x)