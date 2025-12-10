"""
معالج الاتصال التسلسلي
"""

import serial
import time
import threading
from queue import Queue

class SerialHandler:
    def __init__(self, config):
        self.config = config
        self.serial_conn = None
        self.connected = False
        self.command_queue = Queue()
        self.response_queue = Queue()
        self.read_thread = None
        self.running = False
        
    def connect(self):
        """الاتصال بالأجهزة التسلسلية"""
        try:
            self.serial_conn = serial.Serial(
                port=self.config.SERIAL_PORT,
                baudrate=self.config.BAUD_RATE,
                timeout=self.config.TIMEOUT,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            
            time.sleep(2)  # انتظار تهيئة الجهاز
            self.connected = True
            
            # بدء خيط القراءة
            self.running = True
            self.read_thread = threading.Thread(target=self._read_serial)
            self.read_thread.daemon = True
            self.read_thread.start()
            
            print(f"تم الاتصال بنجاح على {self.config.SERIAL_PORT}")
            return True
            
        except serial.SerialException as e:
            print(f"خطأ في الاتصال التسلسلي: {e}")
            return False
        except Exception as e:
            print(f"خطأ غير متوقع: {e}")
            return False
    
    def send_command(self, command, wait_for_response=False, timeout=2):
        """إرسال أمر والانتظار للرد إذا طلب"""
        if not self.connected or not self.serial_conn:
            print(f"لم يتم الاتصال، الأمر: {command}")
            return None
        
        try:
            # إضافة سطر جديد للأمر
            full_command = f"{command}\n"
            self.serial_conn.write(full_command.encode())
            print(f"تم إرسال: {command}")
            
            if wait_for_response:
                return self._wait_for_response(timeout)
            return True
            
        except Exception as e:
            print(f"فشل إرسال الأمر {command}: {e}")
            return None
    
    def _read_serial(self):
        """قراءة البيانات الواردة من المنفذ التسلسلي"""
        while self.running and self.connected:
            try:
                if self.serial_conn and self.serial_conn.in_waiting > 0:
                    response = self.serial_conn.readline().decode().strip()
                    if response:
                        self.response_queue.put(response)
                        print(f"رد وارد: {response}")
                
                time.sleep(0.01)  # منع استهلاك وحدة المعالجة المركزية
                
            except Exception as e:
                print(f"خطأ في قراءة المنفذ التسلسلي: {e}")
                time.sleep(0.1)
    
    def _wait_for_response(self, timeout):
        """الانتظار لرد من المنفذ التسلسلي"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if not self.response_queue.empty():
                return self.response_queue.get()
            time.sleep(0.01)
        
        return None
    
    def get_latest_response(self):
        """الحصول على أحدث رد"""
        if not self.response_queue.empty():
            return self.response_queue.get()
        return None
    
    def clear_queues(self):
        """مسح الطوابير"""
        while not self.command_queue.empty():
            self.command_queue.get()
        while not self.response_queue.empty():
            self.response_queue.get()
    
    def disconnect(self):
        """قطع الاتصال وإيقاف الخيوط"""
        self.running = False
        
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.join(timeout=1)
        
        if self.serial_conn and self.connected:
            self.serial_conn.close()
            self.connected = False
        
        self.clear_queues()
        print("تم قطع الاتصال التسلسلي")
