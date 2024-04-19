from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Это базовый класс, от которого наследуются другие игровые объекты.
    Он содержит общие атрибуты игровых объектов — эти атрибуты
    описывают позицию и цвет объекта. Этот же класс содержит и заготовку
    метода для отрисовки объекта на игровом поле
    """

    def __init__(self, body_color=None):
        self.body_color = body_color
        self.position = CENTER

    def draw(self):
        """Это абстрактный метод, который предназначен для переопределения
        в дочерних классах и должен определять, как объект будет
        отрисовываться на экране.
        """
        pass


class Apple(GameObject):
    """Атрибуты и методы класса обеспечивают логику и координаты
    отрисовки яблока
    """

    def __init__(self, body_color=APPLE_COLOR):
        """Метод инициализирует базовые атрибуты объекта (позиция и цвет)"""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Метод устанавливает случайное положение яблока
        на игровом поле — задаёт атрибуту position новое значение
        """
        self.position = [randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE]

    # Метод draw класса Apple
    def draw(self):
        """Метод отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Атрибуты и методы класса обеспечивают логику движения, отрисовку,
    обработку событий (нажатие клавиши) и другие аспекты поведения
    змейки в игре.
    """

    def __init__(self, body_color=SNAKE_COLOR, direction=RIGHT):
        """Метод инициализирует начальное состояние змейки"""
        super().__init__()
        self.next_direction = None
        self.body_color = body_color
        self.direction = direction
        self.positions = [CENTER]
        self.length = 1

    def draw(self):
        """Метод отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращает координаты первого элемента, в списке координат,
        из которых состоит змея
        """
        head_position = self.positions[0]
        return head_position

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод перезаписывает значение змеи, делает проверку на выход
        за границы экрана, на укус себя, удаляет последний элемент змеи
        если змея съела яблоко
        """
        head_position = self.get_head_position()
        new_position_high = head_position[1] + self.direction[1] * GRID_SIZE
        new_position_widh = head_position[0] + self.direction[0] * GRID_SIZE
        new_head_position = [new_position_widh, new_position_high]
        if new_head_position[0] >= SCREEN_WIDTH:  # Выход за границы экрана
            new_head_position[0] = 0
        elif new_head_position[0] < 0:
            new_head_position[0] = SCREEN_WIDTH
        if new_head_position[1] >= SCREEN_HEIGHT:  # Выход за границы экрана
            new_head_position[1] = 0
        elif new_head_position[1] < 0:
            new_head_position[1] = SCREEN_HEIGHT
        if self.length == len(self.positions):
            self.last = self.positions[-1]
            self.positions.pop()  # Сначала удаляем сегмент
            self.positions.insert(0, new_head_position)  # Добавляем сегмент
        else:
            self.positions.insert(0, new_head_position)  # Добавляем сегмент

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние после
        столкновения с собой.
        """
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.last = None


def main():
    """В функции происходит обновление состояний объектов:
    змейка обрабатывает нажатия клавиш и двигается в соответствии
    с выбранным направлением.
    """
    random_apple = Apple()
    litle_snake = Snake()
    while True:
        clock.tick(3)
        handle_keys(litle_snake)
        litle_snake.update_direction()
        litle_snake.move()
        if random_apple.position == litle_snake.get_head_position():
            litle_snake.length += 1
            while True:
                random_apple.randomize_position()
                if random_apple.position not in litle_snake.positions:
                    break
        elif litle_snake.get_head_position() in litle_snake.positions[3:]:
            litle_snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        random_apple.draw()
        litle_snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
