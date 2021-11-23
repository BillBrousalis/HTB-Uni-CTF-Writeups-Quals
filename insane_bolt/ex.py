#!/usr/bin/env python3
from pwn import *
import sys

ip, port = '64.227.38.214', 32489
r = remote(ip, port)
# ** PLAY **
r.sendlineafter(b'>', b'2')

# emojis used
fire = b'\xf0\x9f\x94\xa5'
tool = b'\xf0\x9f\x94\xa9'
death = b'\xe2\x98\xa0\xef\xb8\x8f'
pl = b'\xf0\x9f\xa4\x96'
gem = b'\xf0\x9f\x92\x8e'


def getjunk(r):
  line = b''
  while fire not in line:
    line = r.recvline()
    if b'HTB' in line:
      print(f'flag : {line.decode()}')
      sys.exit()


def getboard(board):
  # read until bottom border
  while True:
    l = r.recvline()
    line = l.split(b' ')
    # cleanup
    line = [x for x in line if ((x != b'') and (x != b'\n'))]
    # change format
    for idx, item in enumerate(line):
      if item == fire:
        line[idx] = '#'
      elif item == tool:
        line[idx] = ' '
      elif item == death:
        line[idx] = 'D'
      elif item == pl:
        line[idx] = 'O' # player location
      elif item == gem:
        line[idx] = 'X' # gem location

    board.append(line)
    if line[1] == '#':
      break

  # make D's => # for simplicity
  for idx, line in enumerate(board):
    board[idx] = ['#' if item=='D' else item for item in line]
  # reduce board size by removing useless columns
  board = cutdown(board)
  src = [0, board[0].index('O')]
  dest = [len(board)-2, board[-2].index('X')]
  return board, src, dest


# leftover from BFS algorithm approach - not necessary
def cutdown(board):
  if all([line[0] == '#' for line in board]):
    # remove first column
    for idx, line in enumerate(board):
      board[idx] = line[1:]
    cutdown(board)
  elif all([line[-1] == '#' for line in board]):
    # remove last column
    for idx, line in enumerate(board):
      board[idx] = line[:-1]
    cutdown(board)
  return board

  
def render(board):
  print('<render>')
  for line  in board:
    print(' '.join(line))


def solve(board, src, dest, steps):
  if len(steps):
    lstdir = steps[-1]
  else:
    lstdir = 'D'
  # current pos => (x, y)
  x, y = src[0], src[1]
  ylim, xlim = len(board[0]), len(board)
  while True:
    # if dest is reached
    if (x,y) == (dest[0], dest[1]):
      break
    # if immediately close to X
    if y+1 < ylim:
      if board[x][y+1] == 'X':
        steps.append('R')
        break
    if y-1 >= 0:
      if board[x][y-1] == 'X':
        steps.append('L')
        break

    # priority => D then => R if lstdir = R, else L
    if x+1 < xlim:
      if board[x+1][y] != '#':
        x, y = x+1, y 
        steps.append('D')
        return solve(board, [x, y], dest, steps)

    if lstdir == 'R':
      if y+1 < ylim:
        if board[x][y+1] != '#':
          x, y = x, y+1
          steps.append('R')
          return solve(board, [x, y], dest, steps)

      if y-1 >= 0:
        if board[x][y-1] != '#':
          x, y = x, y-1
          steps.append('L')
          return solve(board, [x, y], dest, steps)

    else:
      if y-1 >= 0:
        if board[x][y-1] != '#':
          x, y = x, y-1
          steps.append('L')
          return solve(board, [x, y], dest, steps)

      if y+1 < ylim:
        if board[x][y+1] != '#':
          x, y = x, y+1
          steps.append('R')
          return solve(board, [x, y], dest, steps)

  # remove useless moves like LR or RL => get shortest path
  steps = cleanupsteps(steps)
  return steps


def cleanupsteps(steps):
  steps = ''.join(steps)
  while('RL' in steps) or ('LR' in steps):
    steps = steps.replace('LR', '').replace('RL', '')
  return list(steps)


def exp():
  i = 1
  while True:
    board, steps = [], []
    getjunk(r)
    board, src, dest = getboard(board)
    render(board)

    s = solve(board, src, dest, steps)
    s = ''.join(s)
    print(f'steps : {s}')
    r.sendline(s.encode())

    print('*************************')
    print(f'iter: {i} ==> DONE')
    print('*************************')
    i += 1


if __name__ == '__main__':
  exp()
