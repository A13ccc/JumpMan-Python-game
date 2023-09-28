#import libraries
import pygame.freetype
import pygame.mixer
import random
import pygame


#initialise pygame
pygame.init()


#game window dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


#create game winodw
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jump Man v0.4')


#set frame rate
clock = pygame.time.Clock()
FPS = 90


#game vars
JUMP_VELOCITY = -24
GRAVITY = 2
MAX_PLATFORMS = 10
SCROLL_THRESH = 200
scroll = 0
bg_scroll = 0
game_over = False
score = 0
score1 = 0
hscore = 0
hsx = 300
fade_counter = 0
paused = False
sx = 40
hsx1 = 40
music_paused = False
check_click = False
crossed_high_score = False
last_player_position = None
on_settings_page = False






#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (0, 0, 0)
PURPLE = (35, 11, 77)

#define font
title_font_path = 'assets/font/SedgwickAveDisplay-Regular.ttf'
font_small_path = 'assets/font/Quicksand-Medium.ttf'
font_big_path = 'assets/font/Quicksand-Medium.ttf'
font_small = pygame.font.Font(font_small_path, 14)
font_big = pygame.font.Font(font_big_path, 24)
font_huge = pygame.font.Font(font_big_path, 34)
font_gyatt = pygame.font.Font(font_big_path, 50)
title_font_huge = pygame.font.Font(title_font_path, 85)


# Initialize mixer
pygame.mixer.init()


# Load song
music_file = "assets/music/bedtime-after-coffee.mp3"
pygame.mixer.music.load(music_file)


# Set volume (increase if necessary)
pygame.mixer.music.set_volume(0.7)  # 1.0 means 100% volume


# Set the music end event
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)


# Play music
pygame.mixer.music.play()


#load images
player_image = pygame.image.load('assets/player.png').convert_alpha()
bg_image = pygame.image.load('assets/bg.png').convert_alpha()
platform_image = pygame.image.load('assets/platform.png').convert_alpha()
pause_button_image = pygame.image.load('assets/pause.png').convert_alpha()
play_button_image = pygame.image.load('assets/play.png').convert_alpha()
restart_button_image = pygame.image.load('assets/restart.png').convert_alpha()
city_image = pygame.image.load('assets/city.png').convert_alpha()
start_button_image = pygame.image.load('assets/startbutton.png').convert_alpha()
target_image = pygame.image.load('assets/fade.png').convert_alpha()


#screen text function
def draw_text(text, font, text_col, x, y):
   img = font.render(text, True, text_col)
   screen.blit(img, (x, y))


#info panel function
def draw_panel():
   pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 20))
   pygame.draw.line(screen, WHITE, (0,20), (SCREEN_WIDTH, 20), 2)
   draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 3)
   draw_text('HIGHSCORE: ' + str(hscore), font_small, WHITE, hsx, 3)


def draw_city():
   screen.blit(city_image, (0, 0))


#function backgroung
def draw_bg(bg_scroll):


#draw background
   screen.blit(bg_image, (0, 0 + bg_scroll))
   screen.blit(bg_image, (0, -600 + bg_scroll))


#player class
class Player():
   def __init__(self, x, y):
       self.image = pygame.transform.scale(player_image, (40, 68))
       self.width = 30
       self.height = 70
       self.rect = pygame.Rect(0, 0, self.width, self.height)
       self.rect.center = (x, y)
       self.vel_y = 0
       self.flip = True
  
   def move(self):
        # Reset variables
        scroll = 0
        dx = 0
        dy = 0

        # Process key presses
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            dx = -13
            self.flip = False
        if keys[pygame.K_RIGHT]:
            dx = 13
            self.flip = True

        if keys[pygame.K_UP] and not self.is_jumping:
            self.vel_y = JUMP_VELOCITY
            self.is_jumping = True

        # Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Don't go off the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # Collision with platforms
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        dy = 0
                        self.is_jumping = False

        # Check if player is near the top of the screen
        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -dy

        # Update rect position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

      
  
   def draw(self):
       screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 5, self.rect.y + 25))




#platform class
class Platform(pygame.sprite.Sprite):
   def __init__(self, x, y, width) :
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.transform.scale(platform_image, (width, 60))
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y


   def update(self, scroll):
       self.rect.y += scroll


       #check if platform has gone off screen
       if self.rect.top > SCREEN_HEIGHT:
           self.kill()


#player instance
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)


#create sprite groups
platform_group = pygame.sprite.Group()


#create starting plat
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)


def draw_restart_button():
   screen.blit(pygame.transform.scale(restart_button_image, (75, 75)), (165, 450))




def draw_settings_page():
   screen.fill(PURPLE)  # Fill the screen with the background color


   # Display settings title
   draw_text("Settings", font_huge, WHITE, 20, 20)


   # Display settings options
   draw_text("Music:", font_big, WHITE, 50, 100)
   draw_text("Sound Effects:", font_big, WHITE, 50, 150)


   # Display toggle buttons for music and sound effects
   # You can use rectangles or images to represent buttons
   # For example:
   # pygame.draw.rect(screen, WHITE, (200, 100, 50, 30))  # Music toggle button
   # pygame.draw.rect(screen, WHITE, (200, 150, 50, 30))  # Sound effects toggle button


   # Display a back button to return to the game
   draw_text("Back", font_big, WHITE, 20, 500)






