"""
تولید بافت‌های مختلف: کاغذ، پارچه، نویز ظریف
"""

import numpy as np
from PIL import Image, ImageFilter
from typing import Tuple, Optional
import random

class TextureMaker:
    """ساخت بافت‌های مختلف"""
    
    @staticmethod
    def paper_texture(width: int, height: int, 
                      base_color: Tuple[int, int, int] = (255, 255, 255),
                      roughness: float = 0.1) -> Image.Image:
        """
        بافت کاغذ با نویز کنترل شده
        """
        # ایجاد تصویر پایه
        img_array = np.full((height, width, 3), base_color, dtype=np.uint8)
        
        # نویز گوسی برای بافت کاغذ
        noise = np.random.normal(0, roughness * 255, (height, width, 3))
        img_array = np.clip(img_array.astype(float) + noise, 0, 255).astype(np.uint8)
        
        # نویز نمکی و فلفلی خفیف
        salt_pepper = np.random.random((height, width))
        img_array[salt_pepper < roughness * 0.1] = [0, 0, 0]
        img_array[salt_pepper > 1 - roughness * 0.1] = [255, 255, 255]
        
        return Image.fromarray(img_array)
    
    @staticmethod
    def fabric_texture(width: int, height: int,
                       colors: Tuple[Tuple[int, int, int], Tuple[int, int, int]],
                       thread_density: int = 10) -> Image.Image:
        """
        بافت پارچه با الگوی نخ‌ها
        """
        color1, color2 = colors
        
        # ایجاد الگوی تار و پود
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        for y in range(height):
            for x in range(width):
                # الگوی شطرنجی ظریف
                if (x // thread_density + y // thread_density) % 2 == 0:
                    img_array[y, x] = color1
                else:
                    img_array[y, x] = color2
        
        # افزودن نویز ظریف برای طبیعی‌تر شدن
        noise = np.random.randint(0, 20, (height, width, 3))
        img_array = np.clip(img_array.astype(int) + noise, 0, 255).astype(np.uint8)
        
        # کمی تاری برای نرمی پارچه
        img = Image.fromarray(img_array)
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        return img
    
    @staticmethod
    def noise_texture(width: int, height: int,
                      noise_type: str = "gaussian",
                      intensity: float = 0.3) -> Image.Image:
        """
        بافت نویز (گوسی، یکنواخت، پرلین ساده)
        """
        if noise_type == "gaussian":
            noise = np.random.normal(127, intensity * 127, (height, width, 3))
            img_array = np.clip(noise, 0, 255).astype(np.uint8)
            
        elif noise_type == "uniform":
            noise = np.random.randint(0, int(255 * intensity), (height, width, 3))
            img_array = (noise + 128).astype(np.uint8)
            
        else:  # perlin-like با استفاده از سینوس
            x = np.linspace(0, intensity * 10, width)
            y = np.linspace(0, intensity * 10, height)
            xx, yy = np.meshgrid(x, y)
            
            pattern = (np.sin(xx) * np.cos(yy) + 1) / 2
            img_array = (pattern[:, :, np.newaxis] * 255).astype(np.uint8)
            img_array = np.repeat(img_array, 3, axis=2)
        
        return Image.fromarray(img_array)
    
    @staticmethod
    def marble_texture(width: int, height: int,
                       colors: Tuple[Tuple[int, int, int], Tuple[int, int, int]],
                       turbulence: float = 5.0) -> Image.Image:
        """
        بافت مرمر (با استفاده از توابع سینوسی)
        """
        color1, color2 = colors
        
        x = np.linspace(-2, 2, width)
        y = np.linspace(-2, 2, height)
        xx, yy = np.meshgrid(x, y)
        
        # تابع مرمر: sin(x + sin(y + sin(x)))
        marble = np.sin(xx + turbulence * np.sin(yy + turbulence * np.sin(xx)))
        marble = (marble + 1) / 2  # normalize to [0, 1]
        
        # درون‌یابی بین دو رنگ
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(3):
            img_array[:, :, i] = (color1[i] * (1 - marble) + color2[i] * marble).astype(np.uint8)
        
        return Image.fromarray(img_array)