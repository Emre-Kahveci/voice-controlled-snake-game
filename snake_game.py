import pygame
import sys
import random
import threading
from speech_to_text import SpeechToText

# Ekran Boyutları
WIDTH, HEIGHT = 800, 600

# Yılan Boyutları
SNAKE_SIZE = 3
SNAKE_BLOCK_SIZE = 20
GAME_SPEED = 3

# Renkler
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Yönler
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        pygame.init() # Pygame başlatma
        self.init_display() # Ekranı başlatma

        self.mic = SpeechToText() # Sesi metne dönüştürme nesnesi oluşturma

        self.snake = [(WIDTH // 2, HEIGHT // 2)] # Yılanın başlangıç pozisyonu
        self.direction = RIGHT
        self.food = self.generate_food() # İlk yemi oluşturma

    def init_display(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Ekranı oluşturma
        pygame.display.set_caption("Snake Game") # Ekran başlığını ayarlama
        self.clock = pygame.time.Clock() # Oyun hızını ayarlama

    def generate_food(self): # Yemi rastgele konuma yerleştirme
        food_x = random.randrange(0, WIDTH // SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        food_y = random.randrange(0, HEIGHT // SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        return food_x, food_y # Yemin konumunu döndürme

    def run(self):
        voice_thread = threading.Thread(target=self.listen_voice_commands) # Ses komutlarını dinleme işlemini başlatma
        voice_thread.start()

        while True:
            self.handle_events() # Olayları kontrol etme
            self.move() # Yılanı hareket ettirme
            self.check_collision() # Çarpışmayı kontrol etme
            self.check_food() # Yemi kontrol etme
            self.adjust_snake_position() # Ekranın dışına çıkan yılanı düzeltme
            self.update_display() # Ekranı güncelleme

    def listen_voice_commands(self):
        while True:
            direction = self.mic.listen_command() # Sesli komutlardan yön alma
            self.update_direction(direction) # Yönü güncelleme

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

    def move(self):
        head = self.snake[0] # Yılanın başını al
        new_head = (head[0] + self.direction[0] * SNAKE_BLOCK_SIZE, head[1] + self.direction[1] * SNAKE_BLOCK_SIZE) # Yılanın yeni baş pozisyonunu hesapla
        self.snake.insert(0, new_head) # Yılanın başını yeni pozisyona ekle
        if len(self.snake) > SNAKE_SIZE: # Yılanın yeni boyutu, yılan boyutundan büyükse
            self.snake.pop() # Yılanın kuyruğunu kes

    def adjust_snake_position(self): 
        head = self.snake[0] # Yılanın başını al
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT: # Yılanın başı ekranın dışına çıkmışsa
            self.wrap_around_screen() # Yılanı ekranın içine al

    def wrap_around_screen(self):
        head = self.snake[0] # Yılanın başını al
        self.snake[0] = (head[0] % WIDTH, head[1] % HEIGHT) # Yılanın başını ekranın karşısına al

    def check_collision(self): 
        head = self.snake[0] # Yılanın başını al
        if head in self.snake[1:]: # Yılanın başı yılana çarpmışsa
            self.quit_game() # Oyunu bitir

    def check_food(self):
        head = self.snake[0] # Yılanın başını al
        if head == self.food: # Yılanın başı yeme çarpmışsa
            self.food = self.generate_food() # Yeni yem oluştur
            self.snake.append((0, 0)) # Yılanı büyüt

    def update_direction(self, direction):
        if direction == 1 and self.direction != DOWN: # Komut 1'se ve yılan aşağı gitmiyorsa
            self.direction = UP
        elif direction == 2 and self.direction != UP: # Komut 2'yse ve yılan yukarı gitmiyorsa
            self.direction = DOWN
        elif direction == 3 and self.direction != RIGHT: # Komut 3'se ve yılan sağa gitmiyorsa
            self.direction = LEFT
        elif direction == 4 and self.direction != LEFT: # Komut 4'se ve yılan sola gitmiyorsa
            self.direction = RIGHT

    def update_display(self):
        self.screen.fill(GREY) # Ekranı gri renge boyama
        self.draw_snake() # Yılanı çizme
        self.draw_food() # Yemi çizme
        pygame.display.flip() # Ekranı güncelleme
        self.clock.tick(GAME_SPEED) # Oyun hızını ayarlama

    def draw_snake(self):
        for i, segment in enumerate(self.snake):
            pygame.draw.rect(self.screen, BLACK, (segment[0], segment[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))  # Yılanın karesini siyah ile çizme
            pygame.draw.rect(self.screen, GREEN, (segment[0] + 2, segment[1] + 2, SNAKE_BLOCK_SIZE - 4, SNAKE_BLOCK_SIZE - 4))  # Yılanın içini yeşil ile çizme

            # Yılanın başındaysak
            if i == 0:
                eye = (segment[0] + SNAKE_BLOCK_SIZE - 10, segment[1] + 5)
                pygame.draw.circle(self.screen, YELLOW, eye, 3) # Yılanın gözünü çizme

                # Yılanın gittiği yöne dil çizgi çizme
                direction_line_start = (segment[0] + SNAKE_BLOCK_SIZE // 2, segment[1] + SNAKE_BLOCK_SIZE // 2) # Yılanın başının orta noktası
                direction_line_end = (segment[0] + SNAKE_BLOCK_SIZE // 2 + self.direction[0] * SNAKE_BLOCK_SIZE // 1.5, segment[1] + SNAKE_BLOCK_SIZE // 2 + self.direction[1] * SNAKE_BLOCK_SIZE // 1.5) # Yılanın başının orta noktasından yönün gideceği noktaya doğru çizgi
                pygame.draw.line(self.screen, RED, direction_line_start, direction_line_end, 3) # Çizgiyi çizme

    def draw_food(self):
        pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))  # Yemi çizme
        pygame.draw.rect(self.screen, BLACK, (self.food[0], self.food[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE), 2) # Yemeğin etrafına siyah çizgi çizme


    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()