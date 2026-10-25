import pygame, sys, random, time
from pathlib import Path

#Game Data
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Factory Rush!")
main_font = pygame.font.SysFont("cambria", 45)
sec_font = pygame.font.SysFont("Roboto", 35)
third_font = pygame.font.SysFont("Roboto", 27)
forth_font = pygame.font.SysFont("Cambria", 40)

#Added by Copilot - Game Asset Loading
ASSET_DIR = Path(__file__).resolve().parent / "Game_Assets"
def load_asset(filename):
    return pygame.image.load(str(ASSET_DIR / filename))

#Game Decoration
BG = pygame.transform.scale(load_asset("FactoryRushMenuScreen.png"), (800, 600))

Lvl_1_BG = pygame.transform.scale(load_asset("Factory1Background.png"), (800, 600))
Lvl_2_BG = pygame.transform.scale(load_asset("Factory2Background.png"), (800, 600))
Lvl_3_BG = pygame.transform.scale(load_asset("Factory3Background.png"), (800, 600))

Tutorial_BG = pygame.transform.scale(load_asset("FactoryRushTutorialBackGround.png"), (800, 600))

#Game Modes
Run = False
Tutorial = False
Level_1 = False
Level_2 = False
Level_3 = False

#Button Class
class Button():
    def __init__(self, image, x_pos, y_pos, text_input): 
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.clicked = False

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
            #Button function

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = forth_font.render(self.text_input, True, "green") #Colour change customisable (text only)
        else:
            self.text = forth_font.render(self.text_input, True, "white")

#Button Data
Play1_button_surf = pygame.transform.scale(load_asset("ButtonImageMetal.png"), (250, 75))
Play1_button = Button(Play1_button_surf, 410, 235, "Level 1")
            
Play2_button_surf = pygame.transform.scale(load_asset("ButtonImageMetal.png"), (250, 75))
Play2_button = Button(Play2_button_surf, 410, 320, "Level 2")

Play3_button_surf = pygame.transform.scale(load_asset("ButtonImageMetal.png"), (250, 75))
Play3_button = Button(Play3_button_surf, 410, 405, "Level 3")

Tutorial_button_surf = pygame.transform.scale(load_asset("ButtonImageMetal.png"), (250, 75))
Tutorial_button = Button(Tutorial_button_surf, 410, 490, "Tutorial")

Hammer_display = pygame.transform.scale(load_asset("Nail_BoardSprite.png"), (160, 120))
Screw_display = pygame.transform.scale(load_asset("Screw_PiecesSprite.png"), (160, 120))
Wrench_display = pygame.transform.scale(load_asset("Bolt_MetalSprite.png"), (160, 120))

Hammer_error_display = pygame.transform.scale(load_asset("Nail_BoardErrorSprite.png"), (160, 120))
Screw_error_display = pygame.transform.scale(load_asset("Screw_PiecesSpriteError.png"), (160, 120))
Wrench_error_display = pygame.transform.scale(load_asset("Bolt_MetalSpriteError.png"), (160, 120))

Green_Alarm_Display = pygame.transform.scale(load_asset("GreenAlarm.png"), (60, 60))
Red_Alarm_Display = pygame.transform.scale(load_asset("RedAlarm.png"), (60, 60))

#Game variables
Items = ["Hammer","Screw", "Wrench", "Error"]
Error_items = [Hammer_error_display, Screw_error_display, Wrench_error_display]
Direction = ["<", ">"]
Belt_pos = ["UP", "DOWN"]
Lives = 0
Items_fixed = 0
Start_time = time.time()

Grace_period = 3.00
Item_Spawn_Delay = 180
Delay_count = 0
Item_duration = 600

Main_text = " "
sub_condition = False
Start = False
condition = False
inp = False
ERROR = False
code = ""
direction = ""
position = ""
Item_list = []
Alarm = [Green_Alarm_Display]

