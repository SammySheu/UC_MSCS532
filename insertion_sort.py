def insertion_sort(nums: list[int]):
    # i started with 1 because the first is already sorted
    for i in range(1, len(nums)):
        j = i - 1
        while j >= 0 and nums[j] < nums[j+1]:
            # like bubble sort, compare it one by one
            nums[j], nums[j+1] = nums[j+1], nums[j]
            j -= 1

if __name__ == '__main__':
    nums = [1,2,3,4,5]
    # Since list is a mutable object, 
    # it is access the same memory within the function
    insertion_sort(nums)
    print(nums)
