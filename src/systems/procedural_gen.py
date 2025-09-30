import random
def generate_map(width, height):
    # grid cheia de paredes '#', abrimos caminhos '.'
    grid = [['#' for _ in range(width)] for _ in range(height)]
    x, y = width//2, height//2
    for _ in range(width * height * 3):
        grid[y][x] = '.'
        dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        x = max(1, min(width-2, x+dx))
        y = max(1, min(height-2, y+dy))
    return grid
