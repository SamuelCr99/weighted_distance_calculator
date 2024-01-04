import pygame
import random 
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import pygame_widgets

ROWS = 10
COLS = 10
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
node_width = WINDOW_WIDTH / COLS
grid_screen = True
node_id_count = 0
text_boxes_available = False
text_boxes = []

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)

class Node:
    def __init__(self, row, col):
        global node_id_count
        self.row = row
        self.col = col
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # Create a random color for node
        self.node_id = node_id_count
        node_id_count += 1

class OwnTextBox:
    def __init__(self, node1, node2, screen, x_pos, y_pos):
        self.node1 = node1
        self.node2 = node2
        tb = TextBox(screen, x_pos - 18, y_pos - 12, WINDOW_HEIGHT/COLS/3, WINDOW_HEIGHT/COLS/3, fontSize=12)
        tb.setText("1")
        self.tb = tb

def draw_grid(screen, width, height, rows, cols):
    for i in range(rows):
        pygame.draw.line(screen, (0, 0, 0), (0, i * height / rows), (width, i * height / rows))
    for i in range(cols):
        pygame.draw.line(screen, (0, 0, 0), (i * width / cols, 0), (i * width / cols, height))

def draw_nodes(screen, nodes):
    for node in nodes:
        x_pos = node.col * WINDOW_HEIGHT / COLS + WINDOW_HEIGHT/COLS/2
        y_pos = node.row * WINDOW_HEIGHT / ROWS + WINDOW_HEIGHT/ROWS/2
        pygame.draw.circle(screen, node.color, (x_pos, y_pos), WINDOW_HEIGHT/COLS/4)
        text = font.render(str(node.node_id), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (x_pos, y_pos)
        screen.blit(text, textRect)



def draw_set_weights_screen(screen, nodes):
    global text_boxes_available
    global text_boxes
    for i, node in enumerate(nodes): 
        # Draw x axis
        x_pos = WINDOW_HEIGHT/(len(nodes)+1) * (i+1)
        y_pos = 20
        pygame.draw.circle(screen, node.color, (x_pos, y_pos), WINDOW_HEIGHT/COLS/8)
        text = font.render(str(node.node_id), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (int(x_pos), y_pos)
        screen.blit(text, textRect)

        # Draw y axis
        x_pos = 20
        y_pos = WINDOW_HEIGHT/(len(nodes)+1) * (i+1)
        pygame.draw.circle(screen, node.color, (x_pos, y_pos), WINDOW_HEIGHT/COLS/8)
        text = font.render(str(node.node_id), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (x_pos, int(y_pos))
        screen.blit(text, textRect)

    # Crate a textbox for each cell in the matrix
    for i, node in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if node.node_id < node2.node_id:
                x_pos = WINDOW_WIDTH/(len(nodes)+1) * (i+1)
                y_pos = WINDOW_HEIGHT/(len(nodes)+1) * (j+1)
                text_boxes.append(OwnTextBox(node, node2, screen, x_pos, y_pos))

def calculate_weighted_distance():
    weighted_distance = 0
    for tb in text_boxes:
        # Calculate weighted distance using Manhattan distance
        distance = abs(tb.node1.row - tb.node2.row) + abs(tb.node1.col - tb.node2.col)
        weighted_distance += distance * int(tb.tb.getText())
    print(f"Weighted distace: {weighted_distance}")

def set_grid_screen():
    global grid_screen
    grid_screen = not grid_screen

def main():
    global text_boxes_available
    global text_boxes
    pygame.display.set_caption('Weighted distance calculator')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    nodes = []

    Button(screen, WINDOW_WIDTH - 450, WINDOW_WIDTH - 70, 200, 50, text='Switch mode', onClick=lambda: set_grid_screen())
    Button(screen, WINDOW_HEIGHT - 250, WINDOW_WIDTH - 70, 200, 50, text='Calculate weighted distance', onClick=lambda: calculate_weighted_distance())

    while running:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # Press space
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pos = pygame.mouse.get_pos()
                row = pos[1] // (WINDOW_WIDTH / ROWS)
                col = pos[0] // (WINDOW_HEIGHT / COLS)
                nodes.append(Node(row, col))

        if grid_screen:
            if text_boxes_available:
                for tb in text_boxes:
                    tb.tb.hide()
                text_boxes_available = False
                text_boxes = []
            screen.fill((255, 255, 255))
            draw_grid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, ROWS, COLS)
            draw_nodes(screen, nodes)

        elif not text_boxes_available:
                screen.fill((255, 255, 255))
                draw_set_weights_screen(screen, nodes)
                text_boxes_available = True

        pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
        pygame.display.update()

if __name__ == '__main__':
    main()
