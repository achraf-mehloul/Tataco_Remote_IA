"""
إعدادات MVP v0.4
"""

class Config:
    # إعدادات الكاميرا
    CAMERA_ID = 0
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    CAMERA_FPS = 30
    
    # إعدادات اليد
    HAND_DETECTION_CONFIDENCE = 0.7
    HAND_TRACKING_CONFIDENCE = 0.7
    MAX_NUM_HANDS = 1
    
    # إعدادات الاتصال التسلسلي
    SERIAL_PORT = 'COM3'  # Windows
    # SERIAL_PORT = '/dev/ttyUSB0'  # Linux
    # SERIAL_PORT = '/dev/tty.usbserial'  # Mac
    BAUD_RATE = 9600
    TIMEOUT = 1
    
    # إعدادات الريلاي
    RELAY_PINS = {
        'light': 2,
        'fan': 3,
        'tv': 4,
        'ac': 5
    }
    
    # إعدادات الإيماءات
    GESTURE_THRESHOLD = 0.8
    GESTURE_COOLDOWN = 1.0  # ثانية
    
    # إعدادات الواجهة
    UI_WINDOW_NAME = "Tataco Remote v0.4"
    UI_SHOW_FPS = True
    UI_SHOW_GESTURE = True