#Funtions
def draw(BG, Alarm, Main_text, Elapsed_time, Lives, Items_fixed, Item_list, direction, position):
    global Level_1, Level_2, Level_3
    screen.blit(BG, (0,0))

    if Level_1:
        Text_display = third_font.render(f'{Main_text}', 1, "dark red")
        screen.blit(Text_display, (260, 330))

        Time_display = main_font.render(f'{Elapsed_time}s', 1, "green")
        screen.blit(Time_display, (36, 32))

        Lives_display = sec_font.render(f'Errors: {Lives}', 1, "white")
        screen.blit(Lives_display, (610, 40))

        Items_fixed_display = sec_font.render(f'Fixed: {Items_fixed}', 1, "white")
        screen.blit(Items_fixed_display, (610, 90))

        for item in Item_list:
            screen.blit(item, (320, 80))

        for alarm in Alarm:
            screen.blit(alarm, (250, 30))
    
    if Level_2:
        Text_display = third_font.render(f'{Main_text}', 1, "dark red")
        screen.blit(Text_display, (265, 260))

        Time_display = main_font.render(f'{Elapsed_time}s', 1, "green")
        screen.blit(Time_display, (240, 15))

        Lives_display = sec_font.render(f'Errors: {Lives}', 1, "white")
        screen.blit(Lives_display, (457, 35))

        Items_fixed_display = sec_font.render(f'Fixed: {Items_fixed}', 1, "white")
        screen.blit(Items_fixed_display, (457, 70))

        for item in Item_list:
            if direction == "<":
                screen.blit(item, (80, 200))
            else:
                screen.blit(item, (575, 200))

        for alarm in Alarm:
            screen.blit(alarm, (125, 25))

    if Level_3:
        Text_display = third_font.render(f'{Main_text}', 1, "dark red")
        screen.blit(Text_display, (265, 425))

        Time_display = main_font.render(f'{Elapsed_time}s', 1, "green")
        screen.blit(Time_display, (250, 30))

        Lives_display = sec_font.render(f'Errors: {Lives}', 1, "white")
        screen.blit(Lives_display, (390, 150))

        Items_fixed_display = sec_font.render(f'Fixed: {Items_fixed}', 1, "white")
        screen.blit(Items_fixed_display, (390, 200))

        for item in Item_list:
            if direction == "<":
                if position == "UP":
                    screen.blit(item, (80, 65))
                
                else:
                    screen.blit(item, (80, 370))
                
            else:
                if position == "UP":
                    screen.blit(item, (570, 65))
                
                else:
                    screen.blit(item, (570, 370))

        for alarm in Alarm:
            screen.blit(alarm, (465, 25))

def sub_draw(BG):
    screen.blit(BG, (0,0))
        
def spawn_item():
    global Hammer_display, Screw_display, Wrench_display, Items, Direction, Belt_pos, Error_items
    display = ""
    code_direction = ""
    code_pos = ""
    code = ""
    #Function chooses a random item/ event to be fixed/ occur
    item = random.choice(Items)
    #Function chooses a location to spawn item
    code_direction = random.choice(Direction)
    code_pos = random.choice(Belt_pos)
    #Function will display item image on screen
    if item == "Hammer":
        display = Hammer_display
        code = "a"

    elif item == "Screw":
        display = Screw_display
        code = "s"

    elif item == "Wrench":
        display = Wrench_display
        code = "d"

    elif item == "Error":
        display = random.choice(Error_items)
        code = "f"

    return display, code, code_direction, code_pos

