"""
اختبارات وحدة اكتشاف الإيماءات
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from vision.gesture_detector import GestureDetector

class TestGestureDetector(unittest.TestCase):
    def setUp(self):
        """تهيئة قبل كل اختبار"""
        self.config = Config()
        self.detector = GestureDetector(self.config)
        
        # إنشاء بيانات يد وهمية
        self.mock_landmarks = []
        for i in range(21):
            self.mock_landmarks.append({
                'x': i * 0.05,
                'y': i * 0.05,
                'z': 0.0
            })
    
    def test_fist_detection(self):
        """اختبار اكتشاف القبضة"""
        # محاكاة قبضة (جميع الأصابع مطوية)
        fist_landmarks = self.mock_landmarks.copy()
        # تعديل مواضع أطراف الأصابع لتكون أسفل المفاصل
        for i in [8, 12, 16, 20]:  # أطراف السبابة، الوسطى، البنصر، الخنصر
            fist_landmarks[i]['y'] = 0.6  # أسفل المفاصل
        fist_landmarks[4]['x'] = 0.4  # الإبهام مطوي
        
        gesture = self.detector.detect(fist_landmarks)
        self.assertEqual(gesture, 'fist')
    
    def test_peace_detection(self):
        """اختبار اكتشاف علامة النصر"""
        peace_landmarks = self.mock_landmarks.copy()
        # السبابة والوسطى مرفوعتان
        peace_landmarks[8]['y'] = 0.3  # السبابة
        peace_landmarks[12]['y'] = 0.3  # الوسطى
        # البنصر والخنصر مطويان
        peace_landmarks[16]['y'] = 0.6
        peace_landmarks[20]['y'] = 0.6
        # الإبهام مرفوع
        peace_landmarks[4]['x'] = 0.2
        
        gesture = self.detector.detect(peace_landmarks)
        self.assertEqual(gesture, 'peace')
    
    def test_thumbs_up_detection(self):
        """اختبار اكتشاف الإبهام لأعلى"""
        thumbs_up_landmarks = self.mock_landmarks.copy()
        # الإبهام مرفوع
        thumbs_up_landmarks[4]['x'] = 0.1
        # السبابة مطوية
        thumbs_up_landmarks[8]['y'] = 0.6
        
        gesture = self.detector.detect(thumbs_up_landmarks)
        self.assertEqual(gesture, 'thumbs_up')
    
    def test_invalid_landmarks(self):
        """اختبار معالم يد غير صالحة"""
        # معالم غير كافية
        short_landmarks = self.mock_landmarks[:10]
        gesture = self.detector.detect(short_landmarks)
        self.assertIsNone(gesture)
        
        # معالم فارغة
        empty_landmarks = []
        gesture = self.detector.detect(empty_landmarks)
        self.assertIsNone(gesture)
    
    def test_toggle_debug(self):
        """اختبار تبديل وضع التصحيح"""
        initial_state = self.detector.debug_mode
        self.detector.toggle_debug()
        self.assertNotEqual(initial_state, self.detector.debug_mode)
        
        # العودة للحالة الأصلية
        self.detector.toggle_debug()
        self.assertEqual(initial_state, self.detector.debug_mode)

if __name__ == '__main__':
    unittest.main()
