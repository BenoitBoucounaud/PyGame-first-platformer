import pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 00)
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

class Level():
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.world_shift = 0
    
    # Tiens à jour les sprites
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    # Engendre les sprites
    def draw(self, screen):
        screen.fill(BLUE)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        # World shift est la variable responsable de l'ampleur des mouvements que nous autorisons ici
        self.world_shift += shift_x
        for platform in self.platform_list:
            platform.rect.x +=shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

class levelGreenHill(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = - 1000
        level = [
            [200, 50, 500, 500],
            [200, 50, 800, 400],
            [200, 50, 1000, 500],
            [200, 50, 1100, 300],
            [200, 50, 1500, 500],
            [200, 50, 1800, 400]            
        ]
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class levelMarble(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = - 1000
        level = [
            [200, 50, 400, 400],
            [200, 50, 800, 500],
            [200, 50, 900, 400],
            [200, 50, 1200, 400],
            [200, 50, 1400, 400],
            [200, 50, 1900, 500]            
        ]
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = 50
        height = 50
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.level = None
    
    def update(self):
        self.calc_grav()
        
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0 :
                self.rect.right = block.rect.left
            elif self.change_x < 0 :
                self.rect.left = block.rect.right
        
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0 :
                self.rect.bottom = block.rect.top
            elif self.change_y < 0 :
                self.rect.top = block.rect.bottom
            self.change_y = 0
    
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else :
            self.change_y += 0.35
        
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
    
    def go_left(self):
        self.change_x = -5

    def go_right(self):
        self.change_x = 5

    def stop(self):
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

def main():
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Side-scrolling Platformer")
    player = Player()
    
    level_list = []
    level_list.append(levelGreenHill(player))
    level_list.append(levelMarble(player))

    current_level_no = 0
    current_level = level_list[current_level_no]
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Met le jeu en boucle permanante jusqu a ce qu on abandonne
    done = False
    # Assure le bon déroulement du jeu (vitesse du jeu)
    clock = pygame.time.Clock()

    while not done :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0 :
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0 :
                    player.stop()
        active_sprite_list.update()
        current_level.update()

        if player.rect.right >=500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit: 
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
        
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        clock.tick(60)
        pygame.display.flip()
        # Abandon : pygame.quit()

if __name__ == "__main__":
    main()
