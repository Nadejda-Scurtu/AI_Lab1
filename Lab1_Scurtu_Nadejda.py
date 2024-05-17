import pygame
import sys

class CubeWorld:
    def __init__(self, length, width, block_size=50):
        
        self.length = length
        self.width = width
        self.block_size = block_size  # Размер каждого блока
        self.gap = 2  # Размер промежутка между блоками
        self.matrix = [['0' for _ in range(width)] for _ in range(length)]
        self.log = []
        self.AND_OR_TREE = []

    def display_world(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (self.width * (self.block_size + self.gap) - self.gap, 
             self.length * (self.block_size + self.gap) - self.gap))
        pygame.display.set_caption("Cube World")

        # Шрифт для отображения номеров блоков
        font = pygame.font.Font(None, 24)  # None использует шрифт по умолчанию

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))  # Фон окна

            # Отрисовка блоков
            for y in range(self.length):
                for x in range(self.width):
                    if self.matrix[y][x] != '0':
                        block_color = (0, 128, 255)  # Синий цвет для блоков
                        text = font.render(self.matrix[y][x], True, (255, 255, 255))  # Белый текст
                    else:
                        block_color = (255, 255, 255)  # Белый цвет для пустых мест
                        text = font.render('', True, (255, 255, 255))

                    pygame.draw.rect(
                        screen,
                        block_color,
                        (x * (self.block_size + self.gap),
                         y * (self.block_size + self.gap),
                         self.block_size,
                         self.block_size))

                    # Вывод номера блока на поверхности блока
                    text_rect = text.get_rect(center=(x * (self.block_size + self.gap) + self.block_size // 2,
                                                      y * (self.block_size + self.gap) + self.block_size // 2))
                    screen.blit(text, text_rect)

            pygame.display.flip()

        pygame.quit()
       

    def add_block(self, x, y, block_name):
      found_space = False
    
      # Пытаемся найти свободное место снизу вверх
      for current_level in range(self.length - 1, -1, -1):
        # Проверяем основную позицию и соседние слева и справа
        positions_to_check = [(current_level, y)]
        if y > 0:
            positions_to_check.append((current_level, y - 1))  # слева
        if y < self.width - 1:
            positions_to_check.append((current_level, y + 1))  # справа

        for pos_x, pos_y in positions_to_check:
            if self.matrix[pos_x][pos_y] == '0':  # Если нашли свободное место
                self.matrix[pos_x][pos_y] = block_name
                self.log.append(f"Вставка {block_name} в ячейку ({pos_x}, {pos_y})")
                self.AND_OR_TREE.append(f"Вставка {block_name} в ячейку ({pos_x}, {pos_y})")
                found_space = True
                break
        if found_space:
            break
    
      if not found_space:
        self.log.append(f"Невозможно вставить {block_name}, удаление блока.")
        print(f"Ошибка: Нет свободных ячеек для {block_name}, блок должен быть удален.")

    def save_logs_to_file(self):
        path = 'C:/Users/User/Desktop/PythonForLab/AI/log_and_tree.txt'
        with open('log_and_tree.txt', 'w') as file:
            file.write("Log Entries:\n")
            for log_entry in self.log:
                file.write(log_entry + "\n")
            file.write("\nAND-OR Tree Actions:\n")
            for tree_entry in self.AND_OR_TREE:
                file.write(tree_entry + "\n")

    def cmd_handler(self):
        questions = [f"Почему было выполнено: {action}?" for action in self.AND_OR_TREE]
        while True:
            print("\nДоступные вопросы:")
            for idx, question in enumerate(questions):
                print(f"{idx + 1}. {question}")
            print(f"{len(questions) + 1}. Выход")

            choice = input("Введите ваш выбор (номер): ")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(questions):
                    self.respond_to_question(questions[choice - 1])
                elif choice == len(questions) + 1:
                    print("Выход...")
                    break
                else:
                    print("Неверный выбор, пожалуйста, попробуйте снова.")
            else:
                print("Пожалуйста, введите число.")

    def respond_to_question(self, question):
        parts = question.split()
        action = " ".join(parts[3:-1])  # Извлекаем действие из вопроса

        if question.startswith("Почему было выполнено:"):
            for i, entry in enumerate(self.AND_OR_TREE):
                if action in entry:
                    # Если действие является первым, причину найти сложно
                    if i == 0:
                        print("Данная ячейка свободна")
                    else:
                        print(f"Потому что было выполнено: {self.AND_OR_TREE[i-1]}")
                    return
            print("Действие не найдено в логе.")
        else:
            print("Неизвестный тип вопроса.")


def main():
    length = int(input("Введите длину матрицы: "))
    width = int(input("Введите ширину матрицы: "))
    world = CubeWorld(length, width)
    n_blocks = int(input("Сколько блоков поместить в матрицу? "))

    for i in range(n_blocks):
        x = int(input(f"Введите X координату для блока{i+1}: "))
        y = int(input(f"Введите Y координату для блока{i+1}: "))
        block_name = f"B{i+1}"
        world.add_block(x, y, block_name)

    world.display_world()  
    world.cmd_handler()
    world.save_logs_to_file()

if __name__ == "__main__":
    main()
