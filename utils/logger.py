"""
نظام تسجيل مبسط
"""

import logging

def setup_logger(name='Tataco'):
    """إعداد المسجل"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # معالج وحدة التحكم
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # تنسيق الرسائل
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # إضافة المعالج
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger
