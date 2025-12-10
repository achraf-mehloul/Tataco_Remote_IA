"""
مدير التطبيق الرئيسي
"""

import cv2
import time
from config import Config
from vision.hand_tracker import HandTracker
from vision.gesture_detector import GestureDetector
from hardware.arduino_controller import ArduinoController
from ui.simple_gui import SimpleGUI
from utils.logger import setup_logger

class AppManager:
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger()
        
        # تهيئة المكونات
        self.hand_tracker = HandTracker(self.config)
        self.gesture_detector = GestureDetector(self.config)
        self.arduino = ArduinoController(self.config)
        self.gui = SimpleGUI(self.config)
        
        self.running = False
        self.last_gesture_time = 0
        
    def run(self):
        """تشغيل التطبيق الرئيسي"""
        self.running = True
        self.logger.info("بدء تشغيل التطبيق")
        
        # فتح الكاميرا
        cap = cv2.VideoCapture(self.config.CAMERA_ID)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.CAMERA_HEIGHT)
        
        if not cap.isOpened():
            self.logger.error("فشل فتح الكاميرا")
            return
        
        # الاتصال بالأردوينو
        if not self.arduino.connect():
            self.logger.warning("فشل الاتصال بالأردوينو، التشغيل بدون أجهزة")
        
        try:
            while self.running:
                # قراءة الإطار
                success, frame = cap.read()
                if not success:
                    break
                
                # تتبع اليد
                hands = self.hand_tracker.process_frame(frame)
                
                # اكتشاف الإيماءات
                current_gesture = None
                if hands:
                    current_gesture = self.gesture_detector.detect(hands[0])
                    
                    # التحكم في الأردوينو (مع منع التكرار)
                    if current_gesture and self._can_process_gesture():
                        self._handle_gesture(current_gesture)
                        self.last_gesture_time = time.time()
                
                # عرض النتيجة
                frame = self.gui.update(frame, hands, current_gesture)
                
                # إظهار الإطار
                cv2.imshow(self.config.UI_WINDOW_NAME, frame)
                
                # التحكم بالإيقاف
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord(' '):
                    self.gesture_detector.toggle_debug()
        
        finally:
            # تنظيف الموارد
            cap.release()
            cv2.destroyAllWindows()
            self.arduino.disconnect()
            self.logger.info("إيقاف التطبيق")
    
    def _can_process_gesture(self):
        """فحص إذا كان يمكن معالجة إيماءة جديدة"""
        current_time = time.time()
        return (current_time - self.last_gesture_time) > self.config.GESTURE_COOLDOWN
    
    def _handle_gesture(self, gesture):
        """معالجة الإيماءة المكتشفة"""
        self.logger.info(f"إيماءة مكتشفة: {gesture}")
        
        # تعيين الأوامر بناءً على الإيماءة
        commands = {
            'fist': 'light_toggle',
            'peace': 'fan_toggle',
            'ok': 'tv_toggle',
            'thumbs_up': 'ac_on',
            'thumbs_down': 'ac_off'
        }
        
        if gesture in commands:
            command = commands[gesture]
            self.arduino.send_command(command)
