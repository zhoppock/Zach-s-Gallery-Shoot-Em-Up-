import pygame, sys, random # import the pygame, sys, and random libraries all at once
pygame.init() # General setup with initiating pygame and its clock feature
clock = pygame.time.Clock()

class Reticle(pygame.sprite.Sprite):
    def __init__(self, image_location): # set up the atributes of the shooting reticle, no xy position since the mouse moves it around
        super().__init__()
        self.image = pygame.image.load(image_location) # load in a reticle image to be used in the game window
        self.rect = self.image.get_rect()
        self.gunfire = pygame.mixer.Sound('./Assets/Sounds/GunshotSnglHitLig PE1108102.mp3') # load in a sound that plays when you click your mouse
        self.hit = pygame.mixer.Sound('./Assets/Sounds/TearGasCanisterHit PE409701.mp3')# load in a sound that plays when you hit a target

    def fire(self):
        self.gunfire.play() # gun fire sound
        if pygame.sprite.spritecollide(reticle, targets_group, True): #detects in the reticle sprite interacts with the target sprite
            self.hit.play() # target his sound

    def update(self): # update multiple sprite classes simultaneously when called
        self.rect.center = pygame.mouse.get_pos() # gets the x and 7 coordinates of the mouse to align with the reticle image

class Targets(pygame.sprite.Sprite):
    def __init__(self, image_location, x_position, y_position): # set up the atributes of the shootable targets, has xy position to space it around the game window
        super().__init__()
        load_target = pygame.image.load(image_location) # load in a target image to be used in the game window
        self.image = pygame.transform.scale(load_target, (100, 100)) # size the target image down to look better in the game window
        self.rect = self.image.get_rect()
        self.rect.center = [x_position, y_position]

def you_won(): # displays a winning screen after all targets have been destroyed
    font_type = pygame.font.SysFont('Cooper Black', 100)
    draw_text = font_type.render("Nice shootin', Tex!", 1, (0, 0, 0))
    window.blit(draw_text, (window_width/2 - draw_text.get_width()/2, window_height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) # plays the winning screen for about 5 seconds before closing the window

def you_lost(): # displays a winning screen after all targets have been destroyed
    font_type = pygame.font.SysFont('Cooper Black', 50)
    draw_text = font_type.render("Better luck next time, Pardner.", 1, (0, 0, 0))
    window.blit(draw_text, (window_width/2 - draw_text.get_width()/2, window_height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) # plays the winning screen for about 5 seconds before closing the window

# Game Window with set dimensions
window_width = 1220
window_height = 680
window = pygame.display.set_mode((window_width, window_height)) # set the game window dimensions
load_image = pygame.image.load('./Assets/Images/bg_green.png') # load in an image to be the background
background_image = pygame.transform.scale(load_image, (window_width, window_height)) # resize the image to fit the game window
pygame.mouse.set_visible(False) # makes the default mouse cursor invisibile in the game window

# Reticle group that gets it shown on the game window
reticle = Reticle('./Assets/Images/crosshair_outline_large.png')
reticle_group = pygame.sprite.Group() # need a group to draw the reticle on the window
reticle_group.add(reticle)

#Targets group that places targets all around the game window
targets_group = pygame.sprite.Group() # need a group to draw the targets on the window
for target in range(25): # will display a given number of targets to shoot across the window
    add_target = Targets('./Assets/Images/target_red2.png', random.randrange(0, window_width), random.randrange(0, window_height)) # gives randomized positions for each target within the window
    targets_group.add(add_target)

def main():
    pygame.display.set_caption("Zach's Gallery Shoot 'Em Up!")
    bgm = pygame.mixer.Sound('./Assets/Music/Merry Go.mp3')
    bgm.play()
    start_timer = pygame.time.get_ticks()
    while len(targets_group) > 5:
        for event in pygame.event.get(): # captures an input on the game
            if event.type == pygame.QUIT: # if you exit out of the window, pygame and sys will end their processes
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                reticle.fire() # will play a gun fire sound when you click the mouse button down

        pygame.display.flip()
        window.blit(background_image, (0, 0)) # puts the background image in the game window, starting from 0 0 xy position

        targets_group.draw(window)

        reticle_group.draw(window) # draws the reticle on the window
        reticle_group.update()

        font_type = pygame.font.SysFont('Cooper Black', 50)
        targets_hit = font_type.render("Targets Hit: " + str(25 - len(targets_group)), 1, (0, 0, 0)) # draws a counter of how many targets have been destroyed
        window.blit(targets_hit, (window_width - targets_hit.get_width() - 10, 10))

        seconds = 16 - (pygame.time.get_ticks() - start_timer) / 1000 # you will have 15 seconds to complete the game
        if seconds < 1:
            you_lost() # plays if you run out of time
            pygame.quit()
            sys.exit()
        countdown = font_type.render("Time Left: " + str(int(seconds)), 1, (0, 0, 0))
        window.blit(countdown, (window_width - countdown.get_width() - 10, window_height - 75)) # displays the countdown timer on the window

        clock.tick(60) # controls the framerate of the game
    you_won()
    pygame.quit()
    sys.exit()

main()
