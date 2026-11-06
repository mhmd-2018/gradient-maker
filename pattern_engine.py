"""
موتور اصلی تولید بک‌گراند و پترن
"""

import numpy as np
from PIL import Image, ImageDraw
import random
from typing import Tuple, List, Optional
from enum import Enum

class PatternStyle(Enum):
    ABSTRACT = "abstract"
    GRADIENT = "gradient"
    TEXTURE = "texture"
    SEAMLESS = "seamless"

class PatternEngine:
    """موتور تولید پترن با تنظیمات کامل"""
    
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        self.image = None
        self.draw = None
        
    def set_resolution(self, width: int, height: int):
        """تنظیم رزولوشن خروجی"""
        self.width = width
        self.height = height
        
    def create_canvas(self, bg_color: Tuple[int, int, int] = (255, 255, 255)):
        """ایجاد بوم خالی"""
        self.image = Image.new('RGB', (self.width, self.height), bg_color)
        self.draw = ImageDraw.Draw(self.image)
        return self.image
    
    def generate_random_color(self, base_colors: Optional[List[Tuple[int, int, int]]] = None) -> Tuple[int, int, int]:
        """تولید رنگ تصادفی با کیفیت بالا"""
        if base_colors and len(base_colors) >= 2:
            # ترکیب دو رنگ از پالت
            color1 = random.choice(base_colors)
            color2 = random.choice(base_colors)
            t = random.random()
            return tuple(int(color1[i] * (1-t) + color2[i] * t) for i in range(3))
        
        # تولید رنگ شاد و زنده
        hue = random.random()
        saturation = 0.6 + random.random() * 0.4
        value = 0.7 + random.random() * 0.3
        
        # تبدیل HSV به RGB
        from colorsys import hsv_to_rgb
        rgb = hsv_to_rgb(hue, saturation, value)
        return tuple(int(c * 255) for c in rgb)
    
    def add_noise(self, intensity: float = 0.05):
        """افزودن نویز ظریف به تصویر"""
        if self.image is None:
            return
        
        img_array = np.array(self.image)
        noise = np.random.randint(0, int(255 * intensity), img_array.shape, dtype=np.uint8)
        img_array = np.clip(img_array.astype(int) + noise, 0, 255).astype(np.uint8)
        self.image = Image.fromarray(img_array)
        self.draw = ImageDraw.Draw(self.image)
    
    def apply_blur(self, radius: int = 2):
        """اعمال سایه‌روشن برای زیبایی بیشتر"""
        from PIL import ImageFilter
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius=radius))
        self.draw = ImageDraw.Draw(self.image)
    
    def get_image(self) -> Image.Image:
        """دریافت تصویر نهایی"""
        return self.image
    
    def save(self, path: str, quality: int = 95):
        """ذخیره تصویر با کیفیت بالا"""
        if self.image:
            self.image.save(path, 'PNG', quality=quality)
            return True
        return False