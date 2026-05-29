# 给定一个 m x n 的矩阵，如果一个元素为 0 ，则将其所在行和列的所有元素都设为 0 。请使用 原地 算法。

def setZeroes(matrix):
    m = len(matrix)#行
    n = len(matrix[0])#列

    i = 0
    j = 0
    n = 0
    
    #判断有几个0
    while matrix[i][j] == 0 and i <= m-1 and j <= n-1:
        n += 1
        i +=1
    
    
    

    
    


