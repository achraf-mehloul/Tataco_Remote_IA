"""
دوال مساعدة
"""

import numpy as np

def normalize_coordinates(x, y, width, height):
    """تطبيع الإحداثيات"""
    return x / width, y / height

def calculate_distance(point1, point2):
    """حساب المسافة بين نقطتين"""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def is_clockwise(points):
    """فحص إذا كانت النقاط في اتجاه عقارب الساعة"""
    if len(points) < 3:
        return False
    
    sum_val = 0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        sum_val += (x2 - x1) * (y2 + y1)
    
    return sum_val > 0
