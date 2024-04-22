from random import choice, randint

import pygame as pg

# Инициализация PyGame:
pg.init()

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
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


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
        raise NotImplementedError('<реализация только в дочерних классах>')

    def draw_one(self, position, color=None):
        """Метод отрисовывает яблоко на экране, а также голову змейки
        на экране и дополняется в классе Snake.
        """
        color = color or self.body_color
        if color is None:
            return
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Атрибуты и методы класса обеспечивают логику и координаты
    отрисовки яблока
    """

    def __init__(self, namber_of_snake_body=CENTER, body_color=APPLE_COLOR):
        """Метод инициализирует базовые атрибуты объекта (позиция и цвет)"""
        super().__init__(body_color=body_color)
        self.randomize_position(namber_of_snake_body)

    def randomize_position(self, namber_of_snake_body):
        """Метод устанавливает случайное положение яблока
        на игровом поле — задаёт атрибуту position новое значение
        """
        while True:
            self.position = [randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE]
            if self.position not in namber_of_snake_body:
                break

    def draw(self):
        """Метод отрисовывает яблоко на экране"""
        self.draw_one(self.position)


class Snake(GameObject):
    """Атрибуты и методы класса обеспечивают логику движения, отрисовку,
    обработку событий (нажатие клавиши) и другие аспекты поведения
    змейки в игре.
    """

    def __init__(self, body_color=SNAKE_COLOR, direction=RIGHT):
        """Метод инициализирует начальное состояние змейки"""
        super().__init__(body_color=body_color)
        self.reset()
        self.direction = direction   # По условию задания, начало в вправо

    def draw(self):
        """Метод отрисовывает змейку на экране, затирая след"""
        # Отрисовка головы змейки
        self.draw_one(self.get_head_position(), self.body_color)
        """
        После модификации когда, в определённых условиях, при приближении
        головы к телу, в теле появляются дыры, думаю
        этот кусок позволил бы избежать данной ошибки.
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        """
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращает координаты первого элемента, в списке координат,
        из которых состоит змея
        """
        return self.positions[0]

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
        self.new_head_position = [((head_position[0] + self.direction[0]
                                  * GRID_SIZE) % SCREEN_WIDTH),
                                  ((head_position[1] + self.direction[1]
                                   * GRID_SIZE) % SCREEN_HEIGHT)]
        if self.length == len(self.positions):
            self.last = self.positions[-1]
            self.positions.pop()  # Удаляем сегмент
            self.positions.insert(0, self.new_head_position)

    def eat_aple(self):
        """Метод позволит обновить длину змеи, после поедания яблока"""
        self.positions.insert(0, self.new_head_position)  # Добавляем сегмент
        self.namber_of_snake_body = self.positions

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние после
        столкновения с собой.
        """
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.last = None
        self.next_direction = None
        self.namber_of_snake_body = self.positions


def main():
    """В функции происходит обновление состояний объектов:
    змейка обрабатывает нажатия клавиш и двигается в соответствии
    с выбранным направлением.
    """
    litle_snake = Snake()
    random_apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(litle_snake)
        litle_snake.update_direction()
        if random_apple.position == litle_snake.get_head_position():
            litle_snake.eat_aple()
            litle_snake.length += 1
            random_apple.randomize_position(litle_snake.positions)
        elif litle_snake.get_head_position() in litle_snake.positions[3:]:
            litle_snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        litle_snake.move()
        random_apple.draw()
        litle_snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
