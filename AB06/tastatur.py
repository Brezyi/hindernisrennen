import os
import pygame
import time

class Settings:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")

class Player:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 40))  
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.start_x = (Settings.WINDOW_WIDTH - self.width) // 2
        self.start_y = Settings.WINDOW_HEIGHT - self.height
        self.x = self.start_x
        self.y = self.start_y
        self.speed = 3
        self.base_speed = self.speed 
        self.boost_active = False
        self.boost_start_time = 0
        self.boost_duration = 2  
        self.boost_used_in_round = False  

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        self.x = max(0, min(Settings.WINDOW_WIDTH - self.width, self.x))
        self.y = max(0, min(Settings.WINDOW_HEIGHT - self.height, self.y))

    def activate_boost(self):
        if not self.boost_active and not self.boost_used_in_round: 
            self.boost_active = True
            self.boost_start_time = time.time()
            self.speed = self.base_speed * 2 
            self.boost_used_in_round = True 

    def update_boost(self):
        if self.boost_active and time.time() - self.boost_start_time >= self.boost_duration:
            self.boost_active = False
            self.speed = self.base_speed  

    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.speed = self.base_speed  
        self.boost_active = False

    def reset_for_new_round(self):
        self.reset_position()
        self.boost_used_in_round = False  

class MovingObstacle:
    def __init__(self, image_path, x, y, speed_x, speed_y, size):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < -self.width:
            self.x = Settings.WINDOW_WIDTH
        elif self.x > Settings.WINDOW_WIDTH:
            self.x = -self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, player):
        return self.x < player.x + player.width and self.x + self.width > player.x and self.y < player.y + player.height and self.y + self.height > player.y

def increase_obstacle_speed(obstacles):
    for obstacle in obstacles:
        if obstacle.speed_x != 0: 
            obstacle.speed_x += 1 if obstacle.speed_x > 0 else -1  
        if obstacle.speed_y != 0:  
            obstacle.speed_y += 1 if obstacle.speed_y > 0 else -1

def draw_dark_overlay(screen):
    overlay = pygame.Surface((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))  
    overlay.set_alpha(150)  
    overlay.fill((0, 0, 0))  
    screen.blit(overlay, (0, 0))  

def display_score(screen, score):
    font = pygame.font.Font(None, 36)  
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  
    screen.blit(score_text, (10, 10)) 

def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Spiel ohne Hindernisse")
    clock = pygame.time.Clock()

    obstacles = [
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "toyota.png"), 250, 55, 3, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "toyota.png"), -350, 55, 3, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "toyota.png"), 550, 55, 3, 0, (60, 50)),     
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "LKW.png"), 600, 230, -4, 0, (80, 80)),  
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "Mclaren.png"), 200, 250, -4, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "toyota.png"), 400, 485, 4, 0, (60, 50)), 
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "Mclaren.png"), 830, 125, -8, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "Audi.png"), 350, 112, -8, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "Audi.png"), 450, 175, -6, 0, (60, 50)),  
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "Audi.png"), 700, 670, -6, 0, (60, 50)), 
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "Audi.png"), 450, 670, -6, 0, (60, 50)), 
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "Mclaren.png"), 200, 560, -4, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "LKW.png"), 600, 540, -4, 0, (80, 80)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "toyota.png"), -350, 610, 5, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "toyota.png"), 300, 610, 5, 0, (60, 50)),
    ]

    background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "background.png")).convert()
    background_image = pygame.transform.scale(background_image, (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    player = Player(os.path.join(Settings.IMAGE_PATH, "frogger.png"))

    paused = False
    running = True
    esc_last_pressed = 0
    score = 0  

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    now = time.time()
                    if now - esc_last_pressed < 0.5:
                        running = False
                    esc_last_pressed = now
                elif event.key == pygame.K_SPACE:  
                    player.activate_boost()

        screen.blit(background_image, (0, 0))
        
        if not paused:
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.update_boost() 
            player.draw(screen)

            if player.y <= 0:  
                player.reset_for_new_round()  
                score += 10  
                increase_obstacle_speed(obstacles)
                print("Neue Runde!")

            for obstacle in obstacles:
                obstacle.move()
                obstacle.draw(screen)

                if obstacle.check_collision(player):
                    print("Kollision!")
                    player.reset_position()

            display_score(screen, score)
        else:
            draw_dark_overlay(screen)
        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
