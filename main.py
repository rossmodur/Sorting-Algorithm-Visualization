import pygame
import random
import math

pygame.init()

class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (39, 174, 96)   
    RED = (231, 76, 60)     
    BACKGROUND_COLOR = (30, 30, 30)  

    GRADIENTS = [
        (52, 152, 219),
        (41, 128, 185),
        (31, 97, 141)
    ]

    FONT = pygame.font.SysFont('times_new_roman', 30)
    LARGE_FONT = pygame.font.SysFont('times_new_roman', 40)

    SIDE_PAD = 200
    TOP_PAD = 250  

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.start_x = (self.width - (self.block_width * len(lst))) // 2
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = (50, 50, 50)
        self.hover_color = (70, 70, 70)
    
    def draw(self, win, font):
        pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(pos) else self.base_color
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        pygame.draw.rect(win, DrawInformation.WHITE, self.rect, 2, border_radius=8)
        text_surface = font.render(self.text, True, DrawInformation.WHITE)
        win.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                  self.rect.y + (self.rect.height - text_surface.get_height()) // 2))


class Slider:
    def __init__(self, x, y, width, min_val, max_val, start_val):
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.handle_radius = 10
        self.dragging = False

    def draw(self, win, font):
        track_rect = pygame.Rect(self.x, self.y - 4, self.width, 8)
        pygame.draw.rect(win, (100, 100, 100), track_rect, border_radius=4)
        handle_x = self.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
        pygame.draw.circle(win, (255, 0, 0), (handle_x, self.y), self.handle_radius)
        pygame.draw.circle(win, DrawInformation.WHITE, (handle_x, self.y), self.handle_radius, 2)
        text = font.render(f"Elements: {self.value}", True, DrawInformation.WHITE)
        win.blit(text, (self.x + self.width + 20, self.y - text.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            handle_x = self.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
            if math.sqrt((mouse_x - handle_x) ** 2 + (mouse_y - self.y) ** 2) <= self.handle_radius:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, _ = event.pos
                mouse_x = max(self.x, min(self.x + self.width, mouse_x))
                ratio = (mouse_x - self.x) / self.width
                self.value = int(self.min_val + ratio * (self.max_val - self.min_val))


def draw(draw_info, algo_name, ascending, buttons, slider):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", True, DrawInformation.WHITE)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 20))
    for button in buttons:
        button.draw(draw_info.window, draw_info.FONT)
    slider.draw(draw_info.window, draw_info.FONT)
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (0, draw_info.TOP_PAD, draw_info.width, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = DrawInformation.GRADIENTS[i % len(DrawInformation.GRADIENTS)]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if (lst[j] > lst[j + 1] and ascending) or (lst[j] < lst[j + 1] and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: DrawInformation.GREEN, j + 1: DrawInformation.RED}, True)
                yield True
    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: DrawInformation.GREEN, i: DrawInformation.RED}, True)
            yield True
    return lst


def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    def merge_sort_recursive(left, right):
        if right - left > 1:
            mid = (left + right) // 2
            yield from merge_sort_recursive(left, mid)
            yield from merge_sort_recursive(mid, right)
            yield from merge(left, mid, right)
    def merge(left, mid, right):
        L = lst[left:mid]
        R = lst[mid:right]
        i = 0
        j = 0
        k = left
        while i < len(L) and j < len(R):
            if (L[i] <= R[j] and ascending) or (L[i] >= R[j] and not ascending):
                lst[k] = L[i]
                i += 1
            else:
                lst[k] = R[j]
                j += 1
            k += 1
            draw_list(draw_info, {k-1: DrawInformation.RED}, True)
            yield True
        while i < len(L):
            lst[k] = L[i]
            i += 1
            k += 1
            draw_list(draw_info, {k-1: DrawInformation.RED}, True)
            yield True
        while j < len(R):
            lst[k] = R[j]
            j += 1
            k += 1
            draw_list(draw_info, {k-1: DrawInformation.RED}, True)
            yield True
    yield from merge_sort_recursive(0, len(lst))
    return lst


