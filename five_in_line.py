# 用tkinter写一个五子棋小游戏

from enum import Enum
from typing import Optional, Tuple, List
import tkinter as tk
from tkinter import ttk

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
        self.game_mode: GameMode = GameMode.PVP
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
        pass

    def place_piece(self, row: int, col: int, player: Player) -> bool:
        """放置棋子"""
        pass

    def check_win(self, row: int, col: int) -> bool:
        """检查胜利"""
        pass

class FiveInLine:
    """五子棋游戏主类"""
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("五子棋")
        self.settings = GameSettings()
        self.current_player: Player = Player.BLACK
        self.chess_board: Optional[ChessBoard] = None
        self._init_ui()

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
        pass

    def _start_game(self) -> None:
        """开始新游戏"""
        pass

    def _handle_click(self, event: tk.Event) -> None:
        """处理鼠标点击事件"""
        pass

    def run(self) -> None:
        """运行游戏"""
        self.root.mainloop()

if __name__ == "__main__":
    game = FiveInLine()
    game.run()