"""
رابط کاربری کامل با tkinter
شامل پیش‌نمایش زنده، تنظیمات، دکمه ساخت و ذخیره
"""

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageDraw  # اضافه کردن ImageDraw
import threading
import random
from pathlib import Path

# وارد کردن ماژول‌های پروژه
from pattern_engine import PatternEngine, PatternStyle
from shape_generator import ShapeGenerator
from gradient_maker import GradientMaker
from texture_maker import TextureMaker
from seamless_title import SeamlessTileGenerator

class AIPatternGeneratorUI:
    """رابط کاربری اصلی برنامه"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 AI Pattern Generator - تولید‌کننده حرفه‌ای بک‌گراند")
        self.root.geometry("1200x700")
        
        # متغیرهای برنامه
        self.current_image = None
        self.current_tk_image = None
        self.preview_size = (600, 400)
        
        # تنظیمات پیش‌فرض
        self.width = tk.IntVar(value=1920)
        self.height = tk.IntVar(value=1080)
        self.complexity = tk.IntVar(value=5)
        self.style = tk.StringVar(value="abstract")
        self.colors = []  # لیست رنگ‌های انتخاب شده
        
        # کتابخانه‌های تولید
        self.engine = PatternEngine()
        self.seamless_gen = SeamlessTileGenerator()
        
        self.setup_ui()
        
    def setup_ui(self):
        """راه‌اندازی رابط کاربری"""
        # تقسیم به دو پنل
        left_panel = tk.Frame(self.root, width=300, bg='#2c2c2c')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        right_panel = tk.Frame(self.root, bg='#1e1e1e')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === پنل تنظیمات (چپ) ===
        # عنوان
        title = tk.Label(left_panel, text="AI Pattern Generator", 
                        font=('Arial', 16, 'bold'), bg='#2c2c2c', fg='white')
        title.pack(pady=10)
        
        # انتخاب سبک
        style_frame = tk.LabelFrame(left_panel, text="سبک", bg='#2c2c2c', fg='white')
        style_frame.pack(fill=tk.X, pady=5)
        
        styles = [("انتزاعی", "abstract"), ("گرادینت", "gradient"), 
                  ("بافت", "texture"), ("پترن تکراری", "seamless")]
        for text, value in styles:
            rb = tk.Radiobutton(style_frame, text=text, variable=self.style, 
                               value=value, bg='#2c2c2c', fg='white',
                               selectcolor='#2c2c2c')
            rb.pack(anchor=tk.W, padx=10, pady=2)
        
        # رزولوشن
        res_frame = tk.LabelFrame(left_panel, text="رزولوشن خروجی", bg='#2c2c2c', fg='white')
        res_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(res_frame, text="عرض:", bg='#2c2c2c', fg='white').grid(row=0, column=0, padx=5)
        width_entry = tk.Entry(res_frame, textvariable=self.width, width=8)
        width_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(res_frame, text="ارتفاع:", bg='#2c2c2c', fg='white').grid(row=0, column=2, padx=5)
        height_entry = tk.Entry(res_frame, textvariable=self.height, width=8)
        height_entry.grid(row=0, column=3, padx=5)
        
        # دکمه‌های رزولوشن آماده
        res_buttons = tk.Frame(res_frame, bg='#2c2c2c')
        res_buttons.grid(row=1, column=0, columnspan=4, pady=5)
        
        for label, w, h in [("720p", 1280, 720), ("1080p", 1920, 1080), ("4K", 3840, 2160)]:
            btn = tk.Button(res_buttons, text=label, command=lambda w=w, h=h: self.set_resolution(w, h))
            btn.pack(side=tk.LEFT, padx=5)
        
        # پیچیدگی
        complexity_frame = tk.LabelFrame(left_panel, text="پیچیدگی", bg='#2c2c2c', fg='white')
        complexity_frame.pack(fill=tk.X, pady=5)
        
        complexity_scale = tk.Scale(complexity_frame, from_=1, to=10, 
                                    orient=tk.HORIZONTAL, variable=self.complexity,
                                    bg='#2c2c2c', fg='white', length=200)
        complexity_scale.pack(padx=10, pady=5)
        
        # پالت رنگ
        color_frame = tk.LabelFrame(left_panel, text="پالت رنگ (انتخاب 2-4 رنگ)", bg='#2c2c2c', fg='white')
        color_frame.pack(fill=tk.X, pady=5)
        
        self.color_buttons = []
        colors_container = tk.Frame(color_frame, bg='#2c2c2c')
        colors_container.pack(pady=5)
        
        for i in range(4):
            btn = tk.Button(colors_container, text=f"رنگ {i+1}", 
                          command=lambda idx=i: self.choose_color(idx),
                          bg='#555', fg='white', width=8)
            btn.grid(row=0, column=i, padx=5, pady=2)
            self.color_buttons.append(btn)
        
        tk.Button(color_frame, text="تصادفی‌سازی رنگ‌ها", 
                 command=self.random_colors, bg='#4a6fa5', fg='white').pack(pady=5)
        
        # دکمه‌های اصلی
        tk.Button(left_panel, text="🎲 بساز! (تصادفی)", 
                 command=self.generate_random,
                 bg='#28a745', fg='white', font=('Arial', 12, 'bold'),
                 height=2).pack(fill=tk.X, pady=10)
        
        tk.Button(left_panel, text="💾 ذخیره PNG", 
                 command=self.save_image,
                 bg='#007bff', fg='white', font=('Arial', 11),
                 height=1).pack(fill=tk.X, pady=5)
        
        tk.Button(left_panel, text="📋 کپی به کلیپ‌بورد", 
                 command=self.copy_to_clipboard,
                 bg='#6c757d', fg='white').pack(fill=tk.X, pady=5)
        
        # دکمه تولید دسته‌ای
        tk.Button(left_panel, text="📦 تولید ۱۰ عدد تصادفی", 
                 command=self.batch_generate,
                 bg='#fd7e14', fg='white').pack(fill=tk.X, pady=5)
        
        # === پنل پیش‌نمایش (راست) ===
        self.preview_label = tk.Label(right_panel, bg='#1e1e1e', 
                                     text="روی «بساز!» کلیک کنید\nتصویر در اینجا نمایش داده می‌شود",
                                     font=('Arial', 14), fg='#888')
        self.preview_label.pack(expand=True, fill=tk.BOTH)
        
        # نوار وضعیت
        self.status_bar = tk.Label(self.root, text="آماده", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # راه‌اندازی اولیه
        self.random_colors()
        
    def set_resolution(self, width: int, height: int):
        """تنظیم رزولوشن از دکمه‌های آماده"""
        self.width.set(width)
        self.height.set(height)
        self.update_status(f"رزولوشن تنظیم شد: {width}x{height}")
        
    def choose_color(self, index: int):
        """انتخاب رنگ از Color Picker"""
        color = colorchooser.askcolor(title=f"انتخاب رنگ {index+1}")
        if color[0]:
            while len(self.colors) <= index:
                self.colors.append(None)
            self.colors[index] = tuple(int(c) for c in color[0])
            # به‌روزرسانی رنگ دکمه
            self.color_buttons[index].config(bg=self.rgb_to_hex(self.colors[index]))
            
    def random_colors(self):
        """تولید پالت رنگ تصادفی"""
        self.colors = []
        num_colors = random.randint(2, 4)
        
        for i in range(4):
            if i < num_colors:
                # تولید رنگ شاد و زنده
                hue = random.random()
                sat = 0.6 + random.random() * 0.4
                val = 0.7 + random.random() * 0.3
                from colorsys import hsv_to_rgb
                rgb = hsv_to_rgb(hue, sat, val)
                color = tuple(int(c * 255) for c in rgb)
                self.colors.append(color)
                self.color_buttons[i].config(bg=self.rgb_to_hex(color), state=tk.NORMAL)
            else:
                self.color_buttons[i].config(bg='#555', state=tk.NORMAL)
                
        self.update_status("پالت رنگ تصادفی جدید تولید شد")
        
    def rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def generate_random(self):
        """تولید تصویر تصادفی با تنظیمات فعلی"""
        self.update_status("در حال تولید تصویر...")
        
        # اجرا در ترد جداگانه برای عدم قفل شدن UI
        thread = threading.Thread(target=self._generate_async)
        thread.daemon = True
        thread.start()
        
    def _generate_async(self):
        """تولید غیرهمزمان تصویر"""
        try:
            style = self.style.get()
            colors = [c for c in self.colors if c is not None]
            
            if not colors:
                colors = [(random.randint(0,255), random.randint(0,255), random.randint(0,255))]
            
            if style == "abstract":
                img = self._generate_abstract(colors)
            elif style == "gradient":
                img = self._generate_gradient(colors)
            elif style == "texture":
                img = self._generate_texture(colors)
            else:  # seamless
                img = self._generate_seamless(colors)
            
            self.current_image = img
            
            # نمایش در پیش‌نمایش
            preview = img.copy()
            preview.thumbnail(self.preview_size, Image.LANCZOS)
            
            self.current_tk_image = ImageTk.PhotoImage(preview)
            
            # به‌روزرسانی در ترد اصلی
            self.root.after(0, self._update_preview)
            self.update_status("✅ تصویر با موفقیت تولید شد!")
            
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"❌ خطا: {str(e)}"))
            print(f"Error details: {e}")
    
    def _generate_abstract(self, colors):
        """تولید سبک انتزاعی"""
        self.engine.set_resolution(self.width.get(), self.height.get())
        self.engine.create_canvas(colors[0])
        shape_gen = ShapeGenerator(self.engine.draw, self.engine.width, self.engine.height)
        other_colors = colors[1:] if len(colors) > 1 else colors
        shape_gen.random_style(other_colors, self.complexity.get())
        self.engine.add_noise(0.02)
        return self.engine.get_image()
    
    def _generate_gradient(self, colors):
        """تولید سبک گرادینت"""
        if len(colors) < 2:
            colors.append((255,255,255))
        
        grad_type = random.choice(["linear", "radial"])
        if grad_type == "linear":
            angle = random.randint(0, 360)
            img = GradientMaker.linear_gradient(self.width.get(), self.height.get(), colors, angle)
        else:
            img = GradientMaker.radial_gradient(self.width.get(), self.height.get(), colors)
        
        # اضافه کردن اشکال ساده روی گرادینت
        # استفاده از ImageDraw.Draw (که الان import شده)
        draw = ImageDraw.Draw(img)
        shape_gen = ShapeGenerator(draw, self.width.get(), self.height.get())
        other_colors = colors[1:] if len(colors) > 1 else colors
        shape_gen.random_circles(self.complexity.get() // 2, other_colors, 10, 80, alpha=100)
        
        return img
    
    def _generate_texture(self, colors):
        """تولید سبک بافت"""
        texture_type = random.choice(["paper", "fabric", "noise", "marble"])
        
        if texture_type == "paper":
            img = TextureMaker.paper_texture(self.width.get(), self.height.get(), colors[0], 0.15)
        elif texture_type == "fabric":
            if len(colors) < 2:
                colors.append(colors[0])
            img = TextureMaker.fabric_texture(self.width.get(), self.height.get(), (colors[0], colors[1]), 15)
        elif texture_type == "marble":
            if len(colors) < 2:
                colors.append((255,255,255))
            img = TextureMaker.marble_texture(self.width.get(), self.height.get(), (colors[0], colors[1]), 4)
        else:
            img = TextureMaker.noise_texture(self.width.get(), self.height.get(), "gaussian", 0.3)
        
        return img
    
    def _generate_seamless(self, colors):
        """تولید پترن تکراری بدون درز"""
        if len(colors) < 2:
            colors.append((colors[0][0]//2, colors[0][1]//2, colors[0][2]//2))
        
        tile_size = min(self.width.get(), self.height.get()) // 2
        self.seamless_gen.tile_size = tile_size
        tile = self.seamless_gen.generate_seamless_pattern(colors, self.complexity.get())
        
        # بزرگنمایی به سایز مورد نظر
        img = tile.resize((self.width.get(), self.height.get()), Image.LANCZOS)
        return img
    
    def _update_preview(self):
        """به‌روزرسانی پیش‌نمایش در UI"""
        self.preview_label.config(image=self.current_tk_image, text="")
    
    def save_image(self):
        """ذخیره تصویر"""
        if self.current_image is None:
            messagebox.showwarning("هشدار", "اول یک تصویر تولید کنید!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile=f"pattern_{random.randint(1000,9999)}.png"
        )
        
        if file_path:
            self.current_image.save(file_path, "PNG", quality=95)
            self.update_status(f"تصویر ذخیره شد: {file_path}")
            messagebox.showinfo("موفق", f"تصویر با موفقیت ذخیره شد!\n{file_path}")
    
    def copy_to_clipboard(self):
        """کپی به کلیپ‌بورد (نیاز به کتابخانه اضافی)"""
        messagebox.showinfo("اطلاع", "برای کپی به کلیپ‌بورد از تصویر ذخیره شده استفاده کنید")
        self.update_status("از دکمه ذخیره استفاده کنید سپس تصویر را کپی کنید")
    
    def batch_generate(self):
        """تولید دسته‌ای ۱۰ تصویر تصادفی"""
        folder = filedialog.askdirectory(title="انتخاب پوشه برای ذخیره خروجی‌ها")
        if not folder:
            return
        
        self.update_status("در حال تولید ۱۰ تصویر...")
        
        def generate_batch():
            for i in range(10):
                self.random_colors()
                # کمی تاخیر برای تولید تصویر
                import time
                time.sleep(0.5)
                self._generate_async()
                time.sleep(1)  # صبر برای اتمام تولید
                if self.current_image:
                    self.current_image.save(f"{folder}/pattern_{i+1:03d}.png")
                    print(f"Saved pattern_{i+1:03d}.png")
            self.root.after(0, lambda: messagebox.showinfo("موفق", f"۱۰ تصویر در {folder} ذخیره شدند!"))
            self.root.after(0, lambda: self.update_status("تولید دسته‌ای کامل شد!"))
        
        thread = threading.Thread(target=generate_batch)
        thread.daemon = True
        thread.start()
    
    def update_status(self, message: str):
        """به‌روزرسانی نوار وضعیت"""
        self.root.after(0, lambda: self.status_bar.config(text=message))
    
    def run(self):
        """اجرای برنامه"""
        self.root.mainloop()


# اجرای برنامه
if __name__ == "__main__":
    app = AIPatternGeneratorUI()
    app.run()