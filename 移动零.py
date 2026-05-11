# 给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。
# 请注意 ，必须在不复制数组的情况下原地对数组进行操作。

a = [0,1,0,3,12]

def move_zeroes(nums):
    for i in range(len(nums)):
        for i in range(len(nums)-1):
            if nums[i] == 0 and nums[i+1] != 0:

                nums[i], nums[i+1] = nums[i+1], nums[i]
          
    return a

print(move_zeroes(a))