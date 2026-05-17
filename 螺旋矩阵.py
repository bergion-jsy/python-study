# 给你一个 m 行 n 列的矩阵 matrix ，请按照 顺时针螺旋顺序 ，返回矩阵中的所有元素。

# 测试用例 1: 3x3 矩阵
matrix1 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# 测试用例 2: 1x1 矩阵
matrix2 = [[1]]

# 测试用例 3: 1xn 矩阵
matrix3 = [[1, 2, 3, 4]]

# 测试用例 4: mx1 矩阵
matrix4 = [
    [1],
    [2],
    [3]
]

# 测试用例 5: 3x4 矩阵
matrix5 = [
    [ 1,  2,  3,  4],
    [ 5,  6,  7,  8],
    [ 9, 10, 11, 12]
]

# 测试用例 6: 4x3 矩阵
matrix6 = [
    [ 1,  2,  3],
    [ 4,  5,  6],
    [ 7,  8,  9],
    [10, 11, 12]
]

# 测试用例 7: 空矩阵
matrix7 = []

# 测试用例 8: 空行矩阵
matrix8 = [[]]

# 测试用例 9: 2x2 矩阵
matrix9 = [
    [1, 2],
    [3, 4]
]

# 测试用例 10: 2x3 矩阵
matrix10 = [
    [1, 2, 3],
    [4, 5, 6]
]

def spiralOrder(matrix):
    if not matrix or not matrix[0]:
        return []
    
    m , n = len(matrix) , len(matrix[0])
    result = []
    top , bottom = 0 , m-1
    left , right = 0 , n-1

    while top <= bottom and left <= right:
        for j in range(left,right + 1):
            result.append(matrix[top][j])
        top +=1

        for i in range(top,bottom + 1):
            result.append(matrix[i][right])
        right -=1

        if top <= bottom:
            for j in range(right,left - 1,-1):
                result.append(matrix[bottom][j])
            bottom -=1

        if left<=right:
            for i in range(bottom,top - 1,-1):
                result.append(matrix[i][left])
            left +=1
    return result


# 运行所有测试
test_cases = [
    (matrix1, [1, 2, 3, 6, 9, 8, 7, 4, 5]),
    (matrix2, [1]),
    (matrix3, [1, 2, 3, 4]),
    (matrix4, [1, 2, 3]),
    (matrix5, [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]),
    (matrix6, [1, 2, 3, 6, 9, 12, 11, 10, 7, 4, 5, 8]),
    (matrix7, []),
    (matrix8, []),
    (matrix9, [1, 2, 4, 3]),
    (matrix10, [1, 2, 3, 6, 5, 4]),
]

for i, (matrix, expected) in enumerate(test_cases, 1):
    result = spiralOrder(matrix)
    status = "✅" if result == expected else "❌"
    print(f"测试 {i}: {status}")
    print(f"  结果: {result}")
    print(f"  预期: {expected}")
    if result != expected:
        print(f"  👆 不匹配!")
    print()