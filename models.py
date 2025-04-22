import random
from constants import*

class Snake:
    def __init__(self,x,y):
        self.snake_body = [
            pygame.Rect(x*BLOCK_SIZE,y*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE),
        ]
        
        #初始化分数和方向
        self.dir = pygame.K_d
        self.score = 0
        
        #导入蛇头并缩放
        head_image = pygame.image.load("res/snake_head.png")
        self.snake_head_image = pygame.transform.scale(head_image,(BLOCK_SIZE,BLOCK_SIZE))
        
        #初始化蛇
        for _ in range(3):
            self.grow()
        
        #初始化分数
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

