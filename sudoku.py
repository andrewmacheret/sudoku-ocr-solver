from collections import *
from itertools import *

digits = set(range(1, 10))
dirs = [(-1,0),(1,0),(0,-1),(0,1)]

class Sudoku:
  def parse_and_solve(self, board):
    A, B = self.parse(board)
    self.solve(A, B)
    board = board[:]
    for x,y in product(range(9), repeat=2):
      bx, by = 2*x + 1, 2*y + 1
      if board[by][bx] == '.':
        board[by] = board[by][:bx] + str(A[y][x]) + board[by][bx+1:]
    return board

  def parse(self, board):
    A = [[0 for _ in range(9)] for _ in range(9)]
    B = [[0 for _ in range(9)] for _ in range(9)]
    regions = count(1)
    for x,y in product(range(9), repeat=2):
      bx, by = 2*x + 1, 2*y + 1
      c = board[by][bx]
      A[y][x] = 0 if c == '.' else int(c)
      if B[y][x] == 0:
        region = next(regions)
        q = deque([(bx, by)])
        while q:
          ax, ay = q.popleft()
          B[ay//2][ax//2] = region
          for dx, dy in dirs:
            if board[ay+dy][ax+dx] == ' ' and B[ay//2+dy][ax//2+dx] == 0:
              q.append((ax+dx*2, ay+dy*2))
    return A, B

  def solve(self, A, B):
    blanks = [(x,y) for x,y in product(range(9), repeat=2) if A[y][x] == 0]
    regions = [[] for _ in range(9)]
    for x,y in product(range(9), repeat=2):
      regions[B[y][x]-1].append((x,y))

    def recursive(index):
      if index == len(blanks): return 1
      x, y = blanks[index]
      for c in digits - digits_in_row(x, y):
        A[y][x] = c
        if recursive(index + 1): return 1
        A[y][x] = 0

    def digits_in_row(x, y):
      r = B[y][x] - 1
      f = lambda i: (A[y][i], A[i][x], A[regions[r][i][1]][regions[r][i][0]])
      return set(c for i in range(9) for c in f(i) if c != 0)

    recursive(0)


if __name__ == "__main__":
  board = [
    '+-----+---+-------+',
    '|. 9 .|. .|. 2 . .|',
    '|     +-+ |       |',
    '|2 . . 3|.|1 . . .|',
    '| +-+ +-+ +-----+ |',
    '|4|.|7|. . 2 . 1|.|',
    '+-+ +-+-+ +-+---+-+',
    '|9 6|. .|.|.|. . .|',
    '|   +-+ +-+ |     |',
    '|. 4 8|5 . .|. . 6|',
    '|     | +-+ +-+   |',
    '|. . .|.|8|. .|. .|',
    '+-+---+-+ +-+-+ +-+',
    '|7|. 6 . . .|.|.|.|',
    '| +-----+ +-+ +-+ |',
    '|8 . . 1|7|. . . .|',
    '|       | +-+     |',
    '|. 2 . .|. .|. . .|',
    '+-------+---+-----+',
  ]
  print('\n'.join(board))
  print('->')
  board = Sudoku().parse_and_solve(board)
  print('\n'.join(board))
