from wx import Point


def save_map(path, begin: Point, end: Point, obst: list):
    with open(path, "w+") as obst_map:
        obst_map.write(str(begin.x) + " " + str(begin.y) + "\n")
        obst_map.write(str(end.x) + " " + str(end.y) + "\n")
        for i in obst:
            for j in i:
                obst_map.write("(" + str(j.x) + ", " + str(j.y) + ");")
            obst_map.write("\n")


def load_map(path):
    with open(path, "r") as obst_map:
        data = obst_map.readline().split()
        begin_point = Point(int(data[0]), int(data[1]))
        data = obst_map.readline().split()
        end_point = Point(int(data[0]), int(data[1]))
        data = obst_map.readline()
        obstacles = []
        while data != "":
            data = data.strip().split(sep=";")
            data = [i.strip("(),").split(sep=", ") for i in data[:-1]]
            data = [Point(int(i[0]), int(i[1])) for i in data]
            obstacles.append(data)
            data = obst_map.readline()

        return begin_point, end_point, obstacles









