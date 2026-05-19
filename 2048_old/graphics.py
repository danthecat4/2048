import pygame

# Colours
BG_COLOR = (130, 125, 115)
#GRID_COLOR = (0, 0, 255)
EMPTY_TILE_COLOR = (50, 50, 50)

# original 2048 colour scheme
# TILE_COLORS = {
#     2:  (238, 228, 218),
#     4:  (237, 224, 200),
#     8:  (242, 177, 121),
#     16: (245, 149, 99),
#     32: (246, 124, 95),
#     64: (246, 94, 59),
#     128: (237, 207, 114),
#     256: (237, 204, 97),
#     512: (237, 200, 80),
#     1024: (237, 197, 63),
#     2048: (237, 194, 46),
# }

#my alternative colour scheme
TILE_COLORS = {
    2:  (240, 230, 230),
    4:  (242, 230, 200),
    8:  (243, 230, 140),
    16: (245, 232, 70),
    32: (245, 228, 55),
    64: (245, 225, 40),
    128: (245, 220, 35),
    256: (245, 214, 25),
    512: (248, 210, 20),
    1024: (250, 205, 0),
    2048: (250, 225, 0),
}

TILE_SIZE = 120
GAP = 10


def draw_grid(screen, grid, font):
    screen.fill(BG_COLOR)

    for r in range(4):
        for c in range(4):
            value = grid[r][c]

            x = 300 + c * (TILE_SIZE + GAP) + GAP
            y = 30+ r * (TILE_SIZE + GAP) + GAP
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

            # Background tile
            color = TILE_COLORS.get(value, EMPTY_TILE_COLOR)
            pygame.draw.rect(screen, color, rect, border_radius=8)

            # Draw numbers
            if value != 0:
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)