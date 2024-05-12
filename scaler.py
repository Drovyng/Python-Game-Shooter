data = [(232, 342), (573, 335), (591, 319), (822, 321), (834, 338), (856, 349), (883, 346), (941, 364), (933, 386), (948, 397), (946, 423), (910, 442), (966, 540), (954, 563), (882, 583), (868, 570), (834, 458), (778, 450), (735, 417), (690, 419), (692, 463), (590, 451), (588, 423), (478, 418), (466, 429), (282, 431), (265, 416), (249, 413), (247, 388), (269, 370), (230, 371)]

minX = 1000
minY = 1000
maxX = 0
maxY = 0

for i in data:
    x, y = i
    
    minX = min(minX, x)
    minY = min(minY, y)
    maxX = max(maxX, x)
    maxY = max(maxY, y)
        
newPoses = []
scale = max((maxX - minX) / 150, (maxY - minY) / 150)
for i in data:
    x, y = i
    x -= minX
    y -= minY
    
    x /= scale
    y /= scale
    
    newPoses.append((int(x), int(y)))
    
maxX = 0
maxY = 0

for i in newPoses:
    x, y = i
    
    maxX = max(maxX, x)
    maxY = max(maxY, y)
    
final = []
for i in newPoses:
    x, y = i
    final.append((660 - maxX + int(x), 660 - maxY + int(y)))
    
print(final)