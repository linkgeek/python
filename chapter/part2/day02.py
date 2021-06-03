ret = 1 != 1 or 8 < 1 and 6 > 3
print(ret) # false


# 给定一个成绩分数,判断学生成绩等级,A至E,其中:
# 90分以上为'A',80-89分为'B,70-79分为'C',60-69分为'D',60分以下为'E'

score = 87.5
if score >= 80:
    if score >= 90:
        print("成绩等级：A")
    else:
        print("成绩等级：B")
elif score >= 60:
    if score >= 70:
        print("成绩等级：C")
    else:
        print("成绩等级：D")
else:
    print("成绩等级：E")