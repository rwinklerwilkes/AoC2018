from aocd import get_data
import re

data = get_data(year=2018, day=10)
example_data = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""

def parse_line(line):
    line_regex = r'position=<(\s*-{0,1}[0-9]+),(\s*-{0,1}[0-9]+)> velocity=<(\s*-{0,1}[0-9]+),(\s*-{0,1}[0-9]+)>'
    groups = re.match(line_regex,line).groups()
    position = (int(groups[0]),int(groups[1]))
    velocity = (int(groups[2]),int(groups[3]))
    return position, velocity

def parse_data(data):
    all_parsed_data = [parse_line(line) for line in data.split('\n')]
    position = [p[0] for p in all_parsed_data]
    velocity = [p[1] for p in all_parsed_data]
    return position, velocity

def get_data_at_t(position, velocity, t):
    x_at_t = [p[0] + velocity[i][0] * t for i, p in enumerate(position)]
    y_at_t = [p[1] + velocity[i][1] * t for i, p in enumerate(position)]
    return x_at_t, y_at_t

def get_bounding_box(position, velocity, t):
    x_at_t, y_at_t = get_data_at_t(position, velocity, t)
    minx = min(x_at_t)
    maxx = max(x_at_t)
    miny = min(y_at_t)
    maxy = max(y_at_t)
    area = (maxx-minx)*(maxy-miny)
    return minx, maxx, miny, maxy, area

def find_time_with_min_area(position, velocity):
    t = 0
    min_area = None
    done = False
    while not done:
        minx, maxx, miny, maxy, area = get_bounding_box(position, velocity, t)
        if min_area is None or area < min_area:
            min_area = area
            t += 1
        else:
            t -= 1
            done = True
    return t

def plot_data(x, y):
    minx = min(x)
    assert minx >= 0
    maxx = max(x)
    miny = min(y)
    assert miny >= 0
    maxy = max(y)
    plot = [[' ' for i in range(maxx + 1)] for j in range(maxy + 1)]
    for xi, yi in zip(x, y):
        plot[yi][xi] = '*'
    for i in plot:
        print(''.join(i))

def part_one(data, part_one = True):
    position, velocity = parse_data(data)
    t = find_time_with_min_area(position, velocity)
    x_at_t, y_at_t = get_data_at_t(position, velocity, t)
    if part_one:
        plot_data(x_at_t, y_at_t)
    else:
        print(t)

part_one(example_data)
part_one(data)

part_one(data, False)