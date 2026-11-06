"""
تولید اشکال هندسی انتزاعی
دایره، مثلث، مستطیل، خطوط موج دار و...
"""

import random
import math
from PIL import ImageDraw
from typing import List, Tuple, Optional

class ShapeGenerator:
    """کلاس تولید اشکال هندسی با قابلیت تنظیم"""
    
    def __init__(self, draw: ImageDraw.ImageDraw, width: int, height: int):
        self.draw = draw
        self.width = width
        self.height = height
        
    def random_circles(self, count: int, colors: List[Tuple[int, int, int]], 
                       min_radius: int = 20, max_radius: int = 150,
                       alpha: Optional[int] = None):
        """رسم دایره‌های تصادفی"""
        for _ in range(count):
            color = random.choice(colors)
            if alpha:
                color = color + (alpha,)
            
            radius = random.randint(min_radius, max_radius)
            x = random.randint(radius, self.width - radius)
            y = random.randint(radius, self.height - radius)
            
            bbox = [x - radius, y - radius, x + radius, y + radius]
            
            if alpha:
                self.draw.ellipse(bbox, fill=color, outline=None)
            else:
                self.draw.ellipse(bbox, fill=color)
    
    def random_polygons(self, count: int, colors: List[Tuple[int, int, int]],
                        sides: Tuple[int, int] = (3, 8)):
        """رسم چندضلعی‌های تصادفی (مثلث، مربع، پنج‌ضلعی و...)"""
        for _ in range(count):
            color = random.choice(colors)
            num_sides = random.randint(sides[0], sides[1])
            
            center_x = random.randint(50, self.width - 50)
            center_y = random.randint(50, self.height - 50)
            radius = random.randint(30, 120)
            
            points = []
            for i in range(num_sides):
                angle = (2 * math.pi * i / num_sides) + random.uniform(0, 0.5)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            
            self.draw.polygon(points, fill=color)
    
    def wavy_lines(self, count: int, colors: List[Tuple[int, int, int]],
                   stroke_width: int = 3):
        """رسم خطوط موج دار زیبا"""
        for _ in range(count):
            color = random.choice(colors)
            
            # نقطه شروع و پایان تصادفی
            start_y = random.randint(0, self.height)
            end_y = random.randint(0, self.height)
            
            points = []
            amplitude = random.randint(20, 80)
            frequency = random.randint(2, 8)
            
            for x in range(0, self.width, 10):
                t = x / self.width
                y = start_y * (1-t) + end_y * t
                y += amplitude * math.sin(x * frequency / 100)
                points.append((x, y))
            
            self.draw.line(points, fill=color, width=stroke_width)
    
    def geometric_pattern(self, colors: List[Tuple[int, int, int]]):
        """الگوی هندسی منظم (شبکه‌ای از اشکال)"""
        cell_size = random.randint(40, 100)
        
        for x in range(0, self.width, cell_size):
            for y in range(0, self.height, cell_size):
                color = random.choice(colors)
                shape_type = random.choice(['circle', 'rect', 'diamond'])
                
                if shape_type == 'circle':
                    center_x = x + cell_size // 2
                    center_y = y + cell_size // 2
                    radius = cell_size // 3
                    bbox = [center_x - radius, center_y - radius, 
                           center_x + radius, center_y + radius]
                    self.draw.ellipse(bbox, fill=color)
                    
                elif shape_type == 'rect':
                    margin = cell_size // 4
                    bbox = [x + margin, y + margin, 
                           x + cell_size - margin, y + cell_size - margin]
                    self.draw.rectangle(bbox, fill=color)
                    
                else:  # diamond
                    cx = x + cell_size // 2
                    cy = y + cell_size // 2
                    r = cell_size // 3
                    points = [(cx, cy - r), (cx + r, cy), 
                             (cx, cy + r), (cx - r, cy)]
                    self.draw.polygon(points, fill=color)
    
    def random_style(self, colors: List[Tuple[int, int, int]], 
                     complexity: int = 5):
        """تولید ترکیبی تصادفی از اشکال مختلف"""
        # انتخاب تصادفی بین سبک‌های مختلف
        styles = [
            lambda: self.random_circles(complexity, colors, 20, 150),
            lambda: self.random_polygons(complexity // 2, colors),
            lambda: self.wavy_lines(complexity // 3, colors),
            lambda: self.geometric_pattern(colors)
        ]
        
        # اجرای ۲ تا ۴ سبک مختلف
        num_styles = random.randint(2, min(4, len(styles)))
        selected = random.sample(styles, num_styles)
        
        for style in selected:
            style()