#Main Game loop
while True:
    while not Run and not Tutorial:
        passed_time = time.time() - Start_time
        sub_draw(BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if Play1_button.checkForInput(pygame.mouse.get_pos()):
                    Run = True
                    Level_1 = True
                    BG = Lvl_1_BG
                
                if Play2_button.checkForInput(pygame.mouse.get_pos()):
                    Run = True
                    Level_2 = True
                    BG = Lvl_2_BG

                if Play3_button.checkForInput(pygame.mouse.get_pos()):
                    Run = True
                    Level_3 = True
                    BG = Lvl_3_BG

                if Tutorial_button.checkForInput(pygame.mouse.get_pos()):
                    Tutorial = True
                    BG = Tutorial_BG

        Play1_button.changeColor(pygame.mouse.get_pos())
        Play1_button.update()

        Play2_button.changeColor(pygame.mouse.get_pos())
        Play2_button.update()

        Play3_button.changeColor(pygame.mouse.get_pos())
        Play3_button.update()

        Tutorial_button.changeColor(pygame.mouse.get_pos())
        Tutorial_button.update()

        pygame.display.update()

    while not Run and Tutorial:
        passed_time = time.time() - Start_time
        sub_draw(BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    BG = pygame.transform.scale(load_asset("FactoryRushMenuScreen.png"), (800, 600))
                    Tutorial = False
                    print("Exit")

        pygame.display.update()

    while Run:
        if not sub_condition:
            input_code = ""
            input_direction = ""
            input_pos = ""

        Clock = pygame.time.Clock()
        Delay_count += Clock.tick(60)
        
        Elapsed_time = time.time() - Start_time - passed_time
        Elapsed_time_display = round(Elapsed_time, 2)

        #Create code to monitor live time to proceed with neccasary actions (eg spawn items, speed up events)
        if  Elapsed_time >= Grace_period:
            if not Start:
                Start = True
                print("Start")

            if Start:
                if not condition:
                    condition = True
                    
                if Delay_count > Item_Spawn_Delay and not sub_condition:
                    Alarm = [Red_Alarm_Display]
                    Main_text = " "
                    
                    c = spawn_item()
                    display = c[0]
                    Item_list.append(display)
                    code = c[1]
                    direction = c[2]
                    position = c[3]
                    
                    Delay_count = 0
                    sub_condition = True
                    print(code, direction, position)

        #Create code for user to enter input
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        input_direction += ">"
                        print(">")

                    if event.key == pygame.K_LEFT:
                        input_direction += "<"
                        print("<")

                    if event.key == pygame.K_UP:
                        input_pos += "UP"
                        print("UP")

                    if event.key == pygame.K_DOWN:
                        input_pos += "DOWN"
                        print("DOWN")
                        
                    if event.key == pygame.K_a:
                        input_code += "a"
                        print("a")
                        
                    if event.key == pygame.K_s:
                        input_code += "s"
                        print("s")
                        
                    if event.key == pygame.K_d:
                        input_code += "d"
                        print("d")

                    if event.key == pygame.K_f:
                        input_code += "f"
                        print("f")

        if Level_1:
            if len(input_code) == 1:
                inp = True
                print(input_code)

        if Level_2:
            if len(input_code) == 1 and len(input_direction) == 1:
                inp = True
                print(input_code, input_direction)

        if Level_3:
            if len(input_code) == 1:
                if len(input_direction) == 1:
                    if len(input_pos) > 1:
                        inp = True
                        print(input_code, input_direction, input_pos)
                    
        #Create a code to remove/ display neccasary information (eg too long, error, correct code)
        if Delay_count > Item_duration and condition:
            condition = False
            sub_condition = False
            
            Item_list = []
            Lives += 1
            Delay_count = 0
            Alarm = [Red_Alarm_Display]
            
            Main_text = "         ERROR; Took too long"
            print("Too long")
        
        if inp:
            if Level_1:
                if code == input_code:
                    Items_fixed += 1
                    
                    condition = False
                    sub_condition = False
                    inp = False

                    Item_list = []
                    Delay_count = 0
                    Item_Spawn_Delay -= 4
                    Item_duration -= 2
                    Alarm = [Green_Alarm_Display]

                    print("Correct")
                    
                else:
                    Lives += 1
                    condition = False
                    sub_condition = False
                    inp = False
                    Item_list = []
                    Delay_count = 0
                    Alarm = [Red_Alarm_Display]
                    
                    Main_text = " ERROR; Wrong command used"
                    print("Incorrect")

            if Level_2:
                if code == input_code and direction == input_direction:
                    Items_fixed += 1
                
                    condition = False
                    sub_condition = False
                    inp = False
                
                    Item_list = []
                    Delay_count = 0
                    Item_Spawn_Delay -= 4
                    Item_duration -= 2
                    Alarm = [Green_Alarm_Display]

                    print("Correct")
                
                else:
                    Lives += 1
                    condition = False
                    sub_condition = False
                    inp = False
                    Item_list = []
                    Delay_count = 0
                    Alarm = [Red_Alarm_Display]

                    Main_text = " ERROR; Wrong command used"
                    print("Incorrect")

            if Level_3:
                if code == input_code:
                    if direction == input_direction:
                        if position == input_pos:
                            Items_fixed += 1
                        
                            condition = False
                            sub_condition = False
                            inp = False
                        
                            Item_list = []
                            Delay_count = 0
                            Item_Spawn_Delay -= 4
                            Item_duration -= 2
                            Alarm = [Green_Alarm_Display]

                            print("Correct")
                        else:
                            ERROR = True
                    else:
                        ERROR = True
                else:
                    ERROR = True

            if ERROR:
                Lives += 1
                condition = False
                sub_condition = False
                inp = False
                ERROR = False
                Item_list = []
                Delay_count = 0
                Alarm = [Red_Alarm_Display]

                Main_text = " ERROR; Wrong command used"
                print("Incorrect")
            
        if Lives == 3:
            BG = pygame.transform.scale(load_asset("FactoryLostBackground.png"), (800, 600))
            screen.blit(BG, (0,0))
            Lost_display = sec_font.render(f'Items fixed: {Items_fixed}', 1, "dark red")
            screen.blit(Lost_display, (320, 470))
            
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()
        
        draw(BG, Alarm, Main_text, Elapsed_time_display, Lives, Items_fixed, Item_list, direction, position)
        pygame.display.update()
    
