# 给你一个整数数组 nums ，
# 判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，
# 同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。

# 注意：答案中不可以包含重复的三元组。

nums = [-1,0,1,2,-1,-4]

# def threeSum(nums):
#     n = len(nums)
#     result = []
#     nums.sort()

#     for i in range(n - 2):
#         if i > 0 and nums[i] == nums[i-1]:
#             continue
#         left = i + 1
#         right = n - 1

#         while left < right:
#             total = nums[i] + nums[left] + nums[right]
#             if total ==0:
#                 result.append([nums[i],nums[left],nums[right]])
#                 left += 1
#                 right -= 1

#                 while left < right and nums[left] == nums[left - 1]:
#                     left +=1
#                 while left < right and nums[right] == nums[right + 1]:
#                     right -= 1
#             elif total < 0:
#                 left += 1
#             else:
#                 right -= 1 
#     return result
def threeSum(nums):
    n = len(nums)
    nums.sort()
    result = []

    for i in range(n-1,0,-1):
        if i < n-1 and nums[i] == nums[i+1]:
            continue
        left = 0
        right = i - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i],nums[left],nums[right]])
                left +=1
                right -=1

                while left < right and nums[left] == nums[left-1]:
                    left +=1
                while left < right and nums[right] == nums[right+1]:
                    right -=1
            elif total < 0:
                left +=1
            else:
                right -=1
    return result

if __name__ == "__main__":
    print(threeSum(nums))

    





