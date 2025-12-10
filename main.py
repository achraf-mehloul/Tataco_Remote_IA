"""
نقطة البداية الرئيسية للتطبيق
"""

import cv2
import sys
from core.app_manager import AppManager

def main():
    """الدالة الرئيسية"""
    print("تشغيل Tataco Remote MVP v0.4")
    
    try:
        # إنشاء مدير التطبيق
        app = AppManager()
        
        # تشغيل التطبيق
        app.run()
        
    except KeyboardInterrupt:
        print("\nتم إيقاف التطبيق بواسطة المستخدم")
    except Exception as e:
        print(f"حدث خطأ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
