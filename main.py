"""
AI Pattern Generator - برنامه حرفه‌ای تولید بک‌گراند و پترن
ورودی اصلی برنامه
"""

import sys
import os

# اضافه کردن مسیر جاری به PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui import AIPatternGeneratorUI

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     🎨 AI Pattern Generator - نسخه 1.0                   ║
    ║     تولید حرفه‌ای بک‌گراند و پترن با هوش مصنوعی ساده    ║
    ║                                                          ║
    ║     توسط: تیم برنامه‌نویسی                              ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app = AIPatternGeneratorUI()
    app.run()