h = 45
r = 10.50

SUM = 0

if h > 40:
    SUM = (h - 40)*r*1.5
    SUM = SUM + r*40
else:
    SUM = r*h

print(SUM)