"""
واجهة مستخدم بسيطة باستخدام OpenCV
"""

import cv2
import time

class SimpleGUI:
    def __init__(self, config):
        self.config = config
        self.fps_start_time = time.time()
        self.fps_counter = 0
        self.current_fps = 0
        
    def update(self, frame, hands, gesture):
        """تحديث الواجهة"""
        self.fps_counter += 1
        
        # حساب FPS
        if time.time() - self.fps_start_time >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_start_time = time.time()
        
        # إضافة معلومات للعرض
        self._add_overlay(frame, hands, gesture)
        
        return frame
    
    def _add_overlay(self, frame, hands, gesture):
        """إضافة معلومات على الإطار"""
        h, w, _ = frame.shape
        
        # عرض FPS
        if self.config.UI_SHOW_FPS:
            cv2.putText(frame, f"FPS: {self.current_fps}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # عرض عدد الأيدي
        cv2.putText(frame, f"Hands: {len(hands)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # عرض الإيماءة
        if self.config.UI_SHOW_GESTURE and gesture:
            cv2.putText(frame, f"Gesture: {gesture}", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # إضافة تعليمات
        cv2.putText(frame, "Press 'q' to quit | 'SPACE' to toggle debug", 
                   (w - 400, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # إضافة حدود
        cv2.rectangle(frame, (0, 0), (w, h), (50, 50, 50), 2)
