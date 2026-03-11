import random
from tkinter import *

with open('values.txt', 'a') as f:
    f.write("\n Experiment: ")


def rgb_to_hex(r, g, b):
    return '{:X}{:X}{:X}'.format(r, g, b)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))


def new_day():
    global loops, day, number_blobs, all_blob_list, blob_img, blob, food, food_grabs, speed_average, deaths, food_grabs_dict, color_start
    if loops == 10:
        loops = 0
        day = day + 1
        day_label.config(text="Dia: " + str(day))
        for food in food_list:
            canvas.delete(food)
        food_list.clear()
        for x in range(number_food):
            food = canvas.create_image(random.randint(1, 50) * 10, random.randint(1, 50) * 10, image=food_img)
            food_list.append(food)
        for blob in all_blob_list:
            if food_grabs_dict[blob] > 1:
                for _ in range(food_grabs_dict[blob]-1):
                    x = canvas.coords(blob)[0] + 4
                    y = canvas.coords(blob)[1] + 4
                    blob = canvas.create_rectangle(x - 4, y - 4, x + 4, y + 4,
                                                   fill=canvas.itemcget(blob, "fill"), tags="blob")
                    all_blob_list.append(blob)
                    food_grabs_dict[blob] = 1
                    speed = speed_average + random.randint(-80, 80)
                    root.after(100, move, [blob], speed)
            if food_grabs_dict[blob] < 1:
                deaths = deaths + 1
                canvas.delete(blob)
        all_blob_list = [blob for blob in all_blob_list if food_grabs_dict[blob] > 0]
        food_grabs_dict = {blob: 0 for blob in all_blob_list}
        number_blobs = food_grabs
        blobs_label.config(text="Nombre d'individus: " + str(number_blobs))
        deaths = 0
        food_grabs = 0
        for blob in all_blob_list:
            if 'reproduced' in canvas.gettags(blob):
                print(str(blob) + "off cooldown")
                canvas.dtag(blob, 'reproduced')
        with open('values.txt', 'a') as f:
            f.write(str("       Dia:  "+str(day) + " - Nombre individus: " + str(number_blobs)))
            f.write(str(" Speed: " + str(speed_average)))


