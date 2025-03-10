import numpy as np
from PIL import Image
import cv2
from rich.console import Console
from rich.live import Live
from rich.text import Text
import random
import time

class ASCIIArtGenerator:
    def __init__(self):
        # ASCII字符集，从暗到亮
        self.ASCII_CHARS = "@%#*+=-:. "
        self.console = Console()
        
    def resize_image(self, image, new_width=200):  # 增加默认宽度
        """调整图像大小，保持宽高比"""
        width, height = image.size
        aspect_ratio = height/width
        # 根据字符宽高比调整，因为终端字符通常高度是宽度的2倍
        new_height = int(aspect_ratio * new_width * 0.5)  # 添加0.5系数来补偿字符宽高比
        resized_image = image.resize((new_width, new_height))
        return resized_image

    def get_pixel_color(self, pixel):
        """获取像素的RGB颜色值和灰度值"""
        if isinstance(pixel, tuple):
            if len(pixel) >= 3:
                r, g, b = pixel[:3]
                gray = int(0.299*r + 0.587*g + 0.114*b)
                return (r, g, b), gray
        return (0, 0, 0), pixel

    def pixels_to_colored_ascii(self, image):
        """将像素转换为带颜色的ASCII字符"""
        pixels = list(image.getdata())
        ascii_pixels = []
        
        for pixel in pixels:
            color, gray = self.get_pixel_color(pixel)
            char = self.ASCII_CHARS[min(gray*len(self.ASCII_CHARS)//256, len(self.ASCII_CHARS)-1)]
            ascii_pixels.append((char, color))
        return ascii_pixels

    def image_to_ascii(self, image_path, width=200):  # 增加默认宽度
        """将图像转换为ASCII艺术"""
        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"Unable to open image file {image_path}")
            return None
        
        image = self.resize_image(image, width)
        # 保持图像的颜色模式
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        ascii_pixels = self.pixels_to_colored_ascii(image)
        
        # 构建ASCII图像数据
        img_width = image.width
        ascii_image = {
            'width': img_width,
            'height': image.height,
            'pixels': ascii_pixels
        }
        
        # 为终端显示构建字符串
        ascii_str = ""
        for i in range(0, len(ascii_pixels), img_width):
            row = ascii_pixels[i:i+img_width]
            ascii_str += ''.join(pixel[0] for pixel in row) + "\n"
        
        return ascii_image, ascii_str

    def generate_random_ascii(self, width, height):
        """生成随机ASCII字符"""
        return ''.join(random.choice(self.ASCII_CHARS) for _ in range(width * height))

    def animate_transition(self, ascii_image, duration=3):
        """在终端中显示ASCII动画（仅字符，无颜色）"""
        if isinstance(ascii_image, tuple):
            ascii_image = ascii_image[1]  # 使用字符串版本
            
        target_lines = ascii_image.split('\n')
        height = len(target_lines)
        width = len(target_lines[0]) if target_lines else 100

        current = self.generate_random_ascii(width, height)
        current_lines = [current[i:i+width] for i in range(0, len(current), width)]

        start_time = time.time()
        with Live(refresh_per_second=30) as live:  # 提高刷新率
            while True:
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break

                progress = elapsed / duration
                new_frame = ""
                for i in range(height):
                    for j in range(width):
                        if random.random() < progress * 1.5:  # 加快转换速度
                            new_frame += target_lines[i][j] if i < len(target_lines) and j < len(target_lines[i]) else " "
                        else:
                            new_frame += current_lines[i][j] if i < len(current_lines) else " "
                    new_frame += "\n"

                text = Text(new_frame)
                live.update(text)
                time.sleep(0.02)  # 减少延迟

        self.console.print(ascii_image)

def main():
    generator = ASCIIArtGenerator()
    ascii_art = generator.image_to_ascii("input.jpg")
    if ascii_art:
        generator.animate_transition(ascii_art[1])  # 使用字符串版本

if __name__ == "__main__":
    main() 