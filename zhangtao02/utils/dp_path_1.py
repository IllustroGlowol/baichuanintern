class Solution:
    def minPathSum(self, grid):
        # 步骤1:dp数组:dp[i][j]:[0,0] 到 [i,j]的不同路径数
        m, n = len(grid), len(grid[0])
        dp = [[float("inf") for _ in range(n)] for _ in range(m)]

        # 步骤2:边界条件
        dp[0][0] = grid[0][0]
        for i in range(m):
            dp[i][0] = dp[i-1][0] + grid[i][0]
        for j in range(n):
            dp[0][j] = dp[0][j-1] + grid[0][j]

        # 步骤3:遍历填表
        for i in range(1, m):
            for j in range(1, n):
                # 步骤4:转移方程
                dp[i][j] = min(
                    dp[i-1][j],
                    dp[i][j-1]) + grid[i][j]
        

        # 步骤5:返回值
        return dp[-1][-1]