import game
"""
    贪吃蛇游戏
    1.准备pygame开发环境:窗口尺寸,标题,图标
        a.准备背景,蛇头
    
    2.while True:
        a.处理用户输入事件
        b.处理游戏逻辑
        c.渲染图画
        d.控制fps
    游戏逻辑:
    1.根据用户输入方向改变移动方向并移动
    2.遇到食物,蛇身长一节
    3.碰到自己或墙壁,游戏结束
    4.全部吃完,结束游戏
"""

if __name__ == '__main__':
    snake_game = game.Game()
    snake_game.start()
