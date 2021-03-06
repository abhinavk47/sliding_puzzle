import sys
import os
PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,PACKAGE_ROOT)
import time
from config.constants import PUZZLE_N
# sys.setrecursionlimit(10**6) 

def get_distance(puzzle):
    distance = 0 
    for i in range(len(puzzle)):
        if puzzle[i]!=PUZZLE_N**2-1:
            distance+=abs(puzzle[i]%PUZZLE_N-i%PUZZLE_N)
            distance+=abs(puzzle[i]//PUZZLE_N-i//PUZZLE_N)

    return distance

def BFS(puzzle_list):
    node = Node(puzzle_list, [], [])
    open_list = []
    open_list.append(node)
    finished = False
    moves = None
    no_of_iterations = 1
    max_moves = (PUZZLE_N**2-(PUZZLE_N-2)**2-1)*(PUZZLE_N-1)*2

    max_distance = (PUZZLE_N**2-(PUZZLE_N-2)**2-1)*(2*PUZZLE_N-3)

    while len(open_list)!=0 and not finished:
        current_node = open_list[0]
        open_list.pop(0)
        current_node.make_movement()
        for x in current_node.children:
            if len(x.moves)>max_moves or \
                (len(x.distances)>max_moves-max_distance and x.distances[-1]>max_moves-len(x.distances)+1):
                continue
            if x.is_solution():
                print(x.distances)
                moves = x.moves
                finished = True
            open_list.append(x)
            no_of_iterations+=1

    return moves, no_of_iterations

class Node:
    def __init__(self, puzzle, moves, distances):
        self.puzzle = puzzle
        self.children = []
        self.parent = self
        self.moves = moves
        self.distances = distances
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
            distances = self.distances.copy()
            distances.append(get_distance(self.puzzle))
            self.children.append(Node(puzzle_copy, moves_copy, distances))

    def move_right(self, i):
        puzzle_copy = self.puzzle.copy()
        if i%PUZZLE_N!=PUZZLE_N-1:
            temp = puzzle_copy[i]
            puzzle_copy[i] = puzzle_copy[i+1]
            puzzle_copy[i+1] = temp
            moves_copy = self.moves.copy()
            moves_copy.append('left')
            distances = self.distances.copy()
            distances.append(get_distance(self.puzzle))
            self.children.append(Node(puzzle_copy, moves_copy, distances))

    def move_up(self, i):
        puzzle_copy = self.puzzle.copy()
        if i>PUZZLE_N-1:
            temp = puzzle_copy[i]
            puzzle_copy[i] = puzzle_copy[i-PUZZLE_N]
            puzzle_copy[i-PUZZLE_N] = temp
            moves_copy = self.moves.copy()
            moves_copy.append('down')
            distances = self.distances.copy()
            distances.append(get_distance(self.puzzle))
            self.children.append(Node(puzzle_copy, moves_copy, distances))

    def move_down(self, i):
        puzzle_copy = self.puzzle.copy()
        if i<PUZZLE_N**2-PUZZLE_N:
            temp = puzzle_copy[i]
            puzzle_copy[i] = puzzle_copy[i+PUZZLE_N]
            puzzle_copy[i+PUZZLE_N] = temp
            moves_copy = self.moves.copy()
            moves_copy.append('up')
            distances = self.distances.copy()
            distances.append(get_distance(self.puzzle))
            self.children.append(Node(puzzle_copy, moves_copy, distances))

    def make_movement(self):
        for i in range(len(self.puzzle)):
            if self.puzzle[i]==PUZZLE_N**2-1:
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

if __name__ == "__main__":
    puzzle = [15,14,13,12,11,9,5,8,7,6,10,4,3,2,1,0]
    # start = time.time()
    # moves, no_of_iterations = BFS(puzzle)
    # print(moves)
    # print(time.time()-start)
    # print(no_of_iterations)
    print(get_distance(puzzle))


