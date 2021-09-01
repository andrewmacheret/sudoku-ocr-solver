import cv2
import numpy as np
from imutils import contours
import pytesseract
from itertools import *
from collections import *
from sudoku import Sudoku

filename = 'sudoku-example.png'
image = cv2.imread(filename, 0)

image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

cnts = [c for c in cnts if 5000 <= cv2.contourArea(c) <= 9999]

grid = []

cnts, _ = contours.sort_contours(cnts, method="top-to-bottom")

grid.append([*'+-----------------+'])
for i,cnt_row in enumerate(zip(*[iter(cnts)] * 9)):
  cnt_row, _ = contours.sort_contours(cnt_row, method="left-to-right")
  print('...')
  if i != 0:
    row = []
    for c in cnt_row:
      x,y,w,h = cv2.boundingRect(c)
      x,y = x+5, y+5
      w,h = w-10,h-10
      line_size_top = max(len([*v]) for k,v in groupby(*zip(*image[y-15:y, x+w//2:x+w//2+1])) if k==0)
      top = ' ' if line_size_top <= 4 else '-'
      row.append(top)
      row.append(' ')
    row.pop()
    grid.append(['|'] + row + ['|'])

  row = []

  for c in cnt_row:
    x,y,w,h = cv2.boundingRect(c)
    x,y = x+5, y+5
    w,h = w-10,h-10
    line_size_left = max(len([*v]) for k,v in groupby(*image[y+h//2:y+h//2+1, x-15:x]) if k==0)
    
    left = ' ' if line_size_left <= 4 else '|'
    row.append(left)
    
    ROI = image[y:y+h, x:x+w]

    s = pytesseract.image_to_string(
      ROI,
      lang='eng',
      config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'
    ).strip() or '.'
    row.append(s)
  grid.append(row + ['|'])
grid.append([*'+-----------------+'])

n, m = len(grid), len(grid[0])
for x,y in product(range(0, n, 2), range(0, m, 2)):
  hori = any(0<=x+dx<m and grid[y][x+dx] != ' ' for dx in (-1,1))
  vert = any(0<=y+dy<n and grid[y+dy][x] != ' ' for dy in (-1,1))
  if hori and vert:
    grid[y][x] = '+'
  elif hori:
    grid[y][x] = '-'
  elif vert:
    grid[y][x] = '|'

# sigh...
grid[1][3] = '9'

grid = [''.join(row) for row in grid]

print('\n'.join(grid))
print('->')
grid = Sudoku().parse_and_solve(grid)
print('\n'.join(grid))


cv2.imshow('image', image)
cv2.waitKey()