def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst
    def quick_sort_recursive(low, high):
        if low < high:
            pivot_index = yield from partition(low, high)
            yield from quick_sort_recursive(low, pivot_index - 1)
            yield from quick_sort_recursive(pivot_index + 1, high)
    def partition(low, high):
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: DrawInformation.GREEN, j: DrawInformation.RED}, True)
                yield True
        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i+1: DrawInformation.GREEN, high: DrawInformation.RED}, True)
        yield True
        return i + 1
    yield from quick_sort_recursive(0, len(lst) - 1)
    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    min_val_num = 0
    max_val_num = 100

    initial_elements = 250
    lst = generate_starting_list(initial_elements, min_val_num, max_val_num)
    draw_info = DrawInformation(900, 700, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    buttons = []
    button_width = 150
    button_height = 50
    spacing = 20

    total_width_row1 = 4 * button_width + 3 * spacing
    start_x_row1 = (draw_info.width - total_width_row1) // 2
    row1_y = 80
    buttons.append(Button(start_x_row1, row1_y, button_width, button_height, "Reset"))
    buttons.append(Button(start_x_row1 + button_width + spacing, row1_y, button_width, button_height, "Start"))
    buttons.append(Button(start_x_row1 + 2 * (button_width + spacing), row1_y, button_width, button_height, "Ascending"))
    buttons.append(Button(start_x_row1 + 3 * (button_width + spacing), row1_y, button_width, button_height, "Descending"))

    total_width_row2 = 4 * button_width + 3 * spacing
    start_x_row2 = (draw_info.width - total_width_row2) // 2
    row2_y = row1_y + button_height + 20
    buttons.append(Button(start_x_row2, row2_y, button_width, button_height, "Insertion"))
    buttons.append(Button(start_x_row2 + button_width + spacing, row2_y, button_width, button_height, "Bubble"))
    buttons.append(Button(start_x_row2 + 2 * (button_width + spacing), row2_y, button_width, button_height, "Merge"))
    buttons.append(Button(start_x_row2 + 3 * (button_width + spacing), row2_y, button_width, button_height, "Quick"))

    
    slider_width = 300
    slider_x = (draw_info.width - slider_width) // 2
    slider_y = row2_y + button_height + 40
    slider = Slider(slider_x, slider_y, slider_width, 100, 500, initial_elements)

    prev_slider_value = slider.value

    while run:
        clock.tick(60)

        if not sorting and slider.value != prev_slider_value:
            n = slider.value
            lst = generate_starting_list(n, min_val_num, max_val_num)
            draw_info.set_list(lst)
            prev_slider_value = slider.value

        if sorting:
            steps_per_frame = max(1, slider.value // 50)
            for _ in range(steps_per_frame):
                try:
                    next(sorting_algorithm_generator)
                except StopIteration:
                    sorting = False
                    break
        else:
            draw(draw_info, sorting_algo_name, ascending, buttons, slider)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            slider.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(pos):
                        if button.text == "Reset":
                            n = slider.value
                            lst = generate_starting_list(n, min_val_num, max_val_num)
                            draw_info.set_list(lst)
                            sorting = False
                        elif button.text == "Start" and not sorting:
                            sorting = True
                            sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                        elif button.text == "Ascending" and not sorting:
                            ascending = True
                        elif button.text == "Descending" and not sorting:
                            ascending = False
                        elif button.text == "Insertion" and not sorting:
                            sorting_algorithm = insertion_sort
                            sorting_algo_name = "Insertion Sort"
                        elif button.text == "Bubble" and not sorting:
                            sorting_algorithm = bubble_sort
                            sorting_algo_name = "Bubble Sort"
                        elif button.text == "Merge" and not sorting:
                            sorting_algorithm = merge_sort
                            sorting_algo_name = "Merge Sort"
                        elif button.text == "Quick" and not sorting:
                            sorting_algorithm = quick_sort
                            sorting_algo_name = "Quick Sort"

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
