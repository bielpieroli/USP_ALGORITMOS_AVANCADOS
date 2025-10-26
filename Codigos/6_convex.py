import math

def crossProduct(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def squaredDistance(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def convexHullWithCollinear(points):
    n = len(points)
    if n < 3:
        return points
    
    points = sorted(set(map(tuple, points)))
    n = len(points)
    
    if n < 3:
        return list(points)

    lower = []
    for point in points:
        while len(lower) >= 2 and crossProduct(lower[-2], lower[-1], point) <= 1e-9: 
            lower.pop()
        lower.append(point)
    
    upper = []
    for point in reversed(points):
        while len(upper) >= 2 and crossProduct(upper[-2], upper[-1], point) <= 1e-9: 
            upper.pop()
        upper.append(point)
    
    lower.pop()
    upper.pop()
    
    hull = lower + upper
    
    return list(hull)

def convexHullGrahamScan(points):
    n = len(points)
    if n < 3:
        return points
    
    points = sorted(list(set(map(tuple, points))))
    n = len(points)
    
    if n < 3:
        return list(points)
    
    allCollinear = True
    if n >= 2:
        p0 = points[0]
        p1 = points[-1]
        for i in range(1, n - 1):
            if abs(crossProduct(p0, p1, points[i])) > 1e-9:
                allCollinear = False
                break
    
    if allCollinear:
        return list(points)
    
    return convexHullWithCollinear(points)

def main():
    numTests = int(input())
    
    for caseNumber in range(1, numTests + 1):
        try:
            numPoints = int(input())
        except EOFError:
            break
            
        pointList = []
        
        for _ in range(numPoints):
            try:
                line = input().split()
                x, y = float(line[0]), float(line[1])
                pointList.append((x, y))
            except EOFError:
                break
        
        hull = convexHullGrahamScan(pointList)
        
        if hull:
            startIndex = 0
            for i in range(1, len(hull)):
                if hull[i][0] < hull[startIndex][0]:
                    startIndex = i

                elif abs(hull[i][0] - hull[startIndex][0]) < 1e-9:
                    if hull[i][1] < hull[startIndex][1]:
                        startIndex = i
            
            hull = hull[startIndex:] + hull[:startIndex]
        
        print(f"Caso {caseNumber}:")
        print(f"Tamanho do colar: {len(hull)}")
        print("Pedras ancestrais: ", end="")
        
        for i, (x, y) in enumerate(hull):
            print(f"({x:.4f},{y:.4f})", end="")
            if i < len(hull) - 1:
                print(",", end="")
        print()
        print()

if __name__ == "__main__":
    main()