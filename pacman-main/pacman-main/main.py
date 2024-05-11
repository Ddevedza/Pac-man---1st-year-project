import pygame, random, time

# _ passage (empty)
# # wall
# \$ ghost spawn point
# . pellet
# @ Pac-Man (starting point)

clock = pygame.time.Clock()
fps = 60

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

level = 1
max_levels = 5

# Sounds
intro_fx = pygame.mixer.Sound('resource/sound_intro.wav')
intro_fx.set_volume(0.3)
chomp1_fx = pygame.mixer.Sound('resource/sound_chomp2.wav')
chomp1_fx.set_volume(0.3)
chomp2_fx = pygame.mixer.Sound('resource/sound_chomp2.wav')
chomp2_fx.set_volume(0.3)
death_fx = pygame.mixer.Sound('resource/sound_death.wav')
death_fx.set_volume(0.3)

# Display
screen_width = 1000
screen_height = 1000
tile_size = 36

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pacman')
icon=pygame.image.load('resource/sprite_pacman_right1.png')
pygame.display.set_icon(icon)

font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

white = (255, 255, 255)
blue = (0, 0, 255)


# def draw_grid():
#     for line in range(0, 31):
#         pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
#         pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height)) #Map grid draw check

# game reset
def reset(level):
    world.player.reset(world.player_cordinates_list[0][0], world.player_cordinates_list[0][1])
    free_ghost_group.empty()
    coin_group.empty()

    with open(f'resource/level{level}.txt', "r") as file:
        world_data = file.readlines()
    world1 = World(world_data)

    return world1


# button purpose
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.click = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False

        screen.blit(self.image, self.rect)
        return action


# template for text creation
def draw(text, font, font_col, x, y):
    img = font.render(text, True, font_col)
    screen.blit(img, (x, y))


