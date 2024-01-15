"""
import numpy as np

c1 = np.array([1, 5, -3, 2])
c2 = np.array([8, 2, 4, 7])

result = c1 + c2

result_list = result.tolist()
print(result_list)

"""
import numpy as np

# Given vectors a (as a row vector) and b^T (as a column vector)
a = np.array([[1, 5, -3, 2]])  # This is a 2D array representing a row vector
b_transpose = np.array([[8], [2], [4], [7]])  # This is a 2D array representing a column vector

# Since we're adding two vectors, they need to be in the same orientation.
# We'll transpose 'a' to a column vector and then add it to 'b_transpose'.
a_transpose = a.T  # Transpose 'a' to a column vector

# Perform the vector addition
result = a_transpose + b_transpose

# Convert the result to a Python list
result_list = result.flatten().tolist()
print(result_list)