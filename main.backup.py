import pygame
import random

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

#屏幕大小
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

#颜色
COLOR_GREY = (150,150,150)
COLOR_WHITE = (255,255,255)
COLOR_BLUE = (0,0,200)
COLOR_RED = (255,0,0)

#网格大小
BLOCK_SIZE = 20

#移动方向字典
DIRECTION_LIST = {
    pygame.K_w:(0,-BLOCK_SIZE),
    pygame.K_s:(0,BLOCK_SIZE),
    pygame.K_a:(-BLOCK_SIZE,0),
    pygame.K_d:(BLOCK_SIZE,0),
}

#方向元组
LR = (pygame.K_a,pygame.K_d)
UD = (pygame.K_w,pygame.K_s)

#旋转方向字典
HEAD_DICT = {
    pygame.K_w:180,
    pygame.K_s:0,
    pygame.K_a:270,
    pygame.K_d:90,
}

class Snake:
    def __init__(self,x,y):
        self.snake_body = [
            pygame.Rect(x*BLOCK_SIZE,y*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE),
        ]
        
        self.dir = pygame.K_d
        self.score = 0
        
        #导入蛇头并缩放
        head_image = pygame.image.load("res/snake_head.png")
        self.snake_head_image = pygame.transform.scale(head_image,(BLOCK_SIZE,BLOCK_SIZE))
        
        for _ in range(3):
            self.grow()
            
        self.score = 0
        
    def draw(self,screen): 
        #渲染蛇身 
        for node in self.snake_body[1:]:
            pygame.draw.rect(screen,COLOR_WHITE,node,border_radius=3)
        
        #渲染蛇头
        head = self.snake_body[0]
        head_image = pygame.transform.rotate(self.snake_head_image,HEAD_DICT[self.dir])
        screen.blit(head_image,(head.x,head.y))

    #判断方向是否可用
    def is_direction_enable(self,input_key):
        #不能左右掉头
        if self.dir in LR and input_key in LR:
            return False
              
        #不能上下掉头
        if self.dir in UD and input_key in UD:
            return False

        #不是W,S,A,D
        if input_key not in [pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s]:
            return False
        return True
    
    #更新运动方向
    def update_direction(self,new_dir):
        #符合条件
        self.dir = new_dir
    
    #让蛇运动    
    def move(self):
        """
        移动之前根据用户输入修改移动方向
        让蛇向前移动一格
        """
        #蛇头复制一份
        new_node = self.snake_body[0].copy()
        
        #往前进方向移动一格       
        new_move = DIRECTION_LIST[self.dir]
        new_node.x += new_move[0]
        new_node.y += new_move[1]
        
        #如果超出范围，瞬移
        if new_node.x >= SCREEN_WIDTH:
            new_node.x -= SCREEN_WIDTH
        elif new_node.x < 0:
            new_node.x += SCREEN_WIDTH
        if new_node.y >= SCREEN_HEIGHT:
            new_node.y -= SCREEN_HEIGHT
        elif new_node.y < 0:
            new_node.y += SCREEN_HEIGHT
        
        #把新的蛇头放到最前面
        self.snake_body.insert(0,new_node)
        
        #删除蛇尾
        self.snake_body.pop()
        
    #张一节,蛇尾复制一份追加到最后
    def grow(self):
        snake_tail = self.snake_body[-1].copy()
        self.snake_body.append(snake_tail)
        self.score += 1  
    
