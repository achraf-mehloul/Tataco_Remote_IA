"""
التحكم في الأردوينو عبر اتصال تسلسلي
"""

import serial
import time

class ArduinoController:
    def __init__(self, config):
        self.config = config
        self.serial_conn = None
        self.connected = False
        
    def connect(self):
        """الاتصال بالأردوينو"""
        try:
            self.serial_conn = serial.Serial(
                port=self.config.SERIAL_PORT,
                baudrate=self.config.BAUD_RATE,
                timeout=self.config.TIMEOUT
            )
            time.sleep(2)  # انتظار تهيئة الأردوينو
            self.connected = True
            print(f"تم الاتصال بالأردوينو على {self.config.SERIAL_PORT}")
            return True
        except Exception as e:
            print(f"فشل الاتصال بالأردوينو: {e}")
            return False
    
    def send_command(self, command):
        """إرسال أمر للأردوينو"""
        if not self.connected or not self.serial_conn:
            print(f"لم يتم الاتصال بالأردوينو، الأمر: {command}")
            return False
        
        try:
            # إرسال الأمر مع سطر جديد
            self.serial_conn.write(f"{command}\n".encode())
            print(f"تم إرسال الأمر: {command}")
            return True
        except Exception as e:
            print(f"فشل إرسال الأمر {command}: {e}")
            return False
    
    def disconnect(self):
        """قطع الاتصال"""
        if self.serial_conn and self.connected:
            self.serial_conn.close()
            self.connected = False
            print("تم قطع الاتصال بالأردوينو")
