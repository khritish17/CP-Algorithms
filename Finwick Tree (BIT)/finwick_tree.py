class FinwickTree:
    def __init__(self, nums):
        self.nums = nums
        self.bit = [0] * (len(nums) + 1) # BIT = Binary Indexed Tree

        # Initiate the Finwick Tree/ BIT 
        for ind, ele in enumerate(self.nums):
            self.point_update(index = ind, val = 2*ele, init = True) 
            # Reasoning behind val = 2 * ele is to use the point update function rather than rewriting the init code
            # if val = ele, then diff in point_upadte will be diff = ele - ele = 0, the whole self.bit will initialized as 0
            # but if val = 2 * ele than diff = 2 * ele - ele = ele
    
    def point_update(self, index, val, init = False):
        # update the index with val
        diff = val - self.nums[index]

        # update the self.nums at index with val
        if not init:
            self.nums[index] = val
        index += 1
        while index < len(self.bit):
            self.bit[index] += diff
            # go to its next index
            index += (index & (-index))
    
    def prefix_sum(self, index):
        # Returns the prefix sum till self.nums[index] (inclusive)
        index += 1
        pre_sum = 0
        while index > 0:
            pre_sum += self.bit[index]
            # go to its parent node
            index -= (index & (-index))
        return pre_sum
    
    def range_sum(self, index_i, index_j):
        # return the sum in the range self.nums[index_i] ... to .... self.nums[index_j]
        if index_i == 0:
            return self.prefix_sum(index_j)
        else:
            return self.prefix_sum(index_j) - self.prefix_sum(index_i - 1)

# Example:
# FT = FinwickTree(nums = [3, 2, -1, 6, 5])
# print(FT.range_sum(2, 4))
# FT.point_update(3, 10)
# print(FT.range_sum(2, 4))
