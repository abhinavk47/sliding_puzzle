import sys
import os
PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,PACKAGE_ROOT)
import time
from config.constants import PUZZLE_N
# sys.setrecursionlimit(10**6) 

class Node:
    def __init__(self, puzzle, moves):
        self.puzzle = puzzle
        self.children = []
        self.parent = self
        self.moves = moves
    
    def is_solution(self):
        is_solution = True
        for i in range(len(self.puzzle)):
            if self.puzzle[i]!=i:
                is_solution = False

        return is_solution

    def move_left(self, i):
        puzzle_copy = self.puzzle.copy()
        if i%PUZZLE_N!=0:
            temp = puzzle_copy[i]
            puzzle_copy[i] = puzzle_copy[i-1]
            puzzle_copy[i-1] = temp
            moves_copy = self.moves.copy()
            moves_copy.append('right')
            self.children.append(Node(puzzle_copy, moves_copy))

    def move_right(self, i):
        puzzle_copy = self.puzzle.copy()
        if i%PUZZLE_N!=PUZZLE_N-1:
            temp = puzzle_copy[i]
            puzzle_copy[i] = puzzle_copy[i+1]
            puzzle_copy[i+1] = temp
            moves_copy = self.moves.copy()
            moves_copy.append('left')
            self.children.append(Node(puzzle_copy, moves_copy))

    def move_up(self, i):
        puzzle_copy = self.puzzle.copy()
        if i>PUZZLE_N-1:
            temp = puzzle_copy[i]
            puzzle_copy[i] = puzzle_copy[i-PUZZLE_N]
            puzzle_copy[i-PUZZLE_N] = temp
            moves_copy = self.moves.copy()
            moves_copy.append('down')
            self.children.append(Node(puzzle_copy, moves_copy))

    def move_down(self, i):
        puzzle_copy = self.puzzle.copy()
        if i<PUZZLE_N**2-PUZZLE_N:
            temp = puzzle_copy[i]
            puzzle_copy[i] = puzzle_copy[i+PUZZLE_N]
            puzzle_copy[i+PUZZLE_N] = temp
            moves_copy = self.moves.copy()
            moves_copy.append('up')
            self.children.append(Node(puzzle_copy, moves_copy))

    def make_movement(self):
        for i in range(len(self.puzzle)):
            if self.puzzle[i]==8:
                x=i

        last_move = None
        if len(self.moves)!=0:
            last_move = self.moves[-1]
        
        if last_move!='left':
            self.move_left(x)
        if last_move!='right':
            self.move_right(x)
        if last_move!='up':
            self.move_up(x)
        if last_move!='down':
            self.move_down(x)
    
    def print_puzzle(self):
        for i in range(PUZZLE_N):
            for j in range(PUZZLE_N):
                print(self.puzzle[PUZZLE_N*i+j], end = " ")
            print()
