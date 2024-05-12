import keyboard, mouse

points = []

def addPoint():
    global points
    points.append(mouse.get_position())

def stopAll():
    global points
    print(points)

keyboard.on_press_key("\\", lambda lol: addPoint())
keyboard.on_press_key("j", lambda lol: stopAll())

while True:
    pass