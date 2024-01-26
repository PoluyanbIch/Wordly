import pygame
import random

pygame.init()

with open('dictionary.txt', encoding='utf-8') as f:
    WORDS = []
    for i in f.readlines():
        WORDS.append(i.strip())

field = [[None for k in range(5)] for _ in range(6)]
keyword_letters = {}

WIDTH, HEIGHT = 728, 800
LETTER_SIZE = 75
FONT = pygame.font.SysFont('arial', 40)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill('white')
COLORS = {-1: '#49423d', 0: 'grey', 1: '#f0c05a', 2: '#3caa3c'}


class Letter:
    def __init__(self, letter: str, position: tuple[int, int] | tuple[int, int, int, int], color=COLORS[0]):
        self.letter = letter
        self.position = position[:2]
        self.color = color
        if len(position) == 4:
            self.pos = position[2:]
        else:
            self.pos = (57, 75)

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, (self.position[0] - 15, self.position[1], LETTER_SIZE - 18, LETTER_SIZE),
                         border_radius=8)
        letter = FONT.render(self.letter, True, 'black')
        SCREEN.blit(letter, letter.get_rect(center=(self.position[0] + 13, self.position[1] + 40)))
        pygame.display.update()


def draw_keyboard():
    global keyword_letters
    x, y = 20, 550
    keyboard = ['ЙЦУКЕНГШЩЗХЪ', 'ФЫВАПРОЛДЖЭ', 'ЯЧСМИТЬБЮ']
    for string in keyboard:
        for letter in string:
            letter_object = Letter(letter, (x, y))
            letter_object.draw()
            keyword_letters[letter] = letter_object
            x += 60
        y += 80
        if string == keyboard[0]:
            x = 50
        elif string == keyboard[1]:
            x = 100


def draw_field():
    global field
    x, y = 200, 20
    for i in range(6):
        for j in range(5):
            # pygame.draw.rect(SCREEN, 'black', (x, y, 50, 60))
            cell = Letter('', (x, y, 50, 60), '#b0b7c6')
            cell.draw()
            field[i][j] = cell
            pygame.display.update()
            x += 70
        x = 200
        y += 90


def delete(pos: tuple[int, int] | list[int]):
    global field
    cell = field[pos[0]][pos[1]]
    cell.letter = ''
    cell.draw()
    pygame.display.update()


def create(letter: str, pos: tuple[int, int] | list[int], color=None):
    global field
    cell = field[pos[0]][pos[1]]
    cell.letter = letter
    if color is not None:
        cell.color = color
    cell.draw()
    pygame.display.update()


def check_word(answer: str, word: str, index: int) -> bool:
    global keyword_letters
    word = word.upper()
    answer = answer.upper()
    result = [0 for _ in range(5)]
    num_of_letters = {}
    for letter in answer:
        if letter not in num_of_letters:
            num_of_letters[letter] = 1
        else:
            num_of_letters[letter] += 1
    for i in range(len(word)):
        if answer[i].lower() == word[i].lower():
            create(word[i], (index, i), COLORS[2])
            cell = keyword_letters[word[i]]
            cell.color = COLORS[2]
            cell.draw()
            pygame.display.update()
            result[i] = 2
            num_of_letters[word[i]] -= 1

    for i in range(len(word)):
        if word[i] in answer and result[i] != 2 and num_of_letters[word[i]] > 0:
            create(word[i], (index, i), COLORS[1])
            cell = keyword_letters[word[i]]
            if cell.color != COLORS[2]:
                cell.color = COLORS[1]
                cell.draw()
                pygame.display.update()
            result[i] = 1
            num_of_letters[word[i]] -= 1
    for i in range(len(word)):
        if result[i] == 0:
            create(word[i], (index, i), COLORS[-1])
        if result[i] == 0 and keyword_letters[word[i]].color not in (COLORS[1], COLORS[2]):
            keyword_letters[word[i]].color = COLORS[-1]
            keyword_letters[word[i]].draw()
            pygame.display.update()
    return answer.lower() == word.lower()


if __name__ == '__main__':
    is_running = True
    pause = False
    cursor_pos = [0, 0]
    # answer = random.choice(WORDS)
    answer = 'курок'
    cur_word = ''
    draw_keyboard()
    draw_field()
    while is_running:
        if len(cur_word) == 5:
            t = check_word(answer, cur_word, cursor_pos[0])
            cur_word = ''
            if cursor_pos[0] < 5 and not t:
                cursor_pos[0] += 1
                cursor_pos[1] = 0
            else:
                pause = True
                while pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                pause = False
                                cursor_pos = [0, 0]
                                answer = random.choice(WORDS)
                                cur_word = ''
                                draw_keyboard()
                                draw_field()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if cursor_pos[1] > 0:
                        cursor_pos[1] -= 1
                        delete(cursor_pos)
                        cur_word = cur_word[:-1]
                else:
                    key = event.unicode.lower()
                    if key in 'йцукенгшщзхъфывапролджэячсмитьбю' and key != '':
                        key = key.upper()
                        create(key, cursor_pos)
                        cur_word += key
                        cursor_pos[1] += 1
