from random import choice
from string import ascii_lowercase
from requests import get
import pygame
pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self):
        self.fonte = pygame.font.Font('JetBrainsMono-Regular.ttf', 45)
        self.alfabeto = ascii_lowercase + "áãâàéêíóõôúç"
        self.tela: pygame.Surface = pygame.display.set_mode((1200, 675))

        self.choice = None
        self.category = None
        self.atual = None
        self.erros = None
        self.letras = None
        self.running = True

    @staticmethod
    def get_word():
        cat = choice([2, 3, 4, 5, 8, 10, 12, 13])
        response = get(f"https://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=1&fs2={cat}&Submit=Nova+palavra")
        response.encoding = 'UTF-8'
        palavra = response.text.split('<td')[1].split("<div style=\"font-size:3em; color:#6200C5;\">")[1].split('<')[0]
        categorias = ["Dicionário completo", "Dicionário para crianças", "Alimentos",
                      "Animais", "Cores", "Corpo humano", "Educação", "Família",
                      "Figuras geométricas", "Mídia de comunicação", "Números",
                      "Números de 0 a 9", "Profissões", "Transporte"]
        return palavra[2:].lower(), categorias[cat]

    @staticmethod
    def string_assign(string, index, value):
        string = list(string)
        string[index] = value
        return ''.join(string)

    def center(self, imagem: pygame.Surface):
        return int((self.tela.get_width() - imagem.get_width()) / 2)

    def click(self, letter):
        if letter in self.letras:
            return
        self.letras = self.string_assign(self.letras, self.alfabeto.index(letter), letter)
        if letter in self.choice:
            for ind, ltr in enumerate(self.choice):
                if ltr == letter:
                    self.atual = self.string_assign(self.atual, ind*2, ltr)
        else:
            self.erros += 1
            if self.erros >= 7:
                self.lose()
        if self.atual[::2] == self.choice:
            self.win()

    def new_game(self):
        self.choice, self.category = self.get_word()
        self.atual = ("_ " * len(self.choice))[:-1]
        self.letras = " " * len(self.alfabeto)
        self.erros = 0

    def blit(self):
        palavra: pygame.Surface = self.fonte.render(self.atual, True, (0, 0, 0))
        digitadas: pygame.Surface = self.fonte.render(self.letras, True, (0, 0, 0))
        todas: pygame.Surface = self.fonte.render(self.alfabeto, True, (150, 150, 150))
        categ1: pygame.Surface = self.fonte.render("Categoria: ", True, (0, 0, 0))
        categ2: pygame.Surface = self.fonte.render(self.category, True, (0, 200, 0))

        y = 400
        self.tela.blit(palavra, (self.center(palavra), y))
        self.tela.blit(todas, (self.center(todas), y + 100))
        self.tela.blit(digitadas, (self.center(todas), y + 100))
        self.tela.blit(categ1, (50, 50))
        self.tela.blit(categ2, (350, 50))
        image = pygame.transform.scale(pygame.image.load(f"Images/{self.erros}.png"), (480, 270))
        self.tela.blit(image, (200, 150))

    def win(self):
        self.blit()
        pygame.display.update()
        pygame.mixer.music.load("cheers.mp3")
        pygame.mixer.music.play()
        self.new_game()
        pygame.mixer.music.stop()

    def lose(self):
        txt = self.fonte.render(' '.join(list(self.choice)), True, (255, 0, 0))
        self.tela.blit(txt, (self.center(txt), 400))
        self.blit()
        pygame.display.update()
        pygame.mixer.music.load("crack.mp3")
        pygame.mixer.music.play()
        self.new_game()
        pygame.mixer.music.stop()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode in list(self.alfabeto):
                    self.click(event.unicode)

    def loop(self):
        self.new_game()
        while self.running:
            self.tela.fill((200, 200, 255))
            self.event_handler()
            self.blit()
            pygame.display.update()


Game().loop()