# get ready drawing text
def get_ready(seconds):
    intro_fx.play()
    img = font.render("Get ready!", True, "yellow")
    screen.fill("black")
    screen.blit(img, ((screen_width // 2) - 170, screen_height // 2 - 60))

    pygame.display.update()
    time.sleep(seconds)


# map
class World():
    def __init__(self, data):
        self.tile_list = []
        wall_img = pygame.image.load('resource/sprite_wall.png')
        wall_img1 = pygame.image.load('resource/sprite_wall2.png')
        self.player_cordinates_list = []

        self.player = ''

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == '#':
                    if level == 1 or level == 3:
                        img = pygame.transform.scale(wall_img, (tile_size, tile_size))
                    if level == 2 or level == 4:
                        img = pygame.transform.scale(wall_img1, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == '&':
                    free_ghost = Enemy(col_count * tile_size, row_count * tile_size + 2 + 3)
                    free_ghost_group.add(free_ghost)
                if tile == '.':
                    coin = Coin(col_count * tile_size, row_count * tile_size + 2)
                    coin_group.add(coin)
                if tile == '@':
                    self.player = Player(col_count * tile_size, (row_count * tile_size) + 3)
                    cordinates = (col_count * tile_size, (row_count * tile_size) + 3)
                    self.player_cordinates_list.append(cordinates)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


# player creation and functions
class Player():
    def __init__(self, x, y):
        self.reset(x, y)
        self.movement = "s" # still movement on startup


    # player functions
    def update(self, game_over):
        dx = 0
        dy = 0

        walk_cooldown = 5

        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.movement = -1

            if key[pygame.K_RIGHT]:
                self.movement = 1

            if key[pygame.K_UP]:
                self.movement = 2

            if key[pygame.K_DOWN]:
                self.movement = -2

            if key[pygame.K_LEFT]:
                self.movement = -1

            # keep the movement loop

            if self.movement == -1:
                dx -= 2
                self.counter += 1
                self.direction = -1

            if self.movement == 1:
                dx += 2
                self.counter += 1
                self.direction = 1

            if self.movement == 2:
                dy -= 2
                self.counter += 1
                self.direction = 2


            if self.movement == -2:
                dy += 2
                self.counter += 1
                self.direction = -2


            movementtimer = 1
            if movementtimer % 2 == 0:
                movementtimer += 1
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                    if self.index == 1:
                        chomp1_fx.play()
                    if self.index == 3:
                        chomp2_fx.play()
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 2:
                    self.image = self.images_up[self.index]
                if self.direction == -2:
                    self.image = self.images_down[self.index]
                if movementtimer >= 100:
                    movementtimer = 0

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index == 1:
                    chomp1_fx.play()
                if self.index == 3:
                    chomp2_fx.play()
                if self.index >= len(self.images_right):
                    self.index = 0

                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 2:
                    self.image = self.images_up[self.index]
                if self.direction == -2:
                    self.image = self.images_down[self.index]

            # check for collision
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dy = 0

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0

            if pygame.sprite.spritecollide(world.player, free_ghost_group, False):
                game_over = -1
                death_fx.play()

        # draw player onto screen
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2) #Player grid draw check

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_up = []
        self.images_down = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_right = pygame.image.load(f'resource/sprite_pacman_right{num}.png')
            img_right = pygame.transform.scale(img_right, (tile_size - 10, tile_size - 10))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 4):
            img_down = pygame.image.load(f'resource/sprite_pacman_down{num}.png')
            img_down = pygame.transform.scale(img_down, (tile_size - 5, tile_size - 5))
            img_up = pygame.transform.rotate(img_down, 180)
            self.images_down.append(img_down)
            self.images_up.append(img_up)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = 0


# enemy definiton and movement
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        num = random.randint(1, 4)
        img = pygame.image.load(f'resource/sprite_ghost_{num}_down1.png')
        self.image = pygame.transform.scale(img, (tile_size - 10, tile_size - 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        dx = 0
        dy = 0

        if self.rect.x < world.player.rect.x:
            dx += 2
        elif self.rect.x > world.player.rect.x:
            dx -= 2
        if self.rect.y < world.player.rect.y:
            dy += 2
        elif self.rect.y > world.player.rect.y:
            dy -= 2

        for tile in world.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0

        self.rect.x += dx
        self.rect.y += dy


# coins/pellet/score
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f'resource/sprite_pellet.png')
        self.image = pygame.transform.scale(img, (tile_size - 5, tile_size - 5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# button image load
button_img = pygame.image.load('resource/restart_btn.png')
start_img = pygame.image.load('resource/start_btn.png')
exit_img = pygame.image.load('resource/exit_btn.png')

# button image creation
reset_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, button_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

if __name__ == '__main__':

    # sprite group creator
    free_ghost_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()

    # txt map opener
    with open(f'resource/level{level}.txt', "r") as file:
        world_data = (file.readlines())

    world = World(world_data)

    score = 0
    player_score = 0
    game_over = 0

    main_menu = True

    run = True
    while run:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # main menu
        if main_menu == True:
            if start_button.draw():
                get_ready(4)
                main_menu = False

            if exit_button.draw():
                run = False

        if main_menu == False:
            if game_over == 0:
                free_ghost_group.update()
                if pygame.sprite.spritecollide(world.player, coin_group, True):
                    score += 1
                    player_score += 1
                draw('Score: ' + str(player_score), font_score, white, tile_size - 10, 10)
                if world.player.rect == (970, 513, 26, 26) or world.player.rect == (
                970, 504, 26, 26) or world.player.rect == (
                        970, 512, 26, 26) or world.player.rect == (970, 511, 26, 26) or world.player.rect == (
                        970, 510, 26, 26) or world.player.rect == (970, 509, 26, 26) or world.player.rect == (
                        970, 508, 26, 26) or world.player.rect == (970, 507, 26, 26) or world.player.rect == (
                        970, 506, 26, 26) or world.player.rect == (970, 505, 26, 26) or world.player.rect == (
                970, 514, 26, 26):
                    world.player.reset(38, 508)
                elif world.player.rect == (38, 513, 26, 26) or world.player.rect == (
                        38, 512, 26, 26) or world.player.rect == (38, 511, 26, 26) or world.player.rect == (
                        38, 510, 26, 26) or world.player.rect == (
                        38, 509, 26, 26) or world.player.rect == (38, 508, 26, 26) or world.player.rect == (
                        38, 507, 26, 26) or world.player.rect == (38, 506, 26, 26) or world.player.rect == (
                        38, 505, 26, 26) or world.player.rect == (38, 514, 26, 26) or world.player.rect == (
                38, 504, 26, 26):
                    world.player.reset(970, 508)
                if world.player.rect == (504, 974, 26, 26) or world.player.rect == (
                        505, 974, 26, 26) or world.player.rect == (506, 974, 26, 26) or world.player.rect == (
                        507, 974, 26, 26) or world.player.rect == (508, 974, 26, 26) or world.player.rect == (
                        508, 974, 26, 26) or world.player.rect == (509, 974, 26, 26) or world.player.rect == (
                        510, 974, 26, 26) or world.player.rect == (511, 974, 26, 26) or world.player.rect == (
                        512, 974, 26, 26) or world.player.rect == (513, 974, 26, 26) or world.player.rect == (
                514, 974, 26, 26):
                    world.player.reset(508, 11)
                elif world.player.rect == (508, 11, 26, 26) or world.player.rect == (
                        507, 11, 26, 26) or world.player.rect == (506, 11, 26, 26) or world.player.rect == (
                        505, 11, 26, 26) or world.player.rect == (504, 11, 26, 26) or world.player.rect == (
                        508, 11, 26, 26) or world.player.rect == (509, 11, 26, 26) or world.player.rect == (
                        510, 11, 26, 26) or world.player.rect == (511, 11, 26, 26) or world.player.rect == (
                        512, 11, 26, 26) or world.player.rect == (513, 11, 26, 26) or world.player.rect == (
                514, 11, 26, 26):
                    world.player.reset(508, 974)
                if level == 1 or level == 3:
                    if score == 109:
                        game_over = 1
                if level == 2 or level == 4:
                    if score == 129:
                        game_over = 1

            coin_group.draw(screen)
            free_ghost_group.draw(screen)
            world.draw()
            # death
            if game_over == -1:

                draw('GAME OVER!', font, blue, (screen_width // 2) - 170, screen_height // 2)
                if reset_button.draw() == True:
                    world.player.reset(world.player_cordinates_list[0][0], world.player_cordinates_list[0][1])
                    world = reset(level)
                    game_over = 0
                    score = 0
                    player_score = 0
                    get_ready(4)
            # level or game win
            if game_over == 1:
                level += 1
                if level >= max_levels:
                    draw('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
                    if reset_button.draw() == True:
                        level = 1
                        world = reset(level)
                        game_over = 0
                        score = 0
                        get_ready(4)
                else:
                    world = reset(level)
                    game_over = 0
                    score = 0

            game_over = world.player.update(game_over)

        # fps clock
        clock.tick(fps)
        pygame.display.update()
