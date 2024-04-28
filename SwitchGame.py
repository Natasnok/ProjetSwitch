import pygame
import random
import time
import sys
import math
import csv
import os

# Initialize Pygamef
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)
FONT_SIZE = 48
FONT = pygame.font.Font(None, FONT_SIZE)
FONT_TITRE= pygame.font.Font(None, 100)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SwitchGame")

# Charger l'image de fond
image_fond = pygame.image.load("switchgame.jpg")
# Redimensionner l'image de fond à la taille de la fenêtre
image_fond = pygame.transform.scale(image_fond, (WIDTH, HEIGHT))

# Charger l'image de fond
game_over_fond = pygame.image.load("game over.jpg")
# Redimensionner l'image de fond à la taille de la fenêtre
game_over_fond = pygame.transform.scale(game_over_fond, (WIDTH, HEIGHT))

# Variable pour stocker le choix du menu
menu_choice = 0

def main_menu():
    global nb_switch, menu_choice
    screen.blit(image_fond, (0, 0))
    
    # Charger l'image du bouton "parametre"
    parametre_img = pygame.image.load("parametre.png")
    parametre_rect = parametre_img.get_rect()
    parametre_rect.bottomright = (WIDTH - 25, HEIGHT - 25)
    
    while True:
        draw_text("Switch Game", FONT_TITRE, BLACK, screen, WIDTH//2 - 215, HEIGHT//2 - 145)
        draw_text("Switch Game", FONT_TITRE, WHITE, screen, WIDTH//2 - 217, HEIGHT//2 - 147)

        # Dessiner le bouton "Start"
        start_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
        pygame.draw.rect(screen, GREEN, start_button_rect)
        draw_text("Start", FONT, BLACK, screen, WIDTH//2 - 40, HEIGHT//2 + 10)

        # Dessiner le bouton "HighScore"
        highscore_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
        pygame.draw.rect(screen, YELLOW, highscore_button_rect)
        draw_text("HighScore", FONT, BLACK, screen, WIDTH//2 - 80, HEIGHT//2 + 110)

        # Dessiner le bouton "Quitter"
        quit_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 200, 200, 50)
        pygame.draw.rect(screen, RED, quit_button_rect)
        draw_text("Quitter", FONT, BLACK, screen, WIDTH//2 - 60, HEIGHT//2 + 210)

        # Dessiner le bouton "parametre"
        screen.blit(parametre_img, parametre_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Vérifier si le bouton "Start" a été cliqué ...
                if start_button_rect.collidepoint(mouse_pos):
                    # Code pour le bouton "Start"
                    button.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('switchgame.mp3')
                    pygame.mixer.music.play(-1)
                    nb_switch = 3
                    menu_choice = 1
                    return
                # Vérifier si le bouton "HighScore" a été cliqué ...
                elif highscore_button_rect.collidepoint(mouse_pos):
                    # Code pour le bouton "HighScore"
                    button.play()
                    menu_choice = 2
                    return
                # Vérifier si le bouton "Quitter" a été cliqué ...
                elif quit_button_rect.collidepoint(mouse_pos):
                    button.play()
                    pygame.quit()
                    sys.exit()
                # Vérifier si le bouton "parametre" a été cliqué
                elif parametre_rect.collidepoint(mouse_pos):
                    # Traitez ici le clic sur le bouton "parametre"
                    button.play()
                    menu_choice = 3
                    return

def init_score():
    chemin=os.path.join(os.path.dirname(__file__), "highscore.csv")

    if not os.path.exists(chemin):
        # Exemple de données à enregistrer dans le fichier CSV
        donnees = [
        ["None", -1],
        ["None", -1],
        ["None", -1],
        ["None", -1],
        ["None", -1],
        ["None", -1],
        ["None", -1],
        ["None", -1],
        ["None", -1],
        ["None", -1],
        ]
    
        # Création et écriture dans le fichier CSV
        with open(chemin, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(donnees)

def verif_score(new_score):
    chemin=os.path.join(os.path.dirname(__file__), "highscore.csv")

    # Lecture du fichier CSV
    with open(chemin, 'r') as csvfile:
        reader = csv.reader(csvfile)
        highscore = list(reader)
    
    # Modification de la ligne spécifiée
    for i, score in enumerate(highscore):
        if new_score > int(score[1]):
            return True
    return False

def actuali_score(new_score,name):
    chemin=os.path.join(os.path.dirname(__file__), "highscore.csv")

    # Lecture du fichier CSV
    with open(chemin, 'r') as csvfile:
        reader = csv.reader(csvfile)
        highscore = list(reader)
    
    # Modification de la ligne spécifiée
    for i, score in enumerate(highscore):
        if new_score > int(score[1]):
            highscore.insert(i, [name, new_score])
            highscore.pop()
    
            # Écriture dans le fichier CSV
            with open(chemin, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(highscore)
            return
    return

def generate_question():
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operator = random.choice(['+', '-', '*'])
        if operator == '+':
            answer = num1 + num2
        elif operator == '-':
            answer = num1 - num2
        else:
            answer = num1 * num2
        question_text = f"{num1} {operator} {num2}"
        return question_text, answer
# Fonction pour le jeu de calcul mental
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def Calcul_mental():
    global question,answer,score_calcul, score_switch, nb_switch
    time_per_question = 10  # Temps en secondes par question
    current_time = pygame.time.get_ticks()
    user_answer = "" # Variable pour stocker la réponse de l'utilisateur
    game_over = False
    start_time = time.time()
    game_duration = switch_time
    pygame.display.flip()

    while not game_over:
        screen.fill(WHITE)
        if time.time() - start_time >= game_duration:
            screen.fill(BLACK)
            pygame.display.flip()
            return

        # Gestion du temps
        time_left = time_per_question - (pygame.time.get_ticks() - current_time) // 1000
        if time_left <= 0:
            current_time = pygame.time.get_ticks()
        else:
            # Générer une question si le temps n'est pas écoulé
            if time_left == time_per_question:
                if question == "" or answer == "":
                    question, answer = generate_question()
            question_surface = FONT.render(question, True, BLACK)
            question_rect = question_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            screen.blit(question_surface, question_rect)

            # Afficher le score, le nombre de vies et le temps restant
            draw_text(f"Score: {score_switch}", FONT, BLACK, screen, 10, 10)
            draw_text(f"{time_left} s", FONT, BLACK, screen, WIDTH - 420, 10)
            draw_text(f"Switch: {nb_switch}", FONT, BLACK, screen, WIDTH - 170 , 10)
            # Afficher la réponse de l'utilisateur
            draw_text(f"Réponse: {user_answer}", FONT, BLACK, screen, WIDTH//2 - 100, HEIGHT - 100)

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Si Enter est pressé
                    if user_answer.lstrip('-').isdigit(): # Vérifier si l'utilisateur a entré un nombre
                        if int(user_answer) == int(answer):
                            ding.play()
                            score_calcul += 1
                            question=""
                            answer=""
                            if score_calcul == 3:
                                validate.play()
                                score_switch += 100
                                nb_switch += 1
                                score_calcul=0
                        else:
                            wrong.play()
                            question=""
                            answer=""
                            screen.fill(BLACK)
                            pygame.display.flip()
                            return
                        current_time = pygame.time.get_ticks()
                        user_answer = "" # Effacer la réponse de l'utilisateur après vérification
                elif event.key == pygame.K_BACKSPACE: # Si la touche Backspace est pressée
                    user_answer = user_answer[:-1] # Supprimer le dernier caractère
                else:
                    if event.unicode.isdigit() or (event.unicode == '-' and len(user_answer) == 0): # Autoriser uniquement les chiffres et le signe négatif
                        user_answer += event.unicode

# Fonction pour dessiner le joueur
def draw_player(x, y):
    pygame.draw.circle(screen, BLACK, (x, y), PLAYER_RADIUS)

# Fonction pour dessiner les flèches
def draw_arrow(x, y, angle):
    pygame.draw.line(screen, RED, (x, y), (x + ARROW_SIZE * math.cos(angle), y + ARROW_SIZE * math.sin(angle)), 2)
    pygame.draw.polygon(screen, RED, [
        (x + ARROW_SIZE * math.cos(angle), y + ARROW_SIZE * math.sin(angle)),
        (x + ARROW_SIZE * math.cos(angle - 5 * math.pi / 6), y + ARROW_SIZE * math.sin(angle - 5 * math.pi / 6)),
        (x + ARROW_SIZE * math.cos(angle + 5 * math.pi / 6), y + ARROW_SIZE * math.sin(angle + 5 * math.pi / 6))
    ])

# Fonction pour dessiner le cercle
def draw_circle():
    pygame.draw.circle(screen, BLACK, CIRCLE_CENTER, CIRCLE_RADIUS, 2)

# Fonction pour générer une nouvelle flèche
def spawn_arrow():
    side = random.randint(0, 3)
    if side == 0:
        x = random.randint(CIRCLE_CENTER[0] - CIRCLE_RADIUS, CIRCLE_CENTER[0] + CIRCLE_RADIUS)
        y = CIRCLE_CENTER[1] - CIRCLE_RADIUS
    elif side == 1:
        x = CIRCLE_CENTER[0] + CIRCLE_RADIUS
        y = random.randint(CIRCLE_CENTER[1] - CIRCLE_RADIUS, CIRCLE_CENTER[1] + CIRCLE_RADIUS)
    elif side == 2:
        x = random.randint(CIRCLE_CENTER[0] - CIRCLE_RADIUS, CIRCLE_CENTER[0] + CIRCLE_RADIUS)
        y = CIRCLE_CENTER[1] + CIRCLE_RADIUS
    else:
        x = CIRCLE_CENTER[0] - CIRCLE_RADIUS
        y = random.randint(CIRCLE_CENTER[1] - CIRCLE_RADIUS, CIRCLE_CENTER[1] + CIRCLE_RADIUS)
        
    # Calcul de l'angle entre la position de départ de la flèche et la position du joueur
    angle = math.atan2(player_y - y, player_x - x)
    return {'x': x, 'y': y, 'angle': angle}

# Fonction pour vérifier si un point est à l'intérieur du cercle
def point_inside_circle(x, y):
    distance_squared = (x - CIRCLE_CENTER[0]) ** 2 + (y - CIRCLE_CENTER[1]) ** 2
    return distance_squared <= CIRCLE_RADIUS ** 2

# Fonction pour le Jeu_Des_Fleches
def Jeu_Des_Fleches():
    global player_x, player_y, score_fleche, arrow_delay, ARROW_WAVE_DELAY, game_over, arrow_count, arrows, CIRCLE_CENTER, CIRCLE_RADIUS, PLAYER_RADIUS, ARROW_SIZE, score_switch, nb_switch

    PLAYER_RADIUS = 10
    PLAYER_SPEED = 5

    # Définition des paramètres des flèches
    ARROW_SIZE = 10
    ARROW_SPEED = 2
    INITIAL_ARROW_DELAY = 60

    # Définition des paramètres du cercle
    CIRCLE_RADIUS = 290
    CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)

    arrow_delay = INITIAL_ARROW_DELAY
    ARROW_WAVE_DELAY = 5  # Initialisation de ARROW_WAVE_DELAY
    ARROW_WAVE_DELAY_REDUCTION = 1
    game_over = False
    start_time = time.time()
    game_duration = switch_time

    clock = pygame.time.Clock()
    pygame.display.flip()
    running = True

    # Boucle principale du jeu
    while running:
        screen.fill(WHITE)
        if time.time() - start_time >= game_duration:
            screen.fill(BLACK)
            pygame.display.flip()
            return

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()


        if game_over:
            crash.play()
            arrows = []
            player_x = WIDTH // 2
            player_y = HEIGHT // 2
            arrow_count = 0
            screen.fill(BLACK)
            pygame.display.flip()
            return

        # Déplacement du joueur
        keys = pygame.key.get_pressed()
        new_player_x = player_x
        new_player_y = player_y
        if keys[pygame.K_LEFT] or keys[pygame.K_q] or keys[pygame.K_a]:
            new_player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_player_x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_z] or keys[pygame.K_w]:
            new_player_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_player_y += PLAYER_SPEED

        # Vérifier si le nouveau positionnement du joueur est à l'intérieur du cercle
        if point_inside_circle(new_player_x, new_player_y):
            player_x = new_player_x
            player_y = new_player_y

        # Dessiner le cercle
        draw_circle()

        # Dessiner le joueur
        draw_player(player_x, player_y)

        # Générer les flèches
        if arrow_count % arrow_delay == 0:
            if arrow_count % (arrow_delay * ARROW_WAVE_DELAY) == 0:
                for _ in range(10):
                    arrows.append(spawn_arrow())
                if ARROW_WAVE_DELAY != 1:
                    ARROW_WAVE_DELAY -= ARROW_WAVE_DELAY_REDUCTION  # Réduction du délai entre les vagues
            else:
                arrows.append(spawn_arrow())
            
        arrow_count += 1

        # Dessiner les flèches et les déplacer
        for arrow in arrows:
            draw_arrow(arrow['x'], arrow['y'], arrow['angle'])
            arrow['x'] += ARROW_SPEED * math.cos(arrow['angle'])
            arrow['y'] += ARROW_SPEED * math.sin(arrow['angle'])

            # Vérifier la collision avec le joueur
            distance = math.sqrt((arrow['x'] - player_x) ** 2 + (arrow['y'] - player_y) ** 2)
            if distance < PLAYER_RADIUS + ARROW_SIZE:
                game_over = True

        # Vérifier si les flèches sont sorties de l'écran
        arrows = [arrow for arrow in arrows if 0 <= arrow['x'] <= WIDTH and 0 <= arrow['y'] <= HEIGHT]

        # Affichage du score
        score_fleche += 1
        if score_fleche >= 400:
            validate.play()
            score_switch += 100
            nb_switch += 1
            score_fleche = 0

        draw_text(f"Score: {score_switch}", FONT, BLACK, screen, 10, 10)
        draw_text(f"Switch: {nb_switch}", FONT, BLACK, screen, WIDTH - 170 , 10)

        # Mettre à jour l'affichage
        pygame.display.flip()
        
        # Limiter le nombre de FPS
        clock.tick(60)

# Fonction pour le Memory
def Memory():
    global selected_tiles, matched_tiles, numbers, score_switch, nb_switch, score_memory
    # Define tile properties
    TILE_SIZE = 100
    GAP_SIZE = 10
    ROWS = 4
    COLS = 4
    pygame.display.flip()

    # Create numbers for tiles
    if numbers==[]:
        numbers = list(range(1, 9)) * 2
        random.shuffle(numbers)

    # Create tile rects
    tile_rects = []
    for row in range(ROWS):
        for col in range(COLS):
            x = col * (TILE_SIZE + GAP_SIZE) + 100
            y = row * (TILE_SIZE + GAP_SIZE) + 100
            tile_rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

    # Game variables
    start_time = time.time()
    game_duration = switch_time

    # Main game loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_text(f"Score: {score_switch}", FONT, BLACK, screen, 10, 10)
        draw_text(f"Switch: {nb_switch}", FONT, BLACK, screen, WIDTH - 170, 10)
        if time.time() - start_time >= game_duration:
            screen.fill(BLACK)
            pygame.display.flip()
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if len(selected_tiles) < 2:
                    for i, rect in enumerate(tile_rects):
                        if rect.collidepoint(event.pos) and i not in selected_tiles and i not in matched_tiles:
                            selected_tiles.append(i)

        # Draw tiles
        for i, rect in enumerate(tile_rects):
            if i in selected_tiles or i in matched_tiles:
                number = numbers[i]
                text = FONT.render(str(number), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)

        pygame.display.flip()

        # Check for match
        if len(selected_tiles) == 2:
            index1, index2 = selected_tiles
            if numbers[index1] == numbers[index2]:
                ding.play()
                matched_tiles.extend(selected_tiles)
                score_memory+=1
                if score_memory==2:
                    validate.play()
                    nb_switch += 1
                    score_switch += 100
                    score_memory = 0
                selected_tiles = []
            else:
                time.sleep(1)
                selected_tiles = []

        # Check for game over
        if len(matched_tiles) == len(numbers):
            validate.play()
            nb_switch += 1
            selected_tiles = []
            matched_tiles = []
            numbers = []
            screen.fill(BLACK)
            pygame.display.flip()
            return
    pygame.display.flip()

# Fonction pour le Snake
def our_snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(screen, BLACK, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = FONT.render(msg, True, color)
    text_rect = mesg.get_rect(center=(WIDTH // 2, (HEIGHT // 2)-10))
    screen.blit(mesg, text_rect)

def Snake():
    global Length_of_snake, x1, y1, x1_change, y1_change, snake_List, Length_of_snake, score_snake, foodx, foody, nb_switch, score_switch
    start_time = time.time()
    game_duration = switch_time
    snake_block = 20  # Augmented the size of the pixels
    snake_speed = 15
   
    clock = pygame.time.Clock()
    pygame.display.flip()
 
    game_over = False
    while not game_over:
        game_close = False
 
        while not game_close:
            if time.time() - start_time >= game_duration:
                screen.fill(BLACK)
                pygame.display.flip()
                return
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
 
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LEFT] or keys[pygame.K_q] or keys[pygame.K_a]) and x1_change != snake_block:
                x1_change = -snake_block
                y1_change = 0
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and x1_change != -snake_block:
                x1_change = snake_block
                y1_change = 0
            elif (keys[pygame.K_UP] or keys[pygame.K_z] or keys[pygame.K_w]) and y1_change != snake_block:
                y1_change = -snake_block
                x1_change = 0
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and y1_change != -snake_block:
                y1_change = snake_block
                x1_change = 0
 
            if x1 >= WIDTH - 60 or x1 < 60 or y1 >= HEIGHT - 60 or y1 < 60:
                crash.play()
                x1 = WIDTH / 2
                y1 = HEIGHT / 2
                x1_change = 20
                y1_change = 0
                snake_List = []
                Length_of_snake = 1
                score_snake = 0
                foodx = round(random.randrange(70, WIDTH - 70) / 20.0) * 20.0
                foody = round(random.randrange(70, HEIGHT - 70) / 20.0) * 20.0
                screen.fill(BLACK)
                pygame.display.flip()
                return
 
            x1 += x1_change
            y1 += y1_change
            screen.fill(BLUE)
 
            pygame.draw.rect(screen, RED, [0, 0, WIDTH, 60])  # top
            pygame.draw.rect(screen, RED, [0, 0, 60, HEIGHT])  # left
            pygame.draw.rect(screen, RED, [WIDTH - 60, 0, 60, HEIGHT])  # right
            pygame.draw.rect(screen, RED, [0, HEIGHT - 60, WIDTH, 60])  # bottom
 
            pygame.draw.rect(screen, GREEN, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
 
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
 
            our_snake(snake_block, snake_List)
 
            if x1 == foodx and y1 == foody or (x1 >= foodx and x1 < foodx + snake_block and y1 >= foody and y1 < foody + snake_block):
                foodx = round(random.randrange(70, WIDTH - 70) / 20.0) * 20.0
                foody = round(random.randrange(70, HEIGHT - 70) / 20.0) * 20.0
                pomme.play()
                Length_of_snake += 1
                score_snake += 1
                if score_snake == 3:
                    validate.play()
                    nb_switch += 1
                    score_switch += 100
                    score_snake = 0
 
            draw_text(f"Score: {score_switch}", FONT, WHITE, screen, 10, 10)
            draw_text(f"Switch: {nb_switch}", FONT, WHITE, screen, WIDTH - 170 , 10)
            pygame.display.update()
 
            clock.tick(snake_speed)
 
        while game_close:
            crash.play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            game_close = False
            x1 = WIDTH / 2
            y1 = HEIGHT / 2
            x1_change = 20
            y1_change = 0
            snake_List = []
            Length_of_snake = 1
            score_snake = 0
            foodx = round(random.randrange(70, WIDTH - 70) / 20.0) * 20.0
            foody = round(random.randrange(70, HEIGHT - 70) / 20.0) * 20.0
            screen.fill(BLACK)
            pygame.display.flip()
            return
        
# Liste des jeux
jeux = [Calcul_mental, Jeu_Des_Fleches, Snake, Memory]

score_switch = 0
current_game = None
next_game=True
new_game=None
start_time = 0 # Time in seconds before switching to a new game
switch_time = random.randint(5,15)
arrows = []
player_x = WIDTH // 2
player_y = HEIGHT // 2
arrow_count = 0
x1 = WIDTH / 2
y1 = HEIGHT / 2
x1_change = 20
y1_change = 0
snake_List = []
Length_of_snake = 1
score_snake = 0
score_calcul = 0
score_fleche = 0
score_memory = 0
foodx = round(random.randrange(70, WIDTH - 70) / 20.0) * 20.0
foody = round(random.randrange(70, HEIGHT - 70) / 20.0) * 20.0
question=""
answer=""
score_calcul=0
selected_tiles = []
matched_tiles = []
numbers = []
games_over = False
clock = pygame.time.Clock()
clock.tick(60)

init_score()
volume_music = 0.5
volume_effet = 0.5
pygame.mixer.music.set_volume(volume_music)
crash=pygame.mixer.Sound("crash.mp3")
crash.set_volume(volume_effet)
button=pygame.mixer.Sound("Button.mp3")
button.set_volume(volume_effet)
validate=pygame.mixer.Sound("Validate.mp3")
validate.set_volume(volume_effet)
teleport=pygame.mixer.Sound("teleport.mp3")
teleport.set_volume(volume_effet)
ding=pygame.mixer.Sound("Ding.mp3")
ding.set_volume(volume_effet)
wrong=pygame.mixer.Sound("Wrong.mp3")
wrong.set_volume(volume_effet)
pomme=pygame.mixer.Sound("Pomme.mp3")
pomme.set_volume(volume_effet)
perdu=pygame.mixer.Sound("pin ouin ouin ouinnnnn.mp3")
perdu.set_volume(volume_effet)

pygame.mixer.music.stop()
pygame.mixer.music.load('switchitup.mp3')
pygame.mixer.music.play(-1)

while True:
    if menu_choice == 0:
        main_menu()  # Si aucun choix n'a été fait, affichez le menu principal
    elif menu_choice == 1:
        # Si le choix est 1, lancez le jeu
        if next_game:
            teleport.play()
            new_game = random.choice(jeux)
            while current_game == new_game:
                new_game = random.choice(jeux)
            current_game = new_game
            next_game = False
            scale_factor = (1 - score_switch / 10000) ** 2
            new_time = 5 + 10 * scale_factor
            switch_time = random.uniform(5,new_time)
            txt = "Next Game: " + (str(new_game)).split()[1]
            if "_" in txt:
                txt = txt.replace("_", " ")
            screen.fill(BLACK)
            message(txt, WHITE)
            pygame.display.flip()
            pygame.time.wait(2000)
            current_game()  # Start the selected game
            nb_switch -= 1
            next_game = False
        if time.time() - start_time >= switch_time:
            next_game=True  # Reset the current game
        if nb_switch <= 0:
            perdu.play()
            pygame.mixer.music.stop()
            pygame.mixer.music.load('game over.mp3')
            pygame.mixer.music.play(-1)
            screen.fill(WHITE)
            screen.blit(game_over_fond, (0, 0))
            if verif_score(score_switch):
                pseudo=False
                draw_text("New record !", FONT_TITRE, BLACK, screen, WIDTH//2 - 188, HEIGHT//2 - 198)
                draw_text("New record !", FONT_TITRE, WHITE, screen, WIDTH//2 - 190, HEIGHT//2 - 200)
                draw_text("Enter a name", FONT, BLACK, screen, WIDTH - 498, HEIGHT - 278)
                draw_text("Enter a name", FONT, WHITE, screen, WIDTH - 500, HEIGHT - 280)
                name = ""
                while not pseudo:
                    draw_text(f"Pseudo : {name}", FONT, BLACK, screen, WIDTH - 568, HEIGHT - 198)
                    draw_text(f"Pseudo : {name}", FONT, WHITE, screen, WIDTH - 570, HEIGHT - 200)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                             # Si la touche Entrée est pressée, vérifier si le pseudo n'est pas vide
                                if name != "":
                                    # Si le pseudo n'est pas vide, quitter
                                    actuali_score(score_switch,name)
                                    games_over=True
                                    pseudo=True
                            elif event.key == pygame.K_BACKSPACE:
                                # Si la touche Backspace est pressée, supprimer le dernier caractère
                                screen.fill(WHITE)
                                screen.blit(game_over_fond, (0, 0))
                                draw_text("New record !", FONT_TITRE, BLACK, screen, WIDTH//2 - 188, HEIGHT//2 - 198)
                                draw_text("New record !", FONT_TITRE, WHITE, screen, WIDTH//2 - 190, HEIGHT//2 - 200)
                                draw_text("Enter a name", FONT, BLACK, screen, WIDTH - 498, HEIGHT - 278)
                                draw_text("Enter a name", FONT, WHITE, screen, WIDTH - 500, HEIGHT - 280)
                                name = name[:-1]
                                pygame.display.update()
                            elif len(name) < 5:
                                # Si la longueur du texte est inférieure à 5 et n'est pas vide, ajouter le caractère saisi
                                if event.unicode != "":
                                    name += event.unicode
            else:
                games_over=True
        while games_over:
            screen.fill(WHITE)
            screen.blit(game_over_fond, (0, 0))
            draw_text("GAME OVER", FONT_TITRE, BLACK, screen, WIDTH//2 - 208, HEIGHT//2 - 148)
            draw_text("GAME OVER", FONT_TITRE, WHITE, screen, WIDTH//2 - 210, HEIGHT//2 - 150)
            draw_text(f"Score: {score_switch}", FONT, BLACK, screen, WIDTH - 463, HEIGHT - 318)
            draw_text(f"Score: {score_switch}", FONT, WHITE, screen, WIDTH - 465, HEIGHT - 320)
            draw_text("Press a key to continue", FONT, BLACK, screen, WIDTH - 588, HEIGHT - 198)
            draw_text("Press a key to continue", FONT, WHITE, screen, WIDTH - 590, HEIGHT - 200)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    games_over = False
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('switchitup.mp3')
                    pygame.mixer.music.play(-1)            
                    score_switch = 0
                    arrows = []
                    player_x = WIDTH // 2
                    player_y = HEIGHT // 2
                    arrow_count = 0
                    x1 = WIDTH / 2
                    y1 = HEIGHT / 2
                    x1_change = 20
                    y1_change = 0
                    snake_List = []
                    Length_of_snake = 1
                    score_snake = 0
                    score_calcul = 0
                    score_fleche = 0
                    score_memory = 0
                    foodx = round(random.randrange(70, WIDTH - 70) / 20.0) * 20.0
                    foody = round(random.randrange(70, HEIGHT - 70) / 20.0) * 20.0
                    question=""
                    answer=""
                    score_calcul=0
                    selected_tiles = []
                    matched_tiles = []
                    numbers = []
                    games_over = False
                    menu_choice=0

    elif menu_choice==2:
        highscore_window_open = True
        screen.fill(WHITE)
        screen.blit(image_fond, (0, 0))

        # Dessiner le bouton "Retour"
        return_button=pygame.draw.rect(screen, GRAY, (20, 40, 118, 30))
        draw_text("Retour", FONT, BLACK, screen, 25, 40)

        chemin=os.path.join(os.path.dirname(__file__), "highscore.csv")
        # Lecture du fichier CSV
        with open(chemin, 'r') as csvfile:
            reader = csv.reader(csvfile)
            highscore = list(reader)
    
        draw_text("HighScore", FONT_TITRE, BLACK, screen, WIDTH//2 - 163, HEIGHT//2 - 278)
        draw_text("HighScore", FONT_TITRE, WHITE, screen, WIDTH//2 - 165, HEIGHT//2 - 280)
        # Modification de la ligne spécifiée
        for i, score in enumerate(highscore):
            if int(score[1])!=-1:
                draw_text(f"{i+1}: {score[0]} -> {int(score[1])}", pygame.font.Font(None, 60), BLACK, screen, WIDTH//2-198 , (102+50*i))
                draw_text(f"{i+1}: {score[0]} -> {int(score[1])}", pygame.font.Font(None, 60), WHITE, screen, WIDTH//2-200 , (100+50*i))
            else:
                draw_text(f"{i+1}: No score", pygame.font.Font(None, 60), BLACK, screen, WIDTH//2-198 , (102+50*i))
                draw_text(f"{i+1}: No score", pygame.font.Font(None, 60), WHITE, screen, WIDTH//2-200 , (100+50*i))
        pygame.display.flip()
        while highscore_window_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if return_button.collidepoint(mouse_pos):
                        button.play()
                        highscore_window_open = False
                        menu_choice=0

    elif menu_choice==3:
        screen.fill(WHITE)
        screen.blit(image_fond, (0, 0))
        parametre_window_open = True
        dragging1 = False
        dragging2 = False
        draw_text("Parametres", FONT_TITRE, BLACK, screen, WIDTH//2 - 188, HEIGHT//2 - 238)
        draw_text("Parametres", FONT_TITRE, WHITE, screen, WIDTH//2 - 190, HEIGHT//2 - 240)
        draw_text("Volume musique", FONT, BLACK, screen, 200, 170)
        draw_text("Volume musique", FONT, WHITE, screen, 198, 168)
        draw_text("Volume effet sonore", FONT, BLACK, screen, 200, 270)
        draw_text("Volume effet sonore", FONT, WHITE, screen, 198, 268)

        # Dessiner le bouton "Retour"
        return_button=pygame.draw.rect(screen, GRAY, (20, 40, 118, 30))
        draw_text("Retour", FONT, BLACK, screen, 25, 40)

        while parametre_window_open:
            pygame.mixer.music.set_volume(volume_music)
            crash.set_volume(volume_effet)
            button.set_volume(volume_effet)
            validate.set_volume(volume_effet)
            teleport.set_volume(volume_effet)
            ding.set_volume(volume_effet)
            wrong.set_volume(volume_effet)
            pomme.set_volume(volume_effet)
            perdu.set_volume(volume_effet)
            pygame.display.flip()
            # Définir les dimensions des barres de volume
            volume_bar_width = 300
            volume_bar_height = 40
            volume_bar_x = 200
            volume_bar_y1 = 210
            volume_bar_y2 = 310

            # Définir la couleur de la barre de volume et du curseur
            volume_bar_color = GRAY
            volume_cursor_color = RED

            # Dessiner les barres de volume
            pygame.draw.rect(screen, volume_bar_color, (volume_bar_x, volume_bar_y1, volume_bar_width, volume_bar_height), border_radius=20)
            volume_cursor_x1 = volume_bar_x + int(volume_music * volume_bar_width)
            draw_text(f"{int(volume_music * 100)}%", FONT, BLACK, screen, volume_bar_x + volume_bar_width + 52, volume_bar_y1 + volume_bar_height // 2 - 13)
            draw_text(f"{int(volume_music * 100)}%", FONT, WHITE, screen, volume_bar_x + volume_bar_width + 50, volume_bar_y1 + volume_bar_height // 2 - 15)
            pygame.draw.circle(screen, volume_cursor_color, (volume_cursor_x1, volume_bar_y1 + volume_bar_height // 2), 20)

            pygame.draw.rect(screen, volume_bar_color, (volume_bar_x, volume_bar_y2, volume_bar_width, volume_bar_height), border_radius=20)
            volume_cursor_x2 = volume_bar_x + int(volume_effet * volume_bar_width)
            draw_text(f"{int(volume_effet * 100)}%", FONT, BLACK, screen, volume_bar_x + volume_bar_width + 52, volume_bar_y2 + volume_bar_height // 2 - 13)
            draw_text(f"{int(volume_effet * 100)}%", FONT, WHITE, screen, volume_bar_x + volume_bar_width + 50, volume_bar_y2 + volume_bar_height // 2 - 15)
            pygame.draw.circle(screen, volume_cursor_color, (volume_cursor_x2, volume_bar_y2 + volume_bar_height // 2), 20)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if return_button.collidepoint(mouse_pos):
                        button.play()
                        parametre_window_open=False
                        menu_choice=0
                    if volume_cursor_x1 - 20 <= mouse_pos[0] <= volume_cursor_x1 + 20 and volume_bar_y1 <= mouse_pos[1] <= volume_bar_y1 + volume_bar_height:
                        dragging1 = True
                    if volume_cursor_x2 - 20 <= mouse_pos[0] <= volume_cursor_x2 + 20 and volume_bar_y2 <= mouse_pos[1] <= volume_bar_y2 + volume_bar_height:
                        dragging2 = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if dragging1:
                        dragging1 = False
                    elif dragging2:
                        dragging2 = False
                if event.type == pygame.MOUSEMOTION:
                    if dragging1:
                        mouse_pos = pygame.mouse.get_pos()
                        volume_music = (mouse_pos[0] - volume_bar_x) / volume_bar_width
                        volume_music = max(0, min(1, volume_music))
                        screen.fill(WHITE)
                        screen.blit(image_fond, (0, 0))
                        pygame.draw.rect(screen, volume_bar_color, (volume_bar_x, volume_bar_y1, volume_bar_width, volume_bar_height), border_radius=20)
                        draw_text(f"{int(volume_music * 100)}%", FONT, BLACK, screen, volume_bar_x + volume_bar_width + 52, volume_bar_y1 + volume_bar_height // 2 - 13)
                        draw_text(f"{int(volume_music * 100)}%", FONT, WHITE, screen, volume_bar_x + volume_bar_width + 50, volume_bar_y1 + volume_bar_height // 2 - 15)
                        pygame.draw.circle(screen, volume_cursor_color, (volume_cursor_x1, volume_bar_y1 + volume_bar_height // 2), 20)
                        pygame.draw.rect(screen, volume_bar_color, (volume_bar_x, volume_bar_y2, volume_bar_width, volume_bar_height), border_radius=20)
                        draw_text(f"{int(volume_effet * 100)}%", FONT, BLACK, screen, volume_bar_x + volume_bar_width + 52, volume_bar_y2 + volume_bar_height // 2 - 13)
                        draw_text(f"{int(volume_effet * 100)}%", FONT, WHITE, screen, volume_bar_x + volume_bar_width + 50, volume_bar_y2 + volume_bar_height // 2 - 15)
                        pygame.draw.circle(screen, volume_cursor_color, (volume_cursor_x2, volume_bar_y2 + volume_bar_height // 2), 20)
                        draw_text("Parametres", FONT_TITRE, BLACK, screen, WIDTH//2 - 188, HEIGHT//2 - 238)
                        draw_text("Parametres", FONT_TITRE, WHITE, screen, WIDTH//2 - 190, HEIGHT//2 - 240)
                        draw_text("Volume musique", FONT, BLACK, screen, 200, 170)
                        draw_text("Volume musique", FONT, WHITE, screen, 198, 168)
                        draw_text("Volume effet sonore", FONT, BLACK, screen, 200, 270)
                        draw_text("Volume effet sonore", FONT, WHITE, screen, 198, 268)
                        return_button=pygame.draw.rect(screen, GRAY, (20, 40, 118, 30))
                        draw_text("Retour", FONT, BLACK, screen, 25, 40)
                    elif dragging2:
                        mouse_pos = pygame.mouse.get_pos()
                        volume_effet = (mouse_pos[0] - volume_bar_x) / volume_bar_width
                        volume_effet = max(0, min(1, volume_effet))
                        screen.fill(WHITE)
                        screen.blit(image_fond, (0, 0))
                        pygame.draw.rect(screen, volume_bar_color, (volume_bar_x, volume_bar_y1, volume_bar_width, volume_bar_height), border_radius=20)
                        draw_text(f"{int(volume_music * 100)}%", FONT, BLACK, screen, volume_bar_x + volume_bar_width + 52, volume_bar_y1 + volume_bar_height // 2 - 13)
                        draw_text(f"{int(volume_music * 100)}%", FONT, WHITE, screen, volume_bar_x + volume_bar_width + 50, volume_bar_y1 + volume_bar_height // 2 - 15)
                        pygame.draw.circle(screen, volume_cursor_color, (volume_cursor_x1, volume_bar_y1 + volume_bar_height // 2), 20)
                        pygame.draw.rect(screen, volume_bar_color, (volume_bar_x, volume_bar_y2, volume_bar_width, volume_bar_height), border_radius=20)
                        draw_text(f"{int(volume_effet * 100)}%", FONT, BLACK, screen, volume_bar_x + volume_bar_width + 52, volume_bar_y2 + volume_bar_height // 2 - 13)
                        draw_text(f"{int(volume_effet * 100)}%", FONT, WHITE, screen, volume_bar_x + volume_bar_width + 50, volume_bar_y2 + volume_bar_height // 2 - 15)
                        pygame.draw.circle(screen, volume_cursor_color, (volume_cursor_x2, volume_bar_y2 + volume_bar_height // 2), 20)
                        draw_text("Parametres", FONT_TITRE, BLACK, screen, WIDTH//2 - 188, HEIGHT//2 - 238)
                        draw_text("Parametres", FONT_TITRE, WHITE, screen, WIDTH//2 - 190, HEIGHT//2 - 240)
                        draw_text("Volume musique", FONT, BLACK, screen, 200, 170)
                        draw_text("Volume musique", FONT, WHITE, screen, 198, 168)
                        draw_text("Volume effet sonore", FONT, BLACK, screen, 200, 270)
                        draw_text("Volume effet sonore", FONT, WHITE, screen, 198, 268)
                        return_button=pygame.draw.rect(screen, GRAY, (20, 40, 118, 30))
                        draw_text("Retour", FONT, BLACK, screen, 25, 40)
                        

