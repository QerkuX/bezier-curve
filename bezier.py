import pygame
pygame.init()

# Creating the window
window_size = [1000, 1000]
window = pygame.display.set_mode((window_size[0], window_size[1]))
pygame.display.set_caption("Bezier curve generator")

# Pretty much the quality of the bezier curve (bigger the variable = better quality)
step_count = 200

point_size = 1

# There is always one point more than lines and two points more than bezier curves, this information is useless by the way
points = [
    [0, 0],
    [250, 500],
    [500, 250],
    [720, 500],
    [1000, 250]
]

# Generates linear function (y = m * x + b) for every pair of points
def generate_line_variables(p0, p1):
    # m = (y1 - y0) / (x1 - x0)
    # Checks the steepness of the line (0 - horizontal | infinite - vertical)
    try:
        m = (p1[1] - p0[1]) / (p1[0] - p0[0])
    except:
        return ["infinite", 0]

    # b = -m * x + y
    b = -1 * m * p0[0] + p0[1]

    return [m, b]

# Creates points for every line
def linear_function(p0, p1):
    m, b = generate_line_variables(p0, p1)
    line_points = []

    # This entire thing below only checks the smallest possible rectangle that the line will fit in (peak of optimization)

    # The if speaks for itself tbh (this only happens when the line is fully vertical)
    if m == "infinite":
        for y in range(min(p0[1], p1[1]), max(p0[1], p1[1]) + 1):
            line_points.append([p0[0], round(y)])

        if p1[1] < p0[1]: return line_points[::-1]
        return line_points

    # Checks if line is more horizontal than vertical
    if abs(m) <= 1:
        for x in range(min(p0[0], p1[0]), max(p0[0], p1[0]) + 1):
            y = m * x + b
            line_points.append([x, round(y)])

        if p1[0] < p0[0]: return line_points[::-1]
        return line_points

    # This happens when the line is more vertical than horizontal
    for y in range(min(p0[1], p1[1]), max(p0[1], p1[1]) + 1):
        x = (-1 * b + y) / m
        line_points.append([round(x), y])

    if p1[1] < p0[1]: return line_points[::-1]
    return line_points

def generate_bezier_curve(points):
    lines = []
    bezier = []

    # Creates points of every line
    for i in range(len(points)-1):
        lines.append(linear_function(points[i], points[i+1]))

    # Creates points for every bezier curve
    for i in range(len(points)-2):
        # Hard to explain, it just makes that the steps are equal in both lines so that they end at the same time. Also we divide the lines by two so that the curve transition is smooth
        if i == 0:
            first_line_ratio = len(lines[i]) / step_count
        else:
            first_line_ratio = int(len(lines[i]) / 2) / step_count

        if i == len(points)-3:
            second_line_ratio = len(lines[i+1]) / step_count
        else:
            second_line_ratio = int(len(lines[i+1]) / 2) / step_count

        bezier_points = []
        for step in range(0, step_count-1):
            first_line_index = int(step * first_line_ratio)
            if not i == 0: first_line_index += round(len(lines[i]) / 2)
            second_line_index = int(step * second_line_ratio)

            step_line = linear_function(lines[i][first_line_index], lines[i+1][second_line_index])
            if len(step_line) == 0: continue

            # The same thing as with the other ratios, I just didnt created the variable because it wouldnt be reused
            bezier_points.append(step_line[int(step * len(step_line) / step_count)])

        # Fixes the gap between two curves
        if not i == len(points)-3: bezier_points.append(lines[i+1][int(len(lines[i+1]) / 2) - 1])

        bezier.append(bezier_points)

    # Prints every line and bezier curve
    for line in lines:
        for point in line:
            pygame.draw.circle(window, (100, 0, 0), (point[0], point[1]), point_size)

    for curve in bezier:
        for point in curve:
            pygame.draw.circle(window, (0, 255, 0), (point[0], point[1]), point_size)


selected_point = 0

# Change this to move at a different speed
speed = 5

run = True
while run:
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # This entire thing is a mess so good luck understanding that, but its not the part of the bezier generator so i dont care
        if event.type == pygame.KEYDOWN:
            try:
                number = int(pygame.key.name(event.key))
                if number == 0: number = 10
                if number <= len(points): selected_point = number-1
            except:
                if pygame.key.name(event.key) == "=" and len(points) < 10:
                    selected_point = len(points)
                    points.append([0, 0])
                if pygame.key.name(event.key) == "-" and len(points) > 2:
                    points.pop()
                    if selected_point >= len(points): selected_point = len(points)-1

    # Moves the point
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        points[selected_point][1] -= speed
    if keys[pygame.K_DOWN]:
        points[selected_point][1] += speed
    if keys[pygame.K_LEFT]:
        points[selected_point][0] -= speed
    if keys[pygame.K_RIGHT]:
        points[selected_point][0] += speed

    # Makes sure that the points dont go out of the screen
    points[selected_point][1] = max(0, points[selected_point][1]) and min(window_size[1], points[selected_point][1])
    points[selected_point][0] = max(0, points[selected_point][0]) and min(window_size[0], points[selected_point][0])
    generate_bezier_curve(points)
    pygame.display.update()

pygame.quit()

#Instruction:
#Press "+" to add the point, "-" to remove it
#Press the corresponding number on the keyboard to select a point
#Use arrows to move selected point