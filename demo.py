from ascii_art import ASCIIArtGenerator
from html_generator import HTMLGenerator
import time
import os
import webbrowser

def main():
    # 创建ASCII艺术生成器实例
    generator = ASCIIArtGenerator()
    
    # 示例代码文本
    code_text = '''def hello_world():
    print("Hello, World!")
    # This is a sample code
    # that will transform
    # into ASCII art
    return True'''
    
    # 首先显示代码文本
    print("Starting with code:")
    print(code_text)
    time.sleep(1)
    
    # 获取测试图片路径
    image_path = os.path.join("test_images", "test.jpg")  # 将test.jpg替换为你的图片名称
    
    # 转换图像为ASCII艺术（现在返回彩色数据和字符串）
    print("\nTransforming to ASCII art...")
    ascii_art_data = generator.image_to_ascii(image_path, width=300)  # 增加宽度以提高分辨率
    
    if ascii_art_data:
        # 生成HTML动画（使用完整的彩色数据）
        html_generator = HTMLGenerator()
        html_path = html_generator.generate_animation_html(
            initial_text=code_text,
            target_ascii=ascii_art_data,  # 传递完整的图像数据
            duration=5,
            fps=30
        )
        
        # 在浏览器中打开生成的HTML文件
        print(f"\nOpening animation in your browser: {html_path}")
        webbrowser.open(f"file://{os.path.abspath(html_path)}")
        
        # 同时在终端中显示动画（仅字符，无颜色）
        generator.animate_transition(ascii_art_data[1], duration=5)
    else:
        print(f"Failed to load image. Please check if {image_path} exists.")

if __name__ == "__main__":
    main() 