import pygame, sys
import random

def Blackjack():
   
    global full_deck
    global card_x_pos
    global card_y_pos
    global AI_card_x_pos
    global AI_card_y_pos
    global hidden_card_x_pos
    global hidden_card_y_pos
 
    global run_game
    # CREA EL OBJETO CARTA
 
    class Card():
        def __init__(self,V,N,S,P):
            self.value = V      # VALORES DE CARTA
            self.name = N       # NOMBRE DE CARTA
            self.suit = S       # SUIT DE CARTA
            self.image = P      # IMAGEN DE CARTA
 
 
    # CREA UNA OBJETOS CARTA PARA LA BARAJA
    def initializeDeck():
        # INICIALIZA LA BARAJA VACÍA
        deck = []
        i = 0
        for j in range(len(CARD_VALUES)):
            for k in CARD_SUITS:
                # CREA OBJETO CARTA Y UN APENDICE A BARAJA (deck)
                deck.append(Card(CARD_VALUES[j], CARD_NAMES[j], k, card_img[i]))
                i += 1
 
        return deck
 
 
    # ENCUENTRA EL ÍNDICE DEL ARREGLO 1D DE CARTAS
    def card_index(V,S):
        if S == 'S':
            T = 1
        elif S == 'C':
            T = 2
        elif S == 'D':
            T = 3
        elif S == 'H':
            T = 4
        else:
            print("Error con T en card_index()")
 
        return (V-1)*4 + (T-1)
 
 
    # DESPLIEGA LAS CARTAS EN LA PANTALLA / GUI
    def display_card():
 
        # DESPLIEGA TODAS LAS CARTAS EN LA MANO DEL JUGADOR    
        if (len( player_hand) != 0):
            for i in range(len( player_hand)):
                SCREEN.blit( player_hand[i].image, (card_x_pos[i],card_y_pos[i]))
 
        if(reveal or spectate):
            # DESPLIEGA TODAS LAS CARTAS EN LA MANO DEL IA HACIA ARRIBA
            if (len( AI_hand) != 0):
                for i in range(len( AI_hand)):
                    SCREEN.blit( AI_hand[i].image, (AI_card_x_pos[i],AI_card_y_pos[i]))
        else:
            # DESPLIEGA TODAS LAS CARTAS EN LA MANO DEL IA HACIA ABAJO
            if (len( hidden_hand) != 0):
                for i in range(len( hidden_hand)):
                    SCREEN.blit( hidden_hand[i].image, (hidden_card_x_pos[i],hidden_card_y_pos[i]))
 
        pygame.display.update()
 
 
    # SELECCIONA DE MANERA ALEATORIA UNA CARTA DE LA BARAJA
    def get_random_card():
       
        r = random.randint(0,len(full_deck)-1)
        print(len(full_deck), end=' ')
        print(r)
 
        # REMUEVE Y REGRESA UNA CARTA DE LA BARAJA
        return full_deck.pop(r)
 
 
    # ASIGNA UNA CARTA DE LA BARAJA A LA MANO DEL JUGADOR
    def player_draw_cards():
 
        # AGREGA UNA CARTA A LA MANO DEL JUGADOR
        player_hand.append(get_random_card())
 
        # AGREGA UNA NUEVA POSICIÓN DE CARTA
        if (len(card_x_pos) == 0):
            card_x_pos.append(DEFAULT_X)
        else:
            card_x_pos.append(card_x_pos[-1] + DEFAULT_OFFSET)
 
        card_y_pos.append(DEFAULT_Y)
 
 
    # ASIGNA UNA CARTA DE LA BARAJA A LA MANO DEL IA
    def AI_draw_card():
 
        # SI LA CARTA DE LA MANO DEL IA ES MENOR A 18,TOMA UNA CARTA
        if get_card_value(AI_hand) < 18:
            AI_hand.append(get_random_card())
            hidden_hand.append(bg_card)
 
            # AGREGA UNA CARTA A LA POSICIÓN PREDETERMINADA SI LA MANO DEL IA ESTÁ VACÍA
            if (len(AI_card_x_pos) == 0):
                AI_card_x_pos.append(DEFAULT_X)
                hidden_card_x_pos.append(DEFAULT_X)
            else:
                # AGREGA UNA CARTA PROXIMA A LA CARTA ANTERIOR
                AI_card_x_pos.append(AI_card_x_pos[-1] + DEFAULT_OFFSET)
                hidden_card_x_pos.append(hidden_card_x_pos[-1] + DEFAULT_OFFSET)
 
            # TODAS LAS CARTAS TIENEN EL MIMSO VALOR-Y
            AI_card_y_pos.append(AI_DEFAULT_Y)
            hidden_card_y_pos.append(AI_DEFAULT_Y)
 
            # ¿TOMÉ UNA CARTA?
            return True
        else:
            return False
 
 
    # OBTIENE LA PUNTUACIÓN ACTUIAL DE LA MANO DEL JUGADOR / IA    
    def get_card_value(hand):
        # SI LA MANO ESTÁ VACÍA, REGRESA CERO
        if len(hand) == 0:
            return 0
        else:
            # INICIALIZA LAS VARIABLES
            Aces = []
            sum = 0
 
            # RECORRE TODA LA MANO
            for i in hand:
                # ¿CUÁNTOS ASES EXISTEN EN LA MANO?
                if i.name == 1:
                    Aces.append(i)
 
                # LA SUMA DE LOS VALORES DE LAS CARTAS
                sum += i.value
           
            # REDUCE EL VALOR DE LOS ASES PARA PREVENIR QUE SE PASE DE 21
            if sum > 21 and (len(Aces) != 0):
                sum -= 10
            return sum
 
 
    # DESPLIEGA EL TEXTO EN LA PANTALLA / GUI
    def draw_texts():
        # DESPLIEGA LOS TEXTOS DEL GUI
        ai_hand_text = GUI_font.render("MANO IA:",True,white)
        player_hand_text = GUI_font.render("MANO JUGADOR:"+str(get_card_value(player_hand)),True,white)
        winner_text = WIN_font.render(win_str[win_int],True,white)
 
        SCREEN.blit(winner_text, (SCREEN_WIDTH//2-win_x[win_int], SCREEN_HEIGHT//4-win_y[win_int]))
        SCREEN.blit(ai_hand_text, (90,15))
        SCREEN.blit(player_hand_text, (90,SCREEN_HEIGHT-CARD_HEIGHT-60))
 
        # DESPLIEGA LAS INSTRUCCIONES
        r_TEXT = INST_font.render('Presione [R] para reiniciar', True, white)
        space_TEXT = INST_font.render('Presione [SPACE] para hacer hit', True, white)
        enter_TEXT = INST_font.render('Presione [ENTER] para pasar', True, white)
        s_TEXT = INST_font.render('Presione [S] para activar modo espectador', True, white)
        esc_TEXT = INST_font.render('Presione [ESC] para salir del juego', True, white)
     
 
        SCREEN.blit(r_TEXT, (SCREEN_WIDTH//2-100,SCREEN_HEIGHT//1.2+0))
        SCREEN.blit(space_TEXT, (SCREEN_WIDTH//2-100,SCREEN_HEIGHT//1.2+20))
        SCREEN.blit(enter_TEXT, (SCREEN_WIDTH//2-100,SCREEN_HEIGHT//1.2+40))
        SCREEN.blit(s_TEXT, (SCREEN_WIDTH//2-100,SCREEN_HEIGHT//1.2+60))
        SCREEN.blit(esc_TEXT, (SCREEN_WIDTH//2-100,SCREEN_HEIGHT//1.2+80))
 
    # win.blit(name_text, (355,7))
        #win.blit(class_text, (450,7+15))
 
        # DESPLIEGA EL PUNTAJE DEL IA SI EL MODO ESPECTADOR ESTÁ HABILITADO
        if spectate or reveal:
            ai_hand_text = GUI_font.render("MANO IA:"+ str(get_card_value(AI_hand)),True,white)
            SCREEN.blit(ai_hand_text, (90,15))
 
 
 
    ## INICIALIZA VARIABLES
 
    # CREA EL GUI
    pygame.init()
 
    # INICIALIZA LA GUI
    SCREEN_WIDTH = 1380
    SCREEN_HEIGHT = 720
    SCREEN = pygame.display.set_mode(((1380, 720)))
    pygame.display.set_caption("BlackJack")
 
 
    # INICIALIZA LOS DATOS DE LAS CARTAS
    CARD_VALUES = [11,2,3,4,5,6,7,8,9,10,10,10,10]
    CARD_NAMES = list(range(1,14))
    CARD_SUITS = list(range(1,5))
 
    # DEFINE EL TAMAÑO DE LAS CARTAS EN PIXELES
    CARD_WIDTH = 200
    CARD_HEIGHT = 300
 
    card_img_dir = []
    card_img = []
 
    # COLORES RGB
    black = (0,0,0)
    white = (255,255,255)
 
 
    # OBTIENE EL DIRECTORIO Y LOS OBJETOS PARA LAS IMAGENES DE LAS CARTAS
    for i in CARD_NAMES:
        for j in CARD_SUITS:
            card_img_dir.append("assets/" + str(i) + "-" + str(j) + ".png")
 
    for i in card_img_dir:
        card_img.append(pygame.transform.scale(pygame.image.load(i), (CARD_WIDTH, CARD_HEIGHT)))
 
    bg_card = Card(0,0,0,pygame.transform.scale(pygame.image.load("assets/Card_Back.png"), (CARD_WIDTH, CARD_HEIGHT)))
 
 
    # INICIALIZA LA BARAJA DEL JUGADOR Y DEL IA
    player_hand = []
    card_x_pos = []
    card_y_pos = []
 
    AI_hand = []
    AI_card_x_pos = []
    AI_card_y_pos = []
 
    hidden_hand = []
    hidden_card_x_pos = []
    hidden_card_y_pos = []
 
    DEFAULT_X = 90
    DEFAULT_Y = SCREEN_HEIGHT-CARD_HEIGHT-30
    AI_DEFAULT_Y = 45
    DEFAULT_OFFSET = 45
 
    def get_font(size):
        return pygame.font.Font("assets/font.ttf", size)
    # INICIALIZA LAS FUENTES PARA EL TEXTO
    GUI_font = pygame.font.Font("assets/font.ttf", 32)
    WIN_font = pygame.font.Font("assets/font.ttf", 32)
    INST_font = pygame.font.Font("assets/font.ttf", 18)
    TITLE_font = pygame.font.Font("assets/font.ttf", 24)
 
    win_int = 0
    win_str = ['', 'JUGADOR GANA', 'IA GANA', 'JUGADOR SE PASÓ — IA GANA', 'JUGADOR GANA — IA SE PASÓ', 'EMPATE', 'SIN GANADORES']
    win_x = [0, 100, 65, 180, 180, 40, 100]
    win_y = [0, 30, 30, 30, 30, 30, 30]
 
 
    # INICIALIZA BOOLEANOS PARA EL MANTENIMIENTO DEL GUI
    main_loop = 0
    run_game = True
    reveal = False
    session = True
    spectate = False
 
 
    # CREA UNA BARAJA Y UNA COPIA DE LA BARAJA PARA MANTENER LA ORIGINAL
    original_deck = initializeDeck()
    full_deck = list(original_deck)
 
 
    # LOOP DEL JUEGO
    while run_game:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # VENTANA DEL GUI PERMANECERA ABIERTA HASTA QUE SE PRESIONE [X] O EL GUI SE CIERRE
                pygame.quit()
                sys.exit()
               
 
        # CREA EL BACKGROUND
        SCREEN.fill("Dark Green")
        draw_texts()
 
        # USADO PARA PREVENIR QUE SE SPAMEEN LOS BOTONES
        if main_loop > 0:
            main_loop += 1
        if main_loop > 5:
            main_loop = 0
 
 
        # OBTIENE TODAS LAS TECLAS PRESIONADAS
        keys = pygame.key.get_pressed()
 
        # REINICIA EL JUEGO
        if keys[pygame.K_r]:
            # REINICIALIZA #
            full_deck = list(original_deck)
            run_game = True
            session = True
            main_loop = 0
            win_int = 0
            reveal = False
            session = True
            player_hand = []
            card_x_pos = []
            card_y_pos = []
            AI_hand = []
            AI_card_x_pos = []
            AI_card_y_pos = []
            hidden_hand = []
            hidden_card_x_pos = []
            hidden_card_y_pos = []
 
        # PLAYER HIT / OBTIENE OTRA CARTA
        if keys[pygame.K_SPACE] and main_loop == 0 and session:
            player_draw_cards()
            main_loop = 1
           
            AI_hit = AI_draw_card()
 
            print("IA: ", end='')
            print(get_card_value(AI_hand))
 
            # PROBAR TODOS LOS POSIBLES RESULTADOS
            if get_card_value(AI_hand) > 21 and get_card_value(player_hand) > 21:
                session = False
                print("SIN GANADORES")
                win_int = 6
                reveal = True
            elif get_card_value(AI_hand) > 21:
                session = False
                print("IA SE PASÓ, JUGADROR GANA")
                win_int = 4
                reveal = True
            elif get_card_value(player_hand) > 21:
                # JUGADOR SE PASÓ
                # IA GANA    
                print('JUGADOR SE PASÓ, IA GANA')
                win_int = 3
                session = False
                reveal = True
            elif get_card_value(AI_hand) == 21 and get_card_value(player_hand) == 21:
                # EMPATE
                print('EMPATE')
                win_int = 5
                session = False
                reveal = True
            elif get_card_value(AI_hand) == 21 and get_card_value(player_hand) != 21:
                # IA GANA
                print('IA GANA')
                win_int = 2
                session = False
                reveal = True
            elif get_card_value(AI_hand) != 21 and get_card_value(player_hand) == 21:
                # JUGADOR GANA
                print('JUGADOR GANA')
                win_int = 1
                session = False
                reveal = True
       
        # JUGADOR PASA TURNO
        if (keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]) and main_loop == 0 and session:
            main_loop = 1
 
            AI_hit = AI_draw_card()
 
            print("IA: ", end='')
            print(get_card_value(AI_hand))
 
            # PROBAR TODAS LOS POSIBLES RESULTADOS
            if (AI_hit == False):
                if get_card_value(AI_hand) > get_card_value(player_hand):
                    session = False
                    print("IA GANA")
                    win_int = 2
                    reveal = True
                elif get_card_value(AI_hand) < get_card_value(player_hand):
                    session = False
                    print("JUGADOR GANA")
                    win_int = 1
                    reveal = True
                else:
                    session = False
                    print("EMPATE")
                    win_int = 5
                    reveal = True
            else:
                if get_card_value(AI_hand) > 21 and get_card_value(player_hand) > 21:
                    session = False
                    print("SIN GANADORES")
                    win_int = 6
                    reveal = True
                elif get_card_value(AI_hand) > 21:
                    session = False
                    print("IA SE PASÓ, JUAGADOR GANA")
                    win_int = 4
                    reveal = True
                elif get_card_value(AI_hand) == 21 and get_card_value(player_hand) == 21:
                    # EMPATE
                    print('EMPATE')
                    win_int = 5
                    session = False
                    reveal = True
                elif get_card_value(AI_hand) == 21 and get_card_value(player_hand) != 21:
                    # IA GANA
                    print('IA GANA')
                    win_int = 2
                    session = False
                    reveal = True
                elif get_card_value(AI_hand) != 21 and get_card_value(player_hand) == 21:
                    # JUGADOR GANA
                    print('JUGADOR GANA')
                    win_int = 1
                    session = False
                    reveal = True
 
        # HABILITAR MODO ESPECTADOR
        if keys[pygame.K_s] and main_loop == 0:
            if spectate == False:
                spectate = True
            else:
                spectate = False
 
            main_loop = 1
 
        # SALIR DEL JUEGO
        if keys[pygame.K_ESCAPE] and main_loop == 0:
            pygame.quit() 
 
        display_card()
    pygame.quit()

Blackjack()