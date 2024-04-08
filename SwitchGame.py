import pygame
import random
import time
import sys
import math

# Initialize Pygamef
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
FONT_SIZE = 48
FONT = pygame.font.Font(None, FONT_SIZE)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SwitchGame")

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
            draw_text(f"Switch: {nb_switch}", FONT, BLACK, screen, WIDTH - 160 , 10)
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
                            score_calcul += 1
                            question=""
                            answer=""
                            if score_calcul == 3:
                                score_switch += 1
                                nb_switch += 1
                                score_calcul=0
                        else:
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
        if keys[pygame.K_LEFT]:
            new_player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            new_player_x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            new_player_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
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
            score_switch += 1
            nb_switch += 1
            score_fleche = 0

        draw_text(f"Score: {score_switch}", FONT, BLACK, screen, 10, 10)
        draw_text(f"Switch: {nb_switch}", FONT, BLACK, screen, WIDTH - 160 , 10)

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
    draw_text(f"Score: {score_switch}", FONT, BLACK, screen, 10, 10)
    draw_text(f"Switch: {nb_switch}", FONT, BLACK, screen, WIDTH - 160 , 10)
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
    turns = 0
    start_time = time.time()
    game_duration = switch_time

    # Main game loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_text(f"Score: {score_switch}", FONT, BLACK, screen, 10, 10)
        draw_text(f"Switch: {nb_switch}", FONT, BLACK, screen, WIDTH - 160, 10)
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
                matched_tiles.extend(selected_tiles)
                score_memory+=1
                if score_memory==2:
                    nb_switch += 1
                    score_switch += 1
                    score_memory = 0
                selected_tiles = []
            else:
                time.sleep(1)
                selected_tiles = []

        # Check for game over
        if len(matched_tiles) == len(numbers):
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

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def Snake():
    global Length_of_snake, x1, y1, x1_change, y1_change, snake_List, Length_of_snake, score_snake, foodx, foody, nb_switch, score_switch
    start_time = time.time()
    game_duration = switch_time
    snake_block = 10
    snake_speed = 20
    
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

            handle_events()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and x1_change != snake_block:
                x1_change = -snake_block
                y1_change = 0
            elif keys[pygame.K_RIGHT] and x1_change != -snake_block:
                x1_change = snake_block
                y1_change = 0
            elif keys[pygame.K_UP] and y1_change != snake_block:
                y1_change = -snake_block
                x1_change = 0
            elif keys[pygame.K_DOWN] and y1_change != -snake_block:
                y1_change = snake_block
                x1_change = 0

            if x1 >= WIDTH - 60 or x1 < 60 or y1 >= HEIGHT - 60 or y1 < 60:
                x1 = WIDTH / 2
                y1 = HEIGHT / 2
                x1_change = 0
                y1_change = 0
                snake_List = []
                Length_of_snake = 1
                score_snake = 0
                foodx = round(random.randrange(61, WIDTH - 61) / 10.0) * 10.0
                foody = round(random.randrange(61, HEIGHT - 61) / 10.0) * 10.0
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

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(61, WIDTH - 61) / 10.0) * 10.0
                foody = round(random.randrange(61, HEIGHT - 61) / 10.0) * 10.0
                Length_of_snake += 1
                score_snake += 1
                if score_snake == 3:
                    nb_switch += 1
                    score_switch += 1
                    score_snake = 0

            draw_text(f"Score: {score_switch}", FONT, WHITE, screen, 10, 10)
            draw_text(f"Switch: {nb_switch}", FONT, WHITE, screen, WIDTH - 160 , 10)
            pygame.display.update()

            clock.tick(snake_speed)

        while game_close:
            handle_events()
            game_close = False
            x1 = WIDTH / 2
            y1 = HEIGHT / 2
            x1_change = 0
            y1_change = 0
            snake_List = []
            Length_of_snake = 1
            score_snake = 0
            foodx = round(random.randrange(61, WIDTH - 61) / 10.0) * 10.0
            foody = round(random.randrange(61, HEIGHT - 61) / 10.0) * 10.0
            screen.fill(BLACK)
            pygame.display.flip()
            return

# Liste des jeux
jeux = [Calcul_mental, Jeu_Des_Fleches, Memory, Snake]

global switch_time, nb_switch, start_time, score_switch

score_switch =0
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
x1_change = 10
y1_change = 0
snake_List = []
Length_of_snake = 1
score_snake = 0
score_calcul = 0
score_fleche = 0
score_memory = 0
foodx = round(random.randrange(61, WIDTH - 61) / 10.0) * 10.0
foody = round(random.randrange(61, HEIGHT - 61) / 10.0) * 10.0
question=""
answer=""
score_calcul=0
nb_switch=3
selected_tiles = []
matched_tiles = []
numbers = []
games_over = False
clock = pygame.time.Clock()
clock.tick(60)

# Main loop
while True:
    # If no game is currently running, select a new game to play
    if next_game:
        new_game=random.choice(jeux)
        while current_game==new_game:
            new_game=random.choice(jeux)
        current_game=new_game
        txt="Next Game: "+ (str(new_game)).split()[1]
        if "_" in txt:
            txt=txt.replace("_", " ")
        message(txt,WHITE)
        pygame.display.flip()
        pygame.time.wait(2000)
        current_game()  # Start the selected game
        nb_switch -= 1
        next_game=False
    # Check if it's time to switch to a new game based on elapsed time
    if time.time() - start_time >= switch_time:
        next_game=True  # Reset the current game
    if nb_switch <= 0:
        games_over=True
    while games_over:
        screen.fill(WHITE)
        message("Game Over",BLACK)
        draw_text(f"Score: {score_switch}", FONT, BLACK, screen, WIDTH - 465, HEIGHT - 290)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                nb_switch = 0
                game_over = False

            

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()