class Solution:
    def tictactoe(self, moves):
        board = [[2]*3 for _ in range(3)]
        for i, (r, c) in enumerate(moves):
            board[r][c] = 1 if i % 2 == 0 else 0

        patterns = [
            [[1,1,1],[5,5,5],[5,5,5]],
            [[5,5,5],[1,1,1],[5,5,5]],
            [[5,5,5],[5,5,5],[1,1,1]],
            [[1,5,5],[1,5,5],[1,5,5]],
            [[5,1,5],[5,1,5],[5,1,5]],
            [[5,5,1],[5,5,1],[5,5,1]],
            [[1,5,5],[5,1,5],[5,5,1]],
            [[5,5,1],[5,1,5],[1,5,5]],
        ]

        for pat in patterns:
            diff = [[board[i][j] - pat[i][j] for j in range(3)] for i in range(3)]
            zeros = sum(row.count(0) for row in diff)
            neg_ones = sum(row.count(-1) for row in diff)
            
            if zeros == 3:
                return "A"
            if neg_ones == 3:
                return "B"

        has_empty = any(2 in row for row in board)
        return "Pending" if has_empty else "Draw"


if __name__ == "__main__":
    solution = Solution()
    
    # 力扣官方示例
    print(solution.tictactoe([[0,0],[2,0],[1,0],[2,1],[1,1],[2,2],[1,2]]))  # "A"
    print(solution.tictactoe([[0,0],[1,1],[0,1],[0,2],[1,0],[2,0]]))       # "B"
    print(solution.tictactoe([[0,0],[1,1],[2,0],[1,0],[1,2],[2,2],[0,1],[0,2],[2,1]]))  # "Draw"
    print(solution.tictactoe([[0,0],[1,1]]))                                # "Pending"
