import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption("躲避游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 小球属性
ball_size = 50
ball_x = screen_width // 2
ball_y = screen_height - ball_size
ball_speed = 5

# 障碍物属性
obstacle_width = 100
obstacle_height = 20
obstacle_x = random.randint(0, screen_width - obstacle_width)
obstacle_y = -obstacle_height
obstacle_speed = 5

# 游戏状态
running = True
clock = pygame.time.Clock()

# 主循环
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取按键状态
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ball_x > 0:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT] and ball_x < screen_width - ball_size:
        ball_x += ball_speed

    # 更新障碍物位置
    obstacle_y += obstacle_speed
    if obstacle_y > screen_height:
        obstacle_y = -obstacle_height
        obstacle_x = random.randint(0, screen_width - obstacle_width)

    # 检查碰撞
    if (ball_x < obstacle_x + obstacle_width and
        ball_x + ball_size > obstacle_x and
        ball_y < obstacle_y + obstacle_height and
        ball_y + ball_size > obstacle_y):
        running = False

    # 绘制背景
    screen.fill(WHITE)

    # 绘制小球
    pygame.draw.circle(screen, BLACK, (ball_x + ball_size // 2, ball_y + ball_size // 2), ball_size // 2)

    # 绘制障碍物
    pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 结束游戏
pygame.quit()
print("游戏结束！")