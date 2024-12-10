def prepare_matrices(subset):
    X = [[1, row['mileage'], row['year'], row['engineSize'], row['mpg'], row['tax'],
        row['model'], row['transmission'], row['fuelType']] for _, row in subset.iterrows()]
    Y = [row['price'] for _, row in subset.iterrows()]
    return X, Y

def transpose(matrix):
    return list(map(list, zip(*matrix)))

def matrix_multiplication(A, B):
    return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]

def matrix_inverse(matrix):
    n = len(matrix)
    identity = [[float(i == j) for i in range(n)] for j in range(n)]
    augmented_matrix = [row[:] + identity_row[:] for row, identity_row in zip(matrix, identity)]

    for i in range(n):
        if augmented_matrix[i][i] == 0:
            for j in range(i + 1, n):
                if augmented_matrix[j][i] != 0:
                    augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                    break
            else:
                raise ValueError("Matrix singular")

        factor = augmented_matrix[i][i]
        augmented_matrix[i] = [element / factor for element in augmented_matrix[i]]

        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                augmented_matrix[j] = [
                    elem_j - factor * elem_i
                    for elem_j, elem_i in zip(augmented_matrix[j], augmented_matrix[i])
                ]
    return [row[n:] for row in augmented_matrix]
