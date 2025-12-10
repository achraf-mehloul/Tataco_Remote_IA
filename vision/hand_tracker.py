"""
تتبع اليد باستخدام MediaPipe
"""

import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, config):
        self.config = config
        
        # إعداد MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.config.MAX_NUM_HANDS,
            min_detection_confidence=self.config.HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=self.config.HAND_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def process_frame(self, frame):
        """معالجة إطار وتتبع اليد"""
        # تحويل BGR إلى RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        # اكتشاف اليد
        results = self.hands.process(rgb_frame)
        
        # تحويل RGB إلى BGR مرة أخرى
        rgb_frame.flags.writeable = True
        
        hands_data = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # رسم معالم اليد
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # استخراج بيانات اليد
                hand_data = []
                for landmark in hand_landmarks.landmark:
                    hand_data.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z
                    })
                hands_data.append(hand_data)
        
        return hands_data
    
    def release(self):
        """تحرير الموارد"""
        self.hands.close()
