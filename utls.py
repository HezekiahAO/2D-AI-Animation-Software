x_1 = 100
x_2 = 200
y_1 = 800
y_2 = 900

def mid_point(x1, y1, x2, y2):
    mid_x = (float(x1) + float(x2)) / 2
    mid_y = (float(y1) + float(y2)) / 2
    return mid_x, mid_y

print(mid_point(x_1, y_1, x_2, y_2))