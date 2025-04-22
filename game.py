from constants import*
from models import*

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
        