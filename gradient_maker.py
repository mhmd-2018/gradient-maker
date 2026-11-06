"""
تولید گرادینت‌های خطی، شعاعی و ترکیبی
"""

import numpy as np
from PIL import Image
from typing import List, Tuple, Optional
import math

class GradientMaker:
    """ساخت انواع گرادینت با کیفیت بالا"""
    
    @staticmethod
    def linear_gradient(width: int, height: int, 
                        colors: List[Tuple[int, int, int]],
                        angle: float = 0) -> Image.Image:
        """
        گرادینت خطی
        angle: زاویه بر حسب درجه
        """
        # تبدیل زاویه به رادیان
        rad = math.radians(angle)
        dx = math.cos(rad)
        dy = math.sin(rad)
        
        # ایجاد آرایه از مختصات
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        xx, yy = np.meshgrid(x, y)
        
        # محاسبه فاصله در جهت گرادینت
        t = (xx * dx + yy * dy + 1) / 2
        t = np.clip(t, 0, 1)
        
        # ایجاد تصویر
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        for i in range(3):
            # درون‌یابی خطی بین رنگ‌ها
            values = np.interp(t.flatten(), 
                              np.linspace(0, 1, len(colors)), 
                              [c[i] for c in colors])
            img_array[:, :, i] = values.reshape(height, width).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    @staticmethod
    def radial_gradient(width: int, height: int,
                        colors: List[Tuple[int, int, int]],
                        center: Optional[Tuple[float, float]] = None,
                        radius: Optional[float] = None) -> Image.Image:
        """
        گرادینت شعاعی
        center: نقطه مرکز (نسبی 0 تا 1)
        radius: شعاع (نسبی 0 تا 1)
        """
        if center is None:
            center = (0.5, 0.5)
        if radius is None:
            radius = max(width, height) / 2
        
        cx = center[0] * width
        cy = center[1] * height
        
        # ایجاد مختصات
        x = np.arange(width)
        y = np.arange(height)
        xx, yy = np.meshgrid(x, y)
        
        # محاسبه فاصله از مرکز
        distance = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        t = np.clip(distance / radius, 0, 1)
        
        # ایجاد تصویر
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        for i in range(3):
            values = np.interp(t.flatten(), 
                              np.linspace(0, 1, len(colors)), 
                              [c[i] for c in colors])
            img_array[:, :, i] = values.reshape(height, width).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    @staticmethod
    def multi_gradient(width: int, height: int,
                       color_stops: List[Tuple[float, Tuple[int, int, int]]],
                       gradient_type: str = "linear",
                       angle: float = 45) -> Image.Image:
        """
        گرادینت چند مرحله‌ای با نقاط توقف رنگی
        color_stops: لیستی از (نسبت, رنگ)
        """
        # مرتب‌سازی بر اساس نسبت
        color_stops.sort(key=lambda x: x[0])
        colors = [c for _, c in color_stops]
        positions = [p for p, _ in color_stops]
        
        # نرمال‌سازی موقعیت‌ها
        positions = np.array(positions)
        
        if gradient_type == "linear":
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)
            
            x = np.linspace(-1, 1, width)
            y = np.linspace(-1, 1, height)
            xx, yy = np.meshgrid(x, y)
            t = (xx * dx + yy * dy + 1) / 2
            t = np.clip(t, 0, 1)
            
        else:  # radial
            cx, cy = width // 2, height // 2
            max_dist = math.sqrt(cx**2 + cy**2)
            
            x = np.arange(width)
            y = np.arange(height)
            xx, yy = np.meshgrid(x, y)
            
            distance = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
            t = np.clip(distance / max_dist, 0, 1)
        
        # درون‌یابی بین نقاط توقف
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        for i in range(3):
            values = np.interp(t.flatten(), positions, [c[i] for c in colors])
            img_array[:, :, i] = values.reshape(height, width).astype(np.uint8)
        
        return Image.fromarray(img_array)