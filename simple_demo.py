import os
from PIL import Image
import numpy as np
import webbrowser
import html
import random
import time

def create_html_animation(code, target_image_path, output_path='output/animation.html', width=200):
    try:
        print(f"正在处理图片：{target_image_path}")
        img = Image.open(target_image_path)
        print(f"原始图片大小：{img.size}")
        
        # 获取原始图片尺寸
        orig_img = Image.open(target_image_path)
        orig_width, orig_height = orig_img.size
        print(f"原始图片尺寸：{orig_width}x{orig_height}")
        
        # 使用原始图片的尺寸
        canvas_width = orig_width  # 1920
        canvas_height = orig_height  # 879
        
        # 调整ASCII艺术的大小以匹配原始图片的比例
        aspect_ratio = orig_height / orig_width
        char_width_height_ratio = 0.5  # 字符的宽高比
        target_aspect_ratio = aspect_ratio * char_width_height_ratio
        height = int(width * target_aspect_ratio)
        
        img = img.resize((width, height))
        print(f"调整后的ASCII艺术大小：{img.size}")
        
        # 获取RGB数据
        img_rgb = img.convert('RGB')
        img_gray = img.convert('L')
        pixels_rgb = np.array(img_rgb)
        pixels_gray = np.array(img_gray)
        
        # 二进制字符集 (0和1)
        binary_chars = '01'
        
        # 将图片转换为二进制字符和颜色
        ascii_art = []
        for y in range(height):
            line = []
            for x in range(width):
                gray = pixels_gray[y, x]
                rgb = pixels_rgb[y, x]
                # 根据亮度选择0或1
                index = 1 if gray > 128 else 0
                char = binary_chars[index]
                color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
                line.append({"char": char, "color": color})
            ascii_art.append(line)
        
        # 将原始图片转换为base64编码，用于在HTML中显示
        import base64
        from io import BytesIO
        
        # 转换为base64
        buffered = BytesIO()
        orig_img.save(buffered, format="JPEG", quality=95)
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # 读取故障艺术过渡效果的JavaScript代码
        try:
            with open('glitch_transition.js', 'r', encoding='utf-8') as f:
                glitch_js = f.read()
        except Exception as e:
            print(f"无法读取故障艺术效果代码: {str(e)}")
            glitch_js = "// 故障艺术效果代码加载失败"
        
        # 生成HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    background-color: #000000;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    overflow: hidden;
                }}
                #container {{
                    width: {canvas_width}px;
                    height: {canvas_height}px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    position: relative;
                }}
                canvas {{
                    image-rendering: pixelated;
                    position: absolute;
                    z-index: 1;
                    width: {canvas_width}px;
                    height: {canvas_height}px;
                }}
                #originalImage {{
                    position: absolute;
                    z-index: 0;
                    opacity: 0;
                    width: {canvas_width}px;
                    height: {canvas_height}px;
                }}
            </style>
        </head>
        <body>
            <div id="container">
                <canvas id="asciiCanvas"></canvas>
                <img id="originalImage" src="data:image/jpeg;base64,{img_base64}" alt="Original Image">
            </div>
            <script>
                const sourceCode = `{html.escape(code)}`;
                const targetAscii = {str([[{"char": cell["char"], "color": cell["color"]} for cell in row] for row in ascii_art])};
                const binaryChars = '{binary_chars}';
                
                // 设置Canvas
                const canvas = document.getElementById('asciiCanvas');
                const ctx = canvas.getContext('2d');
                
                // 设置Canvas大小为原始图片尺寸
                canvas.width = {canvas_width};
                canvas.height = {canvas_height};
                
                // 计算字符大小以适应画布
                const charWidth = Math.ceil({canvas_width} / targetAscii[0].length);
                const charHeight = Math.ceil({canvas_height} / targetAscii.length);
                
                // 解析源代码
                const sourceLines = sourceCode.split('\\n');
                
                // 创建源代码字符数组
                const sourceChars = [];
                for (let i = 0; i < targetAscii.length; i++) {{
                    sourceChars[i] = [];
                    for (let j = 0; j < targetAscii[i].length; j++) {{
                        // 确保我们不会超出源代码行数
                        const lineIndex = Math.min(i, sourceLines.length - 1);
                        // 如果当前行为空，使用空格
                        if (!sourceLines[lineIndex] || sourceLines[lineIndex].length === 0) {{
                            sourceChars[i][j] = ' ';
                            continue;
                        }}
                        // 循环使用当前行的字符
                        const charIndex = j % sourceLines[lineIndex].length;
                        sourceChars[i][j] = sourceLines[lineIndex][charIndex];
                    }}
                }}
                
                // 动画函数
                function animate() {{
                    const duration = 4000; // 4秒
                    const startTime = Date.now();
                    
                    // 初始显示源代码
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.font = `${{charHeight}}px monospace`;
                    ctx.textBaseline = 'top';
                    ctx.fillStyle = '#ffffff';
                    
                    // 先显示源代码
                    for (let i = 0; i < sourceLines.length && i < targetAscii.length; i++) {{
                        ctx.fillText(sourceLines[i], 0, i * charHeight);
                    }}
                    
                    // 创建一个数组来跟踪每个字符的状态
                    const charStates = [];
                    for (let i = 0; i < targetAscii.length; i++) {{
                        charStates[i] = [];
                        for (let j = 0; j < targetAscii[i].length; j++) {{
                            charStates[i][j] = {{
                                char: sourceChars[i][j],
                                color: '#ffffff',
                                startTime: startTime + Math.random() * duration * 0.5 // 减少随机延迟
                            }};
                        }}
                    }}
                    
                    function update() {{
                        const now = Date.now();
                        const progress = (now - startTime) / duration;
                        
                        if (progress >= 1) {{
                            // 最终状态
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                            ctx.font = `${{charHeight}}px monospace`;
                            ctx.textBaseline = 'top';
                            
                            for (let i = 0; i < targetAscii.length; i++) {{
                                for (let j = 0; j < targetAscii[i].length; j++) {{
                                    const cell = targetAscii[i][j];
                                    ctx.fillStyle = cell.color;
                                    ctx.fillText(cell.char, j * charWidth, i * charHeight);
                                }}
                            }}
                            
                            {glitch_js.replace('setTimeout(() => {', 'setTimeout(() => {').replace('}, 300);', '}, 100);')}
                            
                            return;
                        }}
                        
                        // 清除Canvas
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.font = `${{charHeight}}px monospace`;
                        ctx.textBaseline = 'top';
                        
                        // 更新每个字符
                        for (let i = 0; i < targetAscii.length; i++) {{
                            for (let j = 0; j < targetAscii[i].length; j++) {{
                                const state = charStates[i][j];
                                const charProgress = Math.max(0, Math.min(1, (now - state.startTime) / (duration * 0.3)));
                                
                                if (charProgress >= 1) {{
                                    // 完成转换
                                    const cell = targetAscii[i][j];
                                    state.char = cell.char;
                                    state.color = cell.color;
                                }} else if (charProgress > 0 && Math.random() < 0.3) {{
                                    // 正在转换中 - 随机显示0或1
                                    state.char = binaryChars[Math.floor(Math.random() * binaryChars.length)];
                                    
                                    // 颜色逐渐接近目标颜色
                                    if (charProgress > 0.7) {{
                                        state.color = targetAscii[i][j].color;
                                    }} else {{
                                        const randomI = Math.floor(Math.random() * targetAscii.length);
                                        const randomJ = Math.floor(Math.random() * targetAscii[0].length);
                                        state.color = targetAscii[randomI][randomJ].color;
                                    }}
                                }}
                                
                                // 绘制字符
                                ctx.fillStyle = state.color;
                                ctx.fillText(state.char, j * charWidth, i * charHeight);
                            }}
                        }}
                        
                        requestAnimationFrame(update);
                    }}
                    
                    update();
                }}
                
                // 页面加载完成后开始动画
                document.addEventListener('DOMContentLoaded', () => {{
                    // 立即开始动画
                    animate();
                }});
            </script>
        </body>
        </html>
        """
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 保存HTML文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML文件已保存到：{output_path}")
        return output_path
    except Exception as e:
        print(f"发生错误：{str(e)}")
        raise

def main():
    # 从demo.py文件中读取源代码
    try:
        with open('demo.py', 'r', encoding='utf-8') as f:
            source_code = f.read()
        print("成功读取demo.py文件")
        
        # 确保源代码中的换行符被正确处理
        # 在JavaScript中，我们需要确保换行符被正确转义
        source_code = source_code.replace('\r\n', '\n')  # 统一换行符
    except Exception as e:
        print(f"读取demo.py文件失败: {str(e)}")
        # 使用默认代码作为备选
        source_code = '''def ascii_art():
    """这是一个简单的演示
    展示代码如何变成ASCII艺术"""
    print("Hello, ASCII Art!")
    return True'''
    
    # 图片路径
    image_path = os.path.join("test_images", "test.jpg")
    print(f"图片路径：{os.path.abspath(image_path)}")
    
    # 生成动画HTML
    html_path = create_html_animation(source_code, image_path, width=200)  # 使用适中的宽度
    
    # 在浏览器中打开
    abs_path = os.path.abspath(html_path)
    print(f"在浏览器中打开动画：{abs_path}")
    webbrowser.open(f"file://{abs_path}")

if __name__ == "__main__":
    main() 