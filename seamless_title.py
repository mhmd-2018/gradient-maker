"""
تولید پترن‌های تکراری بدون درز (seamless tile)
برای کاغذ دیواری، پارچه، وبسایت
"""

import numpy as np
from PIL import Image, ImageDraw
import random
import math
from typing import List, Tuple

class SeamlessTileGenerator:
    """تولید پترن‌های تکراری بدون درز"""
    
    def __init__(self, tile_size: int = 512):
        self.tile_size = tile_size
        
    def generate_seamless_pattern(self, 
                                   colors: List[Tuple[int, int, int]],
                                   complexity: int = 3) -> Image.Image:
        """
        تولید پترن تکراری بدون درز
        """
        # ایجاد بوم با سایز ۳x۳ برای اطمینان از seamless بودن
        full_size = self.tile_size * 3
        img = Image.new('RGB', (full_size, full_size), colors[0])
        draw = ImageDraw.Draw(img)
        
        # رسم اشکال در کل فضای ۳x۳
        for _ in range(complexity * 20):
            color = random.choice(colors[1:] if len(colors) > 1 else colors)
            
            # شکل تصادفی
            shape_type = random.choice(['circle', 'rect', 'polygon'])
            x = random.randint(0, full_size)
            y = random.randint(0, full_size)
            size = random.randint(20, self.tile_size // 2)
            
            if shape_type == 'circle':
                bbox = [x - size, y - size, x + size, y + size]
                draw.ellipse(bbox, fill=color)
                
            elif shape_type == 'rect':
                bbox = [x - size, y - size, x + size, y + size]
                draw.rectangle(bbox, fill=color)
                
            else:  # polygon (diamond like)
                points = [(x, y - size), (x + size, y), 
                         (x, y + size), (x - size, y)]
                draw.polygon(points, fill=color)
        
        # برش قسمت وسط (seamless tile)
        tile = img.crop((self.tile_size, self.tile_size, 
                         self.tile_size * 2, self.tile_size * 2))
        
        return tile
    
    def create_seamless_preview(self, tile: Image.Image, 
                                 repeat: int = 3) -> Image.Image:
        """
        نمایش پیش‌نمایش از تکرار پترن
        """
        full_size = tile.width * repeat
        preview = Image.new('RGB', (full_size, full_size))
        
        for i in range(repeat):
            for j in range(repeat):
                preview.paste(tile, (i * tile.width, j * tile.height))
        
        return preview
    
    def save_as_pattern_pack(self, patterns: List[Image.Image], 
                             output_dir: str, prefix: str = "pattern"):
        """
        ذخیره مجموعه پترن به همراه پیش‌نمایش
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for idx, pattern in enumerate(patterns):
            # ذخیره تایل اصلی
            pattern.save(f"{output_dir}/{prefix}_{idx:03d}_tile.png")
            
            # ایجاد و ذخیره پیش‌نمایش ۳x۳
            preview = self.create_seamless_preview(pattern, 3)
            preview.save(f"{output_dir}/{prefix}_{idx:03d}_preview.png")