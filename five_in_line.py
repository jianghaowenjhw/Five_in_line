# 用tkinter写一个五子棋小游戏

from enum import Enum
from typing import Optional, Tuple, List
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Player(Enum):
    """玩家枚举类"""
    BLACK = "黑子"
    WHITE = "白子"
    EMPTY = "空"

class GameMode(Enum):
    """游戏模式枚举类"""
    PVP = "玩家对战"
    PVE = "人机对战"

class GameSettings:
    """游戏设置类"""
    def __init__(self) -> None:
        self.board_size: int = 15  # 默认15*15
        self.game_mode: GameMode = GameMode.PVE  # 默认人机对战
        self.player_color: Player = Player.BLACK  # PVE模式下玩家执子颜色
class ChessBoard:
    """棋盘类"""
    def __init__(self, master: tk.Frame, size: int) -> None:
        self.master = master
        self.size = size
        self.board: List[List[Player]] = [[Player.EMPTY] * size for _ in range(size)]
        self.canvas: Optional[tk.Canvas] = None
        self._init_board()
    
    def _init_board(self) -> None:
        """初始化棋盘"""
        # 计算画布大小 (每个格子30像素 + 边距)
        canvas_size = self.size * 30 + 40
        self.canvas = tk.Canvas(self.master, 
                              width=canvas_size, 
                              height=canvas_size, 
                              bg='#FFEEBB')
        self.canvas.pack()

        # 绘制棋盘网格
        for i in range(self.size):
            # 垂直线
            self.canvas.create_line(30 + i * 30, 30,
                                  30 + i * 30, canvas_size - 30)
            # 水平线
            self.canvas.create_line(30, 30 + i * 30,
                                  canvas_size - 30, 30 + i * 30)

    def place_piece(self, row: int, col: int, player: Player) -> bool:
        """放置棋子"""
        if self.board[row][col] != Player.EMPTY:
            return False
        
        self.board[row][col] = player
        x, y = 30 + col * 30, 30 + row * 30
        color = 'black' if player == Player.BLACK else 'white'
        
        # 绘制棋子
        self.canvas.create_oval(x-13, y-13, x+13, y+13, 
                              fill=color, outline='black')
        return True

    def check_win(self, row: int, col: int) -> bool:
        """检查胜利"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 水平、垂直、两个对角线
        player = self.board[row][col]

        for dx, dy in directions:
            count = 1
            # 正向检查
            for i in range(1, 5):
                new_row, new_col = row + dx * i, col + dy * i
                if (0 <= new_row < self.size and 
                    0 <= new_col < self.size and 
                    self.board[new_row][new_col] == player):
                    count += 1
                else:
                    break
            
            # 反向检查
            for i in range(1, 5):
                new_row, new_col = row - dx * i, col - dy * i
                if (0 <= new_row < self.size and 
                    0 <= new_col < self.size and 
                    self.board[new_row][new_col] == player):
                    count += 1
                else:
                    break
                    
            if count >= 5:
                return True
        
        return False

class AI:
    """AI类"""
    def __init__(self, board: ChessBoard, color: Player):
        self.board = board
        self.color = color

    def make_move(self) -> Optional[Tuple[int, int]]:
        """AI下棋"""
        # 简单AI策略：找到第一个空位
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] == Player.EMPTY:
                    return i, j
        return None

class FiveInLine:
    """五子棋游戏主类"""
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("五子棋")
        self.settings = GameSettings()
        self.current_player: Player = Player.BLACK
        self.chess_board: Optional[ChessBoard] = None
        self._init_ui()
        self.game_over: bool = False
        self.ai: Optional[AI] = None

    def _init_ui(self) -> None:
        """初始化用户界面"""
        # 创建按钮框架
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        # 设置按钮
        self.settings_button = ttk.Button(
            self.button_frame, 
            text="设置",
            command=self._show_settings
        )
        self.settings_button.pack(side=tk.LEFT, padx=5)

        # 开始游戏按钮
        self.start_button = ttk.Button(
            self.button_frame,
            text="开始游戏",
            command=self._start_game
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        # 棋盘框架
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=5)

    def _show_settings(self) -> None:
        """显示设置对话框"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("游戏设置")
        settings_window.geometry("300x200")
        settings_window.resizable(False, False)
    
        # 棋盘大小设置
        size_frame = ttk.LabelFrame(settings_window, text="棋盘大小")
        size_frame.pack(padx=10, pady=5, fill="x")
        size_var = tk.StringVar(value=str(self.settings.board_size))
        for size in [10, 15, 20]:
            ttk.Radiobutton(size_frame, text=f"{size}×{size}", 
                           variable=size_var, value=str(size),
                           command=lambda s=size: setattr(self.settings, 'board_size', s)
                           ).pack(side=tk.LEFT, padx=10)
    
        # 游戏模式设置
        mode_frame = ttk.LabelFrame(settings_window, text="游戏模式")
        mode_frame.pack(padx=10, pady=5, fill="x")
        mode_var = tk.StringVar(value=self.settings.game_mode.value)
        for mode in GameMode:
            ttk.Radiobutton(mode_frame, text=mode.value, 
                           variable=mode_var, value=mode.value,
                           command=lambda m=mode: setattr(self.settings, 'game_mode', m)
                           ).pack(side=tk.LEFT, padx=10)
    
        # 玩家颜色设置
        color_frame = ttk.LabelFrame(settings_window, text="执子颜色(PVE模式)")
        color_frame.pack(padx=10, pady=5, fill="x")
        color_var = tk.StringVar(value=self.settings.player_color.value)
        for color in [Player.BLACK, Player.WHITE]:
            ttk.Radiobutton(color_frame, text=color.value, 
                           variable=color_var, value=color.value,
                           command=lambda c=color: setattr(self.settings, 'player_color', c)
                           ).pack(side=tk.LEFT, padx=10)
    
    def _start_game(self) -> None:
        """开始新游戏"""
        # 清理现有棋盘
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        # 创建新棋盘
        self.chess_board = ChessBoard(self.board_frame, self.settings.board_size)
        self.current_player = Player.BLACK
        self.game_over = False
        
        # 如果是PVE模式，创建AI
        if self.settings.game_mode == GameMode.PVE:
            ai_color = Player.WHITE if self.settings.player_color == Player.BLACK else Player.BLACK
            self.ai = AI(self.chess_board, ai_color)
        else:
            self.ai = None
        
        # 绑定点击事件
        self.chess_board.canvas.bind('<Button-1>', self._handle_click)

    def _handle_click(self, event: tk.Event) -> None:
        """处理鼠标点击事件"""
        if self.game_over:
            return

        # 在PVE模式下，如果不是玩家回合，直接返回
        if (self.settings.game_mode == GameMode.PVE and 
            self.current_player != self.settings.player_color):
            return

        # 计算棋子位置
        x, y = event.x, event.y
        row = round((y - 30) / 30)
        col = round((x - 30) / 30)
        
        if not self._make_move(row, col):
            return
        
        # 在PVE模式下，执行AI移动
        if self.settings.game_mode == GameMode.PVE and not self.game_over:
            self.root.after(500, self._ai_move)

    def _make_move(self, row: int, col: int) -> bool:
        """执行走棋"""
        if not (0 <= row < self.chess_board.size and 0 <= col < self.chess_board.size):
            return False
        
        if not self.chess_board.place_piece(row, col, self.current_player):
            return False
            
        if self.chess_board.check_win(row, col):
            self.game_over = True
            messagebox.showinfo("游戏结束", f"{self.current_player.value}获胜！")
            return True
            
        self.current_player = (Player.WHITE if self.current_player == Player.BLACK 
                             else Player.BLACK)
        return True

    def _ai_move(self) -> None:
        """AI走棋"""
        if self.ai and not self.game_over:
            move = self.ai.make_move()
            if move:
                row, col = move
                self._make_move(row, col)

    def run(self) -> None:
        """运行游戏"""
        self.root.mainloop()

if __name__ == "__main__":
    game = FiveInLine()
    game.run()