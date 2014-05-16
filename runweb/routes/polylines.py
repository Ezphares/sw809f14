from routes.gpolyline import decode as depoly
from math import sqrt, cos, radians

''' NOTE:
The points in this script should be given as (longitude, latitude), as opposed to LatLng objects from google
'''


'''
Some math taken from 
http://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
'''
def sqr(x):
    return x * x

def dist2(p1, p2):
    return sqr(p1[0] - p2[0]) + sqr(p1[1] - p2[1])

def distToSegmentSquared(point, start, end):
    l2 = dist2(start, end)
    if l2 == 0:
        return 0

    t = ((point[0] - start[0]) * (end[0] - start[0]) + (point[1] - start[1]) * (end[1] - start[1])) / l2
    if t < 0:
        return dist2(point, start)
    elif t > 1:
        return dist2(point, end)
    else:
        return dist2(point, (start[0] + t * (end[0] - start[0]),
                             start[1] + t * (end[1] - start[1])) )
'''
And some from wikipedia http://en.wikipedia.org/wiki/Decimal_degrees
'''
def metersToDecimalDegrees(meters, point):
    degsize = 111319.9 * cos(radians(point[1]))
    return meters / degsize

class Segment(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    '''
    Distance from segment to a point. This is done in Euclidian geometry, using decimal degrees, so small imprecisions are expected
    '''
    def point_distance(self, point):
        return sqrt(distToSegmentSquared(point, self.start, self.end))

class Polyline(object):
    def __init__(self, encoded):
        self.points = depoly(encoded)
        
    def point_distance(self, point):
        distance = float('inf')
        for segment in self.get_segments():
            d = segment.point_distance(point)
            if (d < distance):
                distance = d
        return distance
        
    def get_segments(self):
        segments = []
        for i in range(len(self.points) - 1):
            segments.append(Segment(self.points[i], self.points[i + 1]))
        return segments
        
    def on_route(self, point, threshold = 50):
        return self.point_distance(point) <= metersToDecimalDegrees(threshold, point)
        
    '''
    Current is index of current point, 0 at start of run
    Returns (<new point index>, <total points>, <finish reached>)
    '''
    def advance(self, current, point, threshold = 50):
        advancing = True
        while advancing:
            next = current + 1
            if next >= len(self.points):
                return (next, next, True)
            
            if sqrt(dist2(point, self.points[next])) <= metersToDecimalDegrees(threshold, point):
                current = next
            else:
                advancing = False
        
        return (current, len(self.points), False)
                
