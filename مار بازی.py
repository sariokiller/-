import turtle
import time
import random

# صفحه بازی را راه‌اندازی کنید
wn = turtle.Screen()
wn.title("بازی مار")
wn.bgcolor("light blue")  # تغییر رنگ پس‌زمینه به آبی روشن
wn.setup(width=600, height=600)
wn.tracer(0)  # خاموش کردن به‌روزرسانی‌های صفحه برای انیمیشن نرم‌تر

# تنظیمات اولیه
delay = 0.1
score = 0
high_score = 0
segments = []  # لیست برای نگهداری بخش‌های بدن مار

# ایجاد سر مار
head = turtle.Turtle()
head.shape("square")
head.color("white")
head.speed(0)  # تنظیم سرعت به حداکثر
head.penup()  # جلوگیری از کشیدن خط توسط لاک‌پشت
head.goto(0, 0)  # موقعیت شروع مار
head.direction = "Stop"  # جهت اولیه

# ایجاد غذا
food = turtle.Turtle()
colors = random.choice(['red', 'orange', 'black'])  # رنگ تصادفی برای غذا
shapes = random.choice(['square', 'triangle', 'circle'])  # شکل تصادفی برای غذا
food.shape(shapes)
food.color(colors)
food.penup()  # جلوگیری از کشیدن خط توسط لاک‌پشت
food.goto(0, 100)  # موقعیت اولیه غذا

# نمایش امتیاز
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()  # پنهان کردن آیکون لاک‌پشت
pen.goto(0, 260)  # موقعیت برای نمایش امتیاز
pen.write("امتیاز: 0 بالاترین امتیاز: 0", align="center", font=("candara", 24, "bold"))

# توابع برای حرکت مار
def goup():
    if head.direction != "down":  # جلوگیری از حرکت مار به سمت مخالف
        head.direction = "up"

def godown():
    if head.direction != "up":
        head.direction = "down"

def goleft():
    if head.direction != "right":
        head.direction = "left"

def goright():
    if head.direction != "left":
        head.direction = "right"

# تابع برای حرکت سر مار
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)  # حرکت به سمت بالا به اندازه 20 واحد
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)  # حرکت به سمت پایین به اندازه 20 واحد
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)  # حرکت به سمت چپ به اندازه 20 واحد
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)  # حرکت به سمت راست به اندازه 20 واحد

# تابع برای اضافه کردن بخش به بدن مار
def add_segment():
    new_segment = turtle.Turtle()
    new_segment.shape("square")
    new_segment.color("grey")
    new_segment.penup()
    segments.append(new_segment)

# تنظیمات کلیدها برای کنترل مار
wn.listen()
wn.onkeypress(goup, "w")  # حرکت به بالا با 'W'
wn.onkeypress(godown, "s")  # حرکت به پایین با 'S'
wn.onkeypress(goleft, "a")  # حرکت به چپ با 'A'
wn.onkeypress(goright, "d")  # حرکت به راست با 'D'

# حلقه اصلی بازی
while True:
    wn.update()  # به‌روزرسانی صفحه
    move()

    # بررسی برخورد با غذا
    if head.distance(food) < 20:  # اگر سر با غذا برخورد کند
        # تغییر موقعیت غذا
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)
        
        # اضافه کردن بخش به بدن مار
        add_segment()
        
        # به‌روزرسانی امتیاز
        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write("امتیاز: {} بالاترین امتیاز: {}".format(score, high_score), align="center", font=("candara", 24, "bold"))

    # بررسی برخورد با دیواره‌ها
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)  # توقف به مدت یک ثانیه
        head.goto(0, 0)  # بازنشانی موقعیت
        head.direction = "Stop"  # متوقف کردن مار
        colors = random.choice(['red', 'blue', 'purple'])  # تغییر رنگ غذا
        shapes = random.choice(['square', 'circle'])  # تغییر شکل غذا
        for segment in segments:  # حرکت تمام بخش‌ها به خارج از دید
            segment.goto(1000, 1000)
        segments.clear()  # پاک کردن لیست بخش‌ها
        score = 0  # بازنشانی امتیاز
        delay = 0.1  # بازنشانی تاخیر

    pen.goto(0, 260)
    pen.write("امتیاز: {} بالاترین امتیاز: {}".format(score, high_score), align="center", font=("candara", 24, "bold"))

    # بررسی برخورد با بدن خود
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)
    
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    for segment in segments:
        if segment.distance(head) < 20:  # اگر سر با هر بخش برخورد کند
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "Stop"
