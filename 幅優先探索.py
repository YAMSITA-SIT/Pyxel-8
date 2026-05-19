import pyxel
from collections import deque

NN = 3  # グリッドの行・列数
SZ = 40  # タイルのサイズ

goalstate = tuple(list(range(1, NN * NN)) + [0])

def nextmoves(stat):
    zeropos = stat.index(0)
    nextstatL = []
    for panel in range(NN * NN):
        if App.mdist(panel, zeropos) == 1:
            newstat = list(stat).copy()
            newstat[zeropos], newstat[panel] = stat[panel], 0
            nextstatL.append(tuple(newstat))
    return nextstatL

def solver(board):
    print("Auto-solving ...")
    start = tuple(board)
    queue = deque([[start]])  # path のリストを入れる
    visited = set()
    visited.add(start)

    for _ in range(10000000000):
        if not queue:
            break
        path = queue.popleft()
        stat = path[-1]

        if stat == goalstate:
            print(f"解けました({len(path) - 1}ステップ)")
            for i, state in enumerate(path):
                print(f"{i}: {list(state)}")
            return [list(s) for s in path[1:]]

        for newstat in nextmoves(stat):
            if newstat not in visited:
                visited.add(newstat)
                queue.append(path + [newstat])

    print("give up")
    return []

class App:
    def __init__(self):
        pyxel.init(NN * SZ, NN * SZ + 20, title="8 Puzzle")
        pyxel.mouse(True)
        self.new_game()
        self.solution = solver(self.board.copy())
        pyxel.run(self.update, self.draw)

    def new_game(self):
        self.board =[8, 6, 7, 2, 5, 4, 3, 0, 1]# 初期配置
        self.steps = 0
        print(f'New game: {self.board}')

    def show_step(self):
        if self.solution:
            self.board = self.solution.pop(0)
            self.steps += 1

    def update(self):
        if pyxel.frame_count % 10 == 0:
            self.show_step()

    def draw(self):
        pyxel.cls(0)
        for i, v in enumerate(self.board):
            x = (i % NN) * SZ
            y = (i // NN) * SZ
            if v:
                color = v % 15 + 1
                pyxel.rect(x, y, SZ - 2, SZ - 2, color)
                font_color = 0 if color in [6, 7, 8, 10, 12, 13] else 7
                pyxel.text(x + 15, y + 13, str(v), font_color)
        pyxel.text(30, NN * SZ + 5, f"{self.steps}steps", 6)
        if self.board == list(goalstate):
            pyxel.text(110, NN * SZ + 5, "Done!", 8)

    @staticmethod
    def mdist(p1, p2):
        x1, y1 = p1 % NN, p1 // NN
        x2, y2 = p2 % NN, p2 // NN
        return abs(x1 - x2) + abs(y1 - y2)

# 実行
App()
