def diagonalSum(mat):
    n = len(mat)
    total = 0
    if n % 2 == 1:          # 奇数
        mid = n // 2
        total = mat[mid][mid]  # 中心元素只加一次
        for i in range(mid):
            total += mat[i][i]           # 主对角线：左上
            total += mat[i][n-1-i]       # 副对角线：右上
            total += mat[n-1-i][i]       # 副对角线：左下
            total += mat[n-1-i][n-1-i]   # 主对角线：右下
    else:                   # 偶数
        for i in range(n // 2):
            total += mat[i][i]
            total += mat[i][n-1-i]
            total += mat[n-1-i][i]
            total += mat[n-1-i][n-1-i]
        return total
        
