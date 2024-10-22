import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# 设置游戏窗口
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 定义蛇和食物的大小
BLOCK_SIZE = 20

# 定义字体
font = pygame.font.SysFont(None, 36)

# 蛇类
class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = "RIGHT"
        self.grow_flag = False

    def move(self):
        x, y = self.body[0]
        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE
        self.body.insert(0, (x, y))
        
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(window, BLACK, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

# 食物类
class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)

    def draw(self):
        pygame.draw.rect(window, YELLOW, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# 游戏主循环
def game_loop():
    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        snake.move()

        # 检查是否吃到食物
        if snake.body[0] == food.position:
            snake.grow()
            food = Food()
            score += 1

        # 检查是否撞墙
        if (snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or
            snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT):
            game_over = True

        # 检查是否撞到自己
        if snake.body[0] in snake.body[1:]:
            game_over = True

        # 绘制游戏界面
        window.fill(WHITE)
        snake.draw()
        food.draw()

        # 绘制计分板
        score_text = font.render(f"Score: {score}", True, RED)
        window.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(10)  # 控制游戏速度

    pygame.quit()

# 运行游戏
if __name__ == "__main__":
    game_loop()
