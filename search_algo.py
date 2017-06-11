from collections import deque
from math import sqrt
import sys
import copy
import bisect


class Problem:
	def __init__(self, initial_board, goal_board):
		self.initial_board = Board(initial_board)
		self.goal_board = Board(goal_board)
		
	def actions(self, board):
                #UDLR
		possible_moves = [["Down", "Right"],
                                  ["Down", "Left", "Right"],
                                  ["Left", "Down"],
                                  ["Up", "Down", "Right"],
                                  ["Up", "Down", "Left", "Right"],
                                  ["Up", "Down", "Left"],
                                  ["Up", "Right"],
                                  ["Up", "Left", "Right"],
                                  ["Up", "Left"]]
		return possible_moves[board.state.index("0")]
		
	def result(self, board, action):
		if action == "Left":
			return board.move("Left")
		elif action == "Right":
			return board.move("Right")
		elif action == "Down":
			return board.move("Down")
		elif action == "Up":
			return board.move("Up")
	
	def goalTest(self, board):
		return board == self.goal_board
		
	def pathCost(self, cost, board_now, action, next_board):
		return cost + 1
	
class Board:
	def __init__(self, state, parent = None, action = None, path_cost = 0):
		self.state = copy.copy(state)
		self.parent = parent
		self.action = action
		self.path_cost = path_cost
		self.depth = 0
		if parent:
			self.depth = parent.depth + 1		
	
	def __eq__(self, other):
		return isinstance(other, Board) and self.state == other.state

	def __str__(self):
		return "<| Board Items: {} |>".format(self.state)

	def __lt__(self, node):
		return self.path_cost < node.path_cost

	def __hash__(self):
		return hash((",").join(self.state))

	def swapStateContent(self, empty_pos, new_pos):
		new_pos_holder = self.state[new_pos]
		self.state[new_pos] = "0"
		self.state[empty_pos] = new_pos_holder
		return self
		
	def move(self, direction):
		empty_pos = self.state.index("0")
		up_down_gauge = int(sqrt(len(self.state)))
		if direction == "Left":
			new_pos = empty_pos - 1
			return self.swapStateContent(empty_pos, new_pos)
		elif direction == "Right":
			new_pos = empty_pos + 1
			return self.swapStateContent(empty_pos, new_pos)
		elif direction == "Up":
			new_pos = empty_pos - up_down_gauge
			return self.swapStateContent(empty_pos, new_pos)
		elif direction == "Down":
			new_pos = empty_pos + up_down_gauge
			return self.swapStateContent(empty_pos, new_pos)
	
	def expand(self, problem):
		m_list = set()
		
		for action in problem.actions(self):
			child = self.childBoard(problem, action)
			m_list.add(child)
			#print(child.state, action)
		return m_list

	def childBoard(self, problem, action):
		my_copy = Board(self.state, self.parent, self.action, self.path_cost)
		next_board = problem.result(my_copy, action)
		return Board(next_board.state, self, action, problem.pathCost(self.path_cost, self.state, action, next_board.state))
	
	def traceBack(self):
		board, parent_n_granies = self, [self]
		while board.parent:
			parent_n_granies.append(board)
			board = board.parent
		return parent_n_granies;
		
	def solution(self, string = False):
		solution_actions = [board.action for board in self.traceBack()]
		return ",".join(solution_actions) if string else solution_actions
		
class QueueType:
	def __init__(self, items=[], length = None):
		self.Queue = deque(items, length)

	def __len__(self):
		return len(self.Queue)

	def __contains__(self, item):
		return item in self.Queue

	def pop(self):
		if len(self.Queue) > 0:
			return self.Queue.popleft()
		else :
			raise Exception('Queue is empty')

	def addItem(self, item):
		if not len(self.Queue) < self.Queue.maxlen:
			self.Queue.append(item)
		else:
			raise Exception('Queue is full')

	def addItems(self, items):
		if not len(items) + len(self.Queue)  <= self.Queue.maxlen:
			self.Queue.extend(items)
		else:
			raise Exception('Queue max length will be overflown')

	def length(self):
		return len(self.Queue)

	def contains(self, item):
		return item in self.Queue