#start screen background
def draw_start_bg():
   pygame.draw.rect(screen, PURPLE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


#def clickable area
image_x = 165
image_y = 450
image_width = 75
image_height = 75
image_width2 = 90
image_height2 = 90
clickable_rect = pygame.Rect(image_x, image_y, image_width, image_height)
clickable_rect2 = pygame.Rect(image_x, image_y, image_width2, image_height2)
start_fade_alpha = 255


def draw_start_button():
   screen.blit(pygame.transform.scale(start_button_image, (90, 90)), (165, 450))




def draw_music_button():
   if music_paused:
       # If music is paused, display the play button
       screen.blit(pygame.transform.scale(play_button_image, (30, 30)), (185, -5))
   else:
       # If music is playing, display the pause button
       screen.blit(pygame.transform.scale(pause_button_image, (30, 30)), (185, -5))


def start_fade_out(start_color):
   start_fade_alpha = 0
   fading_to_black = False


   while start_fade_alpha <= 255:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()


       if fading_to_black:
           screen.fill(BLACK)  # Fill the screen with black
       else:
           screen.fill(start_color)  # Fill the screen with the starting color


       start_fade_alpha += 2  # Increase alpha by 2 (adjust the value as needed)


       # Create a surface with the current alpha value
       fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
       fade_surface.set_alpha(start_fade_alpha)
       screen.blit(fade_surface, (0, 0))


       pygame.display.flip()
       clock.tick(FPS)


       # Check if we should transition to fading into black
       if start_fade_alpha >= 255:
           fading_to_black = True


# Usage example








#start screen loop
start = True
while start:
   draw_start_bg()
   draw_start_button()
   draw_text("A13c's:", font_big, WHITE, 30, 90)
   draw_text("Jump Man", title_font_huge, WHITE, 35, 130)
  
  
  
  
  
  
  
   for event in pygame.event.get():
       if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
           # Check if the left mouse button was clicked
           mouse_x, mouse_y = pygame.mouse.get_pos()
           print(f"Mouse Click Position: ({mouse_x}, {mouse_y})")
           print(f"Clickable Rect: {clickable_rect}")
           if clickable_rect.collidepoint(mouse_x, mouse_y):
               start = False
               start_fade_out(PURPLE)


# Now, you can enter the game loop


       if event.type == pygame.QUIT:
           pygame.quit()
   key = pygame.key.get_pressed()
   if key[pygame.K_ESCAPE]:
       pygame.quit()


   #update display window
   pygame.display.update()






#game loop
run = True
while run:


   clock.tick(FPS)


   if not paused:
       clock.tick(FPS)

       if game_over == False :
          
           clock.tick(FPS)

           #move player
           scroll = player.move()

          
           #draw bg
           bg_scroll += scroll
           if bg_scroll >= 600:
               bg_scroll = 0
           draw_bg(bg_scroll)


           #draw city
           draw_city()
          
           #platform gen
           if len(platform_group) < MAX_PLATFORMS:
               p_w = random.randint(40, 60)
               p_x = random.randint(0, SCREEN_WIDTH - p_w)
               p_y = platform.rect.y - random.randint(80, 120)
               platform = Platform(p_x, p_y, p_w)
               platform_group.add(platform)


          
           #update plats
           platform_group.update(scroll)
          
           #update score
           if scroll > 0:
               score += scroll
          
           #highscore
           if score > hscore:
               hscore = score


          
           #hide cursor
           pygame.mouse.set_visible(False)
          
           #draw sprites
           platform_group.draw(screen)
           player.draw()


           #draw panel
           draw_panel()
          
           draw_music_button()


           #check game over
           if player.rect.top > SCREEN_HEIGHT:
               game_over = True
               last_player_position = (player.rect.x, player.rect.y)
         
           #highscore x check
           if hscore >= 100:
               hsx = 290
           if hscore >= 1000:
               hsx = 280
           if hscore >= 10000:
               hsx = 270


      
           if event.type == MUSIC_END:
               pygame.mixer.music.play()  # Restart the music when it ends


          
      
       else:
           pygame.mouse.set_visible(True)
           score1 = score
           check_click = True
           if fade_counter < SCREEN_WIDTH:
               fade_counter += 7
               for y in range(0, 6, 2):
                   pygame.draw.rect(screen, PURPLE, (0, y * 100, fade_counter, 100))
                   pygame.draw.rect(screen, PURPLE, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
           draw_text('GAME OVER!', font_gyatt, WHITE, 50, 60)
           draw_text('SCORE: ' + str(score), font_huge, WHITE, sx, 350)
           draw_text('HIGHSCORE: ' + str(hscore), font_huge, WHITE, hsx1, 200)
           draw_restart_button()
          


   #escape quit
   key = pygame.key.get_pressed()
   if key[pygame.K_ESCAPE]:
       run = False


  




   #event handler
   for event in pygame.event.get():
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_p:
               paused = not paused
           if event.key == pygame.K_p:
           # Toggle music play/pause
               if music_paused:
                   pygame.mixer.music.unpause()
                   music_paused = False
               else:
                   pygame.mixer.music.pause()
                   music_paused = True


   # Check for mouse events
   if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
       # Check if the left mouse button was clicked
       mouse_x, mouse_y = pygame.mouse.get_pos()
       if clickable_rect.collidepoint(mouse_x, mouse_y) and check_click == True:
           # Execute your code when the image is clicked
           #reset var
               fade_counter = 0
               game_over = False
               score = 0
               scroll = 0
               #repostion player
               player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
               #reset plats
               platform_group.empty()
               #create starting plat
               platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
               platform_group.add(platform)
               check_click = False


   if event.type == pygame.QUIT:
       run = False




  
  
   #update display window
   pygame.display.update()






pygame.quit()