class Food:
    def __init__(self,node):
        self.node = node
        
    @staticmethod
    #根据屏幕宽高和蛇的信息生成新的食物
    def gen_doof_position(snake:Snake):
        while True:
            x = random.randint(0,SCREEN_WIDTH//BLOCK_SIZE - 1)
            y = random.randint(0,SCREEN_HEIGHT//BLOCK_SIZE - 1)
            new_food_node = pygame.Rect(x*BLOCK_SIZE,y*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE)
            #新的食物不在蛇身上，返回食物
            if new_food_node not in snake.snake_body: 
                return new_food_node
    
        #渲染食物
    def draw(self,screen):
        pygame.draw.rect(screen,COLOR_BLUE,self.node,border_radius=3)

class Game:
    def __init__(self):
        pygame.init()
        
        #设置窗体大小，获取surface
        self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH,SCREEN_HEIGHT))

        #设置标题
        pygame.display.set_caption("贪吃蛇大战v1.0")

        #设置图标
        self.icon = pygame.image.load("res/icon.jpg")

        #加载背景图(缩放)
        self.bg_image = pygame.image.load("res/background.jpg")
        pygame.transform.scale(self.bg_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
        
        #判断是否游戏结束
        self.is_game_over = False

    def start(self):
        #clock
        clock = pygame.time.Clock()

        #创建蛇
        snake = Snake(5,3)

        #创建食物
        food = Food(Food.gen_doof_position(snake))
        while True:
            #a.处理事件，获取用户的输入事件
            event_list = pygame.event.get()
            new_dir = None
            #解析处理所有事件
            #event.type 保存用户输入的事件类型：鼠标，按键
            #event.key 保存用户按下或抬起的键
            for event in event_list:
                if event.type == pygame.QUIT:
                    #退出游戏
                    self.quit_game()
                    
                elif event.type == pygame.KEYDOWN:
                    #游戏结束，按键判断
                    if self.is_game_over:
                        if event.key == pygame.K_q:
                            self.quit_game()
                        elif event.key == pygame.K_SPACE:
                            snake = Snake()
                            food = Food(Food.gen_doof_position(snake))
                            self.is_game_over = False
                    #W,A,S,D,ESCAPE
                    elif event.key == pygame.K_ESCAPE:
                        self.quit_game()
                    elif snake.is_direction_enable(event.key):
                        new_dir = event.key
            
            if new_dir is not None:
                snake.update_direction(new_dir)
                           
            if not self.is_game_over:
                #b.处理游戏逻辑
                #蛇移动
                snake.move()
                
                #蛇头
                snake_head = snake.snake_body[0]
                
                #遇到食物，吃掉，蛇长一节
                if snake_head == food.node:
                    food = Food(Food.gen_doof_position(snake))
                    snake.grow()
                    
                #碰到墙壁
                if snake_head.x < 0 or snake_head.x >= SCREEN_WIDTH \
                    or snake_head.y < 0 or snake_head.y >= SCREEN_HEIGHT:
                        self.is_game_over = True
                
                #碰到自己
                if snake_head in snake.snake_body[1:]:
                    self.is_game_over = True
                    
                #c.渲染界面
                # 背景图
                self.screen.blit(self.bg_image,(0,0))
                
                #网格线
                #绘制所有横线
                for y in range(0,480,BLOCK_SIZE):
                    start = (0,y)
                    end = (SCREEN_WIDTH,y)
                    pygame.draw.line(self.screen,COLOR_GREY,start,end)
                #绘制所有竖线
                for x in range(0,640,BLOCK_SIZE):
                    start = (x,0)
                    end = (x,SCREEN_HEIGHT)
                    pygame.draw.line(self.screen,COLOR_GREY,start,end)
                    
                #绘制蛇
                snake.draw(self.screen)
                
                #绘制食物
                food.draw(self.screen)
                
                #绘制得分和fps
                fps = clock.get_fps()
                self.show_text("FPS:{:.2f}".format(fps),20,SCREEN_WIDTH - 100,10)
                score = snake.score
                self.show_text("得分:{}".format(snake.score),20,10,10)
                
                #根据游戏是否结束，渲染文字
                if self.is_game_over:
                    self.show_text("游戏结束",50,SCREEN_WIDTH // 4,SCREEN_HEIGHT // 4)
                    self.show_text("得分:{}".format(snake.score),24,SCREEN_WIDTH // 4,SCREEN_HEIGHT // 4 + 60)
                    self.show_text("按【空格键】重新开始",24,SCREEN_WIDTH // 4,SCREEN_HEIGHT // 4 + 90)
                    self.show_text("按【Q】退出游戏",24,SCREEN_WIDTH // 4,SCREEN_HEIGHT // 4 + 120)
                    
                # 执行最终渲染
                pygame.display.update()         
                
                #设定fps
                clock.tick(10 + snake.score * 0.2) 

    def quit_game(self):
        pygame.display.quit()
        exit(0)  
                 
    #游戏是否结束,渲染文字            
    def show_text(self,text,font_size,x,y):
        font = pygame.font.SysFont("Simhei",font_size)
        text = font.render(text,True,COLOR_RED)
        self.screen.blit(text,(x,y))
        
g = Game()
g.start()