def StackType():
	return []

class PriorityQueueType():
	def __init__(self, direction = 'smallest', f = lambda x: x):
		self.container = []
		self.direction = direction
		self.func = f

	def __delitem__(self, elem):
		for i, (value, elem) in enumerate(self.container):
			if elem == key:
				self.container.pop(i)

	def __len__(self):
		return len(self.container)

	def __contains__(self, elem):
		return any(elem == child[1] for child in self.container)

	def __getitem__(self, key):
		for _, item in self.container:
			if item == key:
				return item

	def append(self, elem):
		bisect.insort_right(self.container, (self.func(elem), elem))

	def pop(self):
		if self.direction == 'smallest':
			return self.container.pop(0)[1]
		else:
			return self.container.pop()[1]


class ImplementSearch:
	def __init__(self, algo, problem, func = None):
		if algo == "BFS":
			self.breadthFirstSearch(problem)
		elif algo == "DFS":
			self.depthFirstSearch(problem)
		elif algo == "AST":
			self.aStarSearch(problem)
	
	def breadthFirstSearch(self, problem):
		ini_board = problem.initial_board
		if problem.goalTest(ini_board):
			print(ini_board)
			return ini_board
		frontier = QueueType()
		frontier.addItem(ini_board)
		explored = []
		while frontier:
			board = frontier.pop()
			if(board.state not in explored):
				explored.append(board.state)
				print(board.state, board.action, board.path_cost)
				print(".................................")
			for child in board.expand(problem):	
				if child.state not in explored and child not in frontier:
					if problem.goalTest(child):
						print(child)
						return child
						sys.exit()
					frontier.addItem(child)
			
		return None
			
	def depthFirstSearch(self, problem):
		ini_board = problem.initial_board
		frontier = StackType()
		frontier.append(ini_board)
		explored = []
		while frontier:
			board = frontier.pop()
			if problem.goalTest(board):
				return board
			if(board.state not in explored):
				explored.append(board.state)
				print(board.state, board.action, board.path_cost)
				print(".................................")
			frontier.extend(child for child in board.expand(problem)
							if child.state not in explored and
							child not in frontier)
		return None

	def aStarSearch(self, problem):
		func = heuristic_h
		board = problem.initial_board
		if problem.goalTest(board):
			return board
		frontier = PriorityQueueType("smallest", func)
		frontier.append(board)
		explored = []
		while frontier:
			board = frontier.pop()
			if problem.goalTest(board):
				print(board.solution())
				return board
			explored.append(board.state)
			#print(board.state, board.action, board.path_cost, func(board))
			#print(".................................")
			for child in board.expand(problem):
				if child.state not in explored and child not in frontier:
					frontier.append(child)
				elif child in frontier:
					incumbent = frontier[child]
					if func(child) < func(incumbent):
						del frontier[incumbent]
						frontier.append(child)
		return None

def cacheFuncValues(fn, slot = None, maxsize = 32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn

def heuristic_h(board):
	goal = ["0","1","2","3","4","5","6","7","8"]
	return sum(abs(int(s) % 3 - int(g) % 3) + abs(int(s) // 3 - int(g) // 3)
        for s, g in ((board.state.index(str(i)), goal.index(str(i))) for i in range(1, 9))) + board.path_cost

def writeToFile(line):
	f = open('output.txt', 'a')
	f.write(line)
	f.write("\n")
	f.close()

if __name__ == "__main__":
	algo = sys.argv[1]
	problem_string = sys.argv[2]
	print(algo)
	f = open('output.txt', 'w')
	f.write("---------------------------------------------------------------------------\n")
	f.write("                          First Men AI Search Algorithm                    \n")
	f.write("---------------------------------------------------------------------------\n")
	f.close()
	problem = Problem(problem_string.split(","), ["0","1","2","3","4","5","6","7","8"])
	ImplementSearch(algo, problem)
	
