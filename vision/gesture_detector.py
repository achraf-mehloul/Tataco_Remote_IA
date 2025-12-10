"""
اكتشاف الإيماءات البسيطة
"""

import math

class GestureDetector:
    def __init__(self, config):
        self.config = config
        self.debug_mode = False
        
        # نقاط معالم اليد
        self.TIP_IDS = [4, 8, 12, 16, 20]  # أطراف الأصابع
        self.PIP_IDS = [3, 6, 10, 14, 18]  # مفاصل منتصف الأصابع
    
    def detect(self, hand_landmarks):
        """اكتشاف الإيماءة من معالم اليد"""
        if len(hand_landmarks) < 21:
            return None
        
        # عد الأصابع المرفوعة
        fingers_up = self._count_fingers(hand_landmarks)
        
        # تحديد الإيماءة بناءً على عدد الأصابع
        if fingers_up == [0, 0, 0, 0, 0]:  # قبضة
            return 'fist'
        elif fingers_up == [1, 1, 0, 0, 0]:  # علامة النصر
            return 'peace'
        elif fingers_up == [0, 1, 1, 0, 0] and self._is_ok_gesture(hand_landmarks):
            return 'ok'
        elif fingers_up == [1, 0, 0, 0, 1]:  # إبهام لأعلى
            return 'thumbs_up'
        elif fingers_up == [0, 0, 0, 0, 1]:  # إبهام لأسفل
            return 'thumbs_down'
        
        return None
    
    def _count_fingers(self, landmarks):
        """عد الأصابع المرفوعة"""
        fingers = []
        
        # الإبهام (مقارنة مع السبابة)
        if landmarks[self.TIP_IDS[0]]['x'] < landmarks[self.TIP_IDS[0]-1]['x']:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # الأصابع الأربعة الأخرى
        for i in range(1, 5):
            if landmarks[self.TIP_IDS[i]]['y'] < landmarks[self.PIP_IDS[i]]['y']:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
    
    def _is_ok_gesture(self, landmarks):
        """فحص إذا كانت إيماءة OK"""
        # المسافة بين السبابة والإبهام
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        distance = math.sqrt(
            (thumb_tip['x'] - index_tip['x'])**2 +
            (thumb_tip['y'] - index_tip['y'])**2
        )
        
        return distance < 0.05  # عتبة المسافة
    
    def toggle_debug(self):
        """تبديل وضع التصحيح"""
        self.debug_mode = not self.debug_mode
        return self.debug_mode
