# 给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，
# 计算按此排列的柱子，下雨之后能接多少雨水。

height = [0,1,0,2,1,0,1,3,2,1,2,1]

def trap(nums):
    n = len(nums)
    left = 0
    right = n - 1
    square = 0

    while left < right:
        # 如果左边比右边矮，就看左边
        if nums[left] < nums[right]:
            if nums[left] > nums[left + 1]:
                square += nums[left] - nums[left+1]
                nums[left + 1] = nums[left]
            left +=1
        else:
            if nums[right]>nums[right-1]:
                square += nums[right] - nums[right-1]
                nums[right-1] = nums[right]
            right -= 1
        
    return square

print(trap(height))

