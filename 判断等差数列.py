arr = [3,5,1]

def canMakeArithmeticProgression(arr):
    if len(arr) == 1 or len(arr) == 2:
        return True
    
    new_arr = sorted(arr)
    diff = new_arr[1] - new_arr[0]
    i = 0

    for j in range(len(arr)-1):
        if new_arr[j+1] == new_arr[j] + diff:
            i += 1
        else:
            i = i
    
    if i == len(arr)-1:
        return True
    else:
        return False
   
print(canMakeArithmeticProgression(arr))
