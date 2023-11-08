import pygame
import os

TITLE = "PvZ Builder"
TILES_HORIZONTAL = 9
TILES_VERTICAL = 6
TILESIZE = 128
WINDOW_WIDTH = TILESIZE * TILES_HORIZONTAL
WINDOW_HEIGHT = TILESIZE * TILES_VERTICAL

class Tiles:
    def __init__(self, screen):
        self.screen = screen
        self.inner = []
        self.current_tile = None
        self._load_data()

    def _load_data(self):
        self.inner = []
        filepath = os.path.join("data", "lawn.txt")
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        id = 0
        for count_i, myline in enumerate(mylines):
            temp_list = myline.split(";")
            temp_list = [i.strip() for i in temp_list if len(i.strip()) > 0]
            for count_j, elem in enumerate(temp_list):
                new_tile = Tile(id, count_j, count_i, elem)
                self.inner.append(new_tile)
                id+= 1

    def draw(self, surface):
        if len(self.inner) == 0:
            raise ValueError("Error! No tiles to display")
        for elem in self.inner:
            self.screen.blit(elem.image, elem.rect)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()
        

class Tile:
    def __init__(self, id, x, y, tileType):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.tileType = tileType

        match tileType:
            case "g":
                filename = "grass01.png"
            case "w":
                filename = "water01.png"
            case _:
                raise ValueError("Error! Tile Type: ", tileType)

        self.rect = pygame.Rect(self.x * TILESIZE, self.y * TILESIZE, TILESIZE, TILESIZE)
        image_path = os.path.join("data", "images")
        self.image = pygame.image.load(os.path.join(image_path, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

    def debug_print(self):
        s = "id: {}, x: {}, y: {}, kind {}"
        s = s.format(self.id, self.x, self.y, self.tileType)
        print(s)
                        


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(TITLE)
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.BG_COLOUR = (100, 255, 100)
        self.keep_looping = True

        self.tiles = Tiles(self.surface)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False

    def update(self):
        pass

    def draw(self):
        self.surface.fill(self.BG_COLOUR)
        self.tiles.draw(self.surface)
        pygame.display.update()

    def main(self):
        while self.keep_looping:
            self.events()
            self.update()
            self.draw()

if __name__ == "__main__":
    mygame = Game()
    mygame.main()
