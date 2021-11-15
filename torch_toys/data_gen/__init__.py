import torch
from typing import Optional, Tuple, TypedDict
from torch_toys import _C
import random

class MKNTicTacToeState(TypedDict):
    board: str
    next_move: str
    winner: str


class MNKTicTacToe:
    def __init__(self, m:int=3, n:int=3, k:int=3):
        self.m = m
        self.n = n
        self.k = k
    
    def generate(self, turn:Optional[int]=None)->MKNTicTacToeState:
        res: MKNTicTacToeState = {}
        board = [' '] * (self.m * self.n)

        if turn is None:
            turn = random.randint(0, self.m * self.n - 1)

        winner = ''
        turnidx = -1
        for turnidx, chosen in enumerate(random.sample(range(self.m * self.n), turn)):
            board[chosen] = 'o' if turnidx % 2 == 1 else 'x'
            winner = _C.tictactoe_winner(''.join(board), self.m, self.n, self.k)
            if winner != ' ': break

        res['board'] = ''.join(board)
        res['winner'] = winner
        res['next_move'] = 'o' if (turnidx + 1) % 2 == 1 else 'x'
        return res
    
    def winner(self, s: MKNTicTacToeState)->str:
        if not 'winner' in s:
            s['winner'] = _C.tictactoe_winner(s['board'], self.m, self.n, self.k)
        return s['winner']
    
    def format_board(self, s: MKNTicTacToeState)->str:
        res = []
        for idx, ch in enumerate(s['board']):
            ridx = idx // self.n
            cidx = idx % self.n
            if cidx > 0:
                res.append('|')
            elif ridx > 0:
                res.append('---+' * (self.n - 1) + '---\n')
            res.append(f' {ch} ')
            if cidx == self.n - 1:
                res.append('\n')
        return ''.join(res)
            
    def board_to_tensor(self, s: MKNTicTacToeState)->torch.Tensor:
        res = [0] * (self.m * self.n)
        for idx, ch in enumerate(s['board']):
            if ch == ' ':
                res[idx] = 0
            elif ch == 'x':
                res[idx] = 1
            elif ch == 'o':
                res[idx] = 2
        return torch.tensor(res, dtype=torch.int64)


    def board_pos_to_tensor(self)->Tuple[torch.Tensor]:
        row_res = [] 
        col_res = [] 
        for ridx in range(self.m):
            for cidx in range(self.n):
                row_res.append(ridx / (self.m-1))
                col_res.append(cidx / (self.n-1))
        return torch.tensor(row_res, dtype=torch.float32), torch.tensor(col_res, dtype=torch.float32)


    def winner_to_tensor(self, s: MKNTicTacToeState)->torch.Tensor:
        w = self.winner(s)

        w_int = 0
        if w == 'x': w_int = 1 
        elif w == 'o': w_int = 2

        res = [w_int]
        return torch.tensor(res, dtype=torch.int64)


    def next_to_tensor(self, s: MKNTicTacToeState)->torch.Tensor:
        n = s['next_move'] 

        n_int = 0
        if n == 'x': n_int = 1 
        elif n == 'o': n_int = 2

        res = [n_int]
        return torch.tensor(res, dtype=torch.int64)
        

if __name__ == '__main__':
    gen = MNKTicTacToe(3, 3, 3)
    s = gen.generate()
    print(gen.format_board(s))
    print(f'winner = {gen.winner(s)}')
    print(gen.board_to_tensor(s))
    print(gen.board_pos_to_tensor())
    print(gen.winner_to_tensor(s))
    print(gen.next_to_tensor(s))