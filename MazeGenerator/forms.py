import pygame

class form:
    def __init__(self, posX, posY, width, height, color):
        self._width = width
        self._height = height
        self._posX = posX;
        self._posY = posY
        self._color = color
        self._inFocusColor = (230, 30, 100)
        self._input = str()
        self._inFocus = False

    def draw(self, screen):
        if self._inFocus:
            pygame.draw.rect(screen, self._inFocusColor, (self._posX, self._posY, self._width, self._height))
        else:
            pygame.draw.rect(screen, self._color, (self._posX, self._posY, self._width, self._height))
        screen.blit(pygame.font.SysFont('Arial', self._height).render(self._input, True, (0, 0, 0)),(self._posX, self._posY))

    def capture(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if mx >= self._posX and mx <= self._posX + self._width and my >= self._posY and my <= self._posY + self._height:
                self._inFocus = True
            else:
                self._inFocus = False
            return
        
        if self._inFocus and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self._input = self._input[:(len(self._input) - 1)]
                return
            keyInput = pygame.key.name(event.key)
            if keyInput.isnumeric():
                if len(self._input) == 0 and keyInput == "0":
                    return
                self._input = self._input + keyInput

    def changeInput(self, newInput):
        self._input = newInput
    
    def getInput(self):
        return self._input

class button:
    def __init__(self, posX, posY, width, height, color, text):
        self._width = width
        self._height = height
        self._posX = posX;
        self._posY = posY
        self._color = color
        self._text = text
    
    def draw(self, screen):
        pygame.draw.rect(screen, self._color, (self._posX, self._posY, self._width, self._height), border_radius = 20)
        text = pygame.font.SysFont('Arial', self._height).render(self._text, True, (0, 0, 0))
        textRect = text.get_rect(center=(self._posX + self._width / 2, self._posY + self._height/2))
        screen.blit(text, textRect)

    def checkClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
           mx, my = pygame.mouse.get_pos()
           if mx >= self._posX and mx <= self._posX + self._width and my >= self._posY and my <= self._posY + self._height:
               return True
        return False

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.flip()
    screen.fill((50, 50, 200))
    f = form(100, 200, 200, 50, (255,255,255))
    
    while True:
        for event in pygame.event.get():
            f.capture(event)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

        f.draw(screen)
        pygame.display.update()