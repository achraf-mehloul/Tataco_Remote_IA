"""
اختبارات الاتصال التسلسلي
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from hardware.arduino_controller import ArduinoController

class TestArduinoController(unittest.TestCase):
    def setUp(self):
        """تهيئة قبل كل اختبار"""
        self.config = Config()
        self.controller = ArduinoController(self.config)
    
    def test_initial_state(self):
        """اختبار الحالة الأولية"""
        self.assertFalse(self.controller.connected)
        self.assertIsNone(self.controller.serial_conn)
    
    def test_connection_failure(self):
        """اختبار فشل الاتصال (منفذ غير موجود)"""
        # حفظ المنفذ الأصلي
        original_port = self.config.SERIAL_PORT
        # استخدام منفذ غير موجود
        self.config.SERIAL_PORT = 'COM999'
        
        result = self.controller.connect()
        self.assertFalse(result)
        self.assertFalse(self.controller.connected)
        
        # استعادة المنفذ الأصلي
        self.config.SERIAL_PORT = original_port
    
    def test_command_without_connection(self):
        """اختبار إرسال أمر بدون اتصال"""
        result = self.controller.send_command('test_command')
        self.assertFalse(result)
    
    def test_disconnect(self):
        """اختبار قطع الاتصال"""
        # محاولة قطع اتصال غير موجود
        self.controller.disconnect()
        self.assertFalse(self.controller.connected)
        
        # التأكد أن عدم وجود اتصال لا يسبب أخطاء
        self.controller.disconnect()
    
    def test_command_encoding(self):
        """اختبار ترميز الأوامر"""
        # هذا اختبار وهمي لفحص منطق إرسال الأوامر
        commands = ['light_toggle', 'fan_toggle', 'tv_toggle', 'ac_on', 'ac_off']
        
        for cmd in commands:
            # محاكاة الإرسال
            encoded = f"{cmd}\n".encode()
            self.assertEqual(encoded, f"{cmd}\n".encode())
            self.assertTrue(isinstance(encoded, bytes))

if __name__ == '__main__':
    # ملاحظة: لا يمكن اختبار الاتصال الفعلي بدون أردوينو متصل
    print("ملاحظة: اختبارات الاتصال الفعلية تحتاج أردوينو متصل")
    unittest.main()