def move(blob_list, delay):
    global loops, day, number_blobs, all_blob_list, blob_img, blob, food, food_grabs, speed_average, food_grabs_dict
    new_day()
    for blob in blob_list:
        direction = random.randint(1, 4)
        if direction == 1 and (canvas.coords(blob)[0]+4) < 500:
            canvas.move(blob, +10, 0)
        elif direction == 2 and (canvas.coords(blob)[0]+4) > 10:
            canvas.move(blob, -10, 0)
        elif direction == 3 and (canvas.coords(blob)[1]+4) < 500:
            canvas.move(blob, 0, +10)
        elif direction == 4 and (canvas.coords(blob)[1]+4) > 10:
            canvas.move(blob, 0, -10)
        else:
            canvas.move(blob, 0, 0)
    for food in food_list:
        if canvas.coords(blob)[0]+4 == canvas.coords(food)[0] and canvas.coords(blob)[1]+4 == canvas.coords(food)[1]:
            canvas.delete(food)
            food_list.remove(food)
            food_grabs = food_grabs + 1
            food_grabs_dict[blob] = food_grabs_dict[blob] + 1
            if speed_average + int(float(delay-speed_average)/10) > 70:
                speed_average = speed_average + int(float(delay-speed_average)/10)
    if 'reproduced' not in canvas.gettags(blob):
        if len(canvas.find_overlapping(canvas.coords(blob)[0], canvas.coords(blob)[1],
                                       canvas.coords(blob)[2], canvas.coords(blob)[3])) == 2 and \
                canvas.gettags(canvas.find_overlapping(canvas.coords(blob)[0], canvas.coords(blob)[1],
                                                       canvas.coords(blob)[2], canvas.coords(blob)[3])[0] + \
                               canvas.find_overlapping(canvas.coords(blob)[0], canvas.coords(blob)[1],
                                                       canvas.coords(blob)[2], canvas.coords(blob)[3])[
                                   1] - blob) == ('blob',):
            parent2 = canvas.find_overlapping(canvas.coords(blob)[0], canvas.coords(blob)[1],
                                              canvas.coords(blob)[2], canvas.coords(blob)[3])[0] + \
                      canvas.find_overlapping(canvas.coords(blob)[0], canvas.coords(blob)[1],
                                              canvas.coords(blob)[2], canvas.coords(blob)[3])[1] - blob
            canvas.addtag_overlapping('reproduced', canvas.coords(blob)[0], canvas.coords(blob)[1],
                                      canvas.coords(blob)[2], canvas.coords(blob)[3])
            print("CHILD!!")
            x = canvas.coords(blob)[0] + 4
            y = canvas.coords(blob)[1] + 4
            rgb1 = hex_to_rgb(canvas.itemcget(blob, "fill"))
            rgb2 = hex_to_rgb(canvas.itemcget(parent2, "fill"))
            rgb = [int((rgb1[0] + rgb2[0]) / 2), int((rgb1[1] + rgb2[1]) / 2), int((rgb1[2] + rgb2[2]) / 2)]
            color_direction = random.randint(1, 3)
            if color_direction == 1:
                color_addition = random.randint(0, 100)
                if rgb[0] + color_addition < 255 and rgb[0] - color_addition > 0:
                    rgb[0] = rgb[0] + color_addition
            elif color_direction == 2:
                color_addition = random.randint(0, 100)
                if rgb[1] + color_addition < 255 and rgb[0] - color_addition > 0:
                    rgb[1] = rgb[1] + color_addition
            elif color_direction == 3:
                color_addition = random.randint(0, 100)
                if rgb[2] + color_addition < 255 and rgb[0] - color_addition > 0:
                    rgb[2] = rgb[2] + color_addition
            hex_value = "#" + str(rgb_to_hex(rgb[0], rgb[1], rgb[2]))
            blob = canvas.create_rectangle(x - 4, y - 4, x + 4, y + 4, fill=hex_value,
                                           tags="blob")
            all_blob_list.append(blob)
            blobs_label.config(text="Nombre d'individus: " + str(number_blobs + 1))
            food_grabs_dict[blob] = 0
            speed = speed_average + random.randint(-80, 80)
            root.after(200, move, [blob], speed)


    root.after(delay, move, blob_list, delay)


def move_everyone():
    for blob in all_blob_list:
        food_grabs_dict[blob] = 0
        speed = speed_average + random.randint(-80, 80)
        root.after(100, move, [blob], speed)


def clock():
    global loops, start
    if start == 0:
        move_everyone()
    start = 1
    loops = loops + 1
    root.after(1000, clock)


root = Tk()
root.title("Simulació de l'evolució d'una espècie: Test 1")
root.iconbitmap("assets/icon.ico")
blob_img = PhotoImage(file="assets/blob.png")
food_img = PhotoImage(file="assets/food.png")

color_start = "#888888"
coordinates = 0
deaths = 0
food_grabs = 0
loops = 0
day = 1
speed = 1
number_blobs = 5
number_food = 100
speed_average = 200
start = 0
food_grabs_dict = {}
all_blob_list = []
food_list = []
reaper_list = []

canvas = Canvas(root, width=506, height=506, bg="white")
canvas.pack(pady=20, padx=20)
day_label = Label(root, text="Dia: "+str(day))
day_label.pack()
blobs_label = Label(root, text="Nombre d'individus: "+str(number_blobs))
blobs_label.pack()

for _ in range(number_blobs):
    x = random.randint(1, 50) * 10
    y = random.randint(1, 50) * 10
    blob = canvas.create_rectangle(x-4, y-4, x+4, y+4, fill=color_start, tags="blob")
    all_blob_list.append(blob)

for y in range(number_food):
    food = canvas.create_image(random.randint(1, 50) * 10, random.randint(1, 50) * 10, image=food_img)
    food_list.append(food)


clock()

root.mainloop()
