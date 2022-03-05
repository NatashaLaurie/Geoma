import matplotlib.pyplot as plt
import random

from lab2.Point import Point


def init_points(xs: list, ys: list) -> list:
    points = []
    for i in range(len(xs)):
        x = Point(xs[i], ys[i])
        points.append(x)
    return points


def draw_polygon(points: list):
    for i in range(len(points) - 1):
        plt.plot([points[i].x, points[i + 1].x], [points[i].y, points[i + 1].y])


def draw_point(point: Point):
    plt.scatter(point.x, point.y)


def draw_line(p1: Point, p2: Point):
    plt.plot([p1.x, p2.x], [p1.y, p2.y])


# Определитель матрицы
def det(a, b, c, d):
    return a * d - b * c


# Пересекаются ли прямые P1P2 и P3P4
def are_intersected(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    d1 = det(p4.x - p3.x, p4.y - p3.y, p1.x - p3.x, p1.y - p3.y)
    d2 = det(p4.x - p3.x, p4.y - p3.y, p2.x - p3.x, p2.y - p3.y)
    d3 = det(p2.x - p1.x, p2.y - p1.y, p3.x - p1.x, p3.y - p1.y)
    d4 = det(p2.x - p1.x, p2.y - p1.y, p4.x - p1.x, p4.y - p1.y)

    if d1 * d2 <= 0 and d3 * d4 <= 0:
        return True
    else:
        return False


# Положение точки Р0 к прямой Р1Р2
def get_point_position_to_line(p0: Point, p1: Point, p2: Point) -> str:
    d = det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y)
    if d > 0:
        return 'left'
    elif d < 0:
        return 'right'
    else:
        return 'on the line'


# Проходит ли прямая P0Q через сторону многоугольника
def ptest(p0: Point, points: list) -> bool:
    for i in range(len(points) - 1):
        if get_point_position_to_line(p0, points[i], points[i + 1]) == 'on the line':
            return True
    return False


# Минимальный Х
def get_min_x(points: list):
    minX = points[0].x
    for i in range(len(points)):
        if (points[i].x < minX):
            minX = points[i].x
    return minX


# Положение точки относительно многоугольника
def check_point_position(initialPoint: Point, points: list) -> bool:
    q = Point(get_min_x(points) - 1, initialPoint.y)
    draw_point(q)
    plt.annotate("Q", (q.x + 0.1, q.y + 0.1))
    plt.annotate("P0", (initialPoint.x + 0.1, initialPoint.y + 0.1))
    draw_line(initialPoint, q)
    s = 0

    for i in range(len(points) - 1):
        # пересекается ли со стороной
        if are_intersected(points[i], points[i + 1], q, initialPoint):
            # если пересекается то проверяем пересечение по вершине многоугольника
            if (not get_point_position_to_line(points[i], q, initialPoint) == 'on the line' and
                    not get_point_position_to_line(points[i + 1], q, initialPoint) == 'on the line'):
                # если нет, то счетчик пересечений увеличиваем
                s += 1
                # если по вершине то запускаем счетчик вершин лежащих на p0q
            elif get_point_position_to_line(points[i], q, initialPoint) == 'on the line':
                k = 0
                while get_point_position_to_line(points[i + k], q, initialPoint) == 'on the line':
                    k += 1
                    # далее находим вершину которая уже не лежит на п0кю
                    # проверяем если вершина последняя перед вершиной в которой пересечение и
                    # первая вершина уже не лежащая на п0кю лежат по одну сторону прямой п0кю
                if (not get_point_position_to_line(points[i - 1], q, initialPoint) ==
                        get_point_position_to_line(points[i + k], q, initialPoint) and
                        not get_point_position_to_line(points[i - 1], q, initialPoint) == 'on the line' and
                        not get_point_position_to_line(points[i + k], q, initialPoint) == 'on the line'):
                    s += 1
                i += k

    if s % 2 == 0:
        return False
    else:
        return True


def init():
    plt.grid(True)  # линии вспомогательной сетки

    xs = [1, 3, 1, 5, 6, 7, 8, 9, 10, 8, 7, 6, 5, 4, 1]  # координаты вершин многоугольника
    ys = [1, 5, 9, 10, 8, 9, 8, 11, 6, 3, 4, 2, 4, 2, 1]
    points = init_points(xs, ys)
    # initialPoint = Point(random.random() * 12, random.random() * 12)  # получение случайных к-т в диапазоне от 0 до 12
    initialPoint = Point(6, 9)
    q = Point(get_min_x(points) - 1, initialPoint.y)  # точка, лежащая слева от многоугольника

    draw_polygon(points)
    draw_point(initialPoint)

    if not check_point_position(initialPoint, points):
        plt.suptitle('Снаружи', fontsize=14)
    elif ptest(initialPoint, points):
        plt.suptitle('Внутри', fontsize=14)
    elif check_point_position(initialPoint, points):
        plt.suptitle('Внутри', fontsize=14)

    plt.show()


init()
