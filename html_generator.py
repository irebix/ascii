import os
import json
from datetime import datetime

class HTMLGenerator:
    @staticmethod
    def generate_animation_html(initial_text, target_ascii, duration=5, fps=20):
        """生成包含ASCII动画的HTML文件"""
        # 创建输出目录
        os.makedirs('output', exist_ok=True)
        
        # 生成唯一的文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_path = f'output/ascii_animation_{timestamp}.html'
        
        # 准备初始文本数据
        initial_lines = initial_text.split('\n')
        initial_colored = []
        for i, line in enumerate(initial_lines):
            initial_colored.extend((char, (200, 200, 200)) for char in line)  # 使用浅灰色
            if i < len(initial_lines) - 1:
                initial_colored.append(('\n', (200, 200, 200)))
        
        # 获取目标ASCII数据
        if isinstance(target_ascii, tuple):
            target_data = target_ascii[0]
            width = target_data['width']
            height = target_data['height']
            target_pixels = []
            pixels = target_data['pixels']
            for i in range(0, len(pixels), width):
                row = pixels[i:i+width]
                target_pixels.extend(row)
                if i + width < len(pixels):
                    target_pixels.append(('\n', (0, 0, 0)))
        else:
            target_lines = target_ascii.split('\n')
            width = len(target_lines[0]) if target_lines else 0
            height = len(target_lines)
            target_pixels = []
            for i, line in enumerate(target_lines):
                target_pixels.extend((char, (51, 255, 51)) for char in line)
                if i < len(target_lines) - 1:
                    target_pixels.append(('\n', (51, 255, 51)))
        
        # 创建HTML内容
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ASCII Art Animation</title>
    <style>
        body {{
            background-color: #1e1e1e;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            font-family: "Courier New", monospace;
        }}
        #ascii-container {{
            background-color: #000;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            overflow: hidden;
            position: relative;
        }}
        #ascii-art {{
            white-space: pre;
            font-size: 8px;
            line-height: 1;
            font-family: "Courier New", monospace;
            letter-spacing: 0;
            font-weight: bold;
        }}
        .ascii-char {{
            display: inline-block;
            width: 0.6em;
            height: 1em;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div id="ascii-container">
        <pre id="ascii-art"></pre>
    </div>
    
    <script>
        const initialPixels = {json.dumps([(char, color) for char, color in initial_colored])};
        const targetPixels = {json.dumps([(char, color) for char, color in target_pixels])};
        const width = {width};
        const height = {height};
        const duration = {duration} * 1000;
        const fps = {fps};
        const frameTime = 1000 / fps;
        
        const asciiArt = document.getElementById('ascii-art');
        let startTime = null;
        
        // 初始化显示
        function initDisplay() {{
            let html = "";
            for (let i = 0; i < targetPixels.length; i++) {{
                const [char, color] = initialPixels[i] || [' ', [200, 200, 200]];
                if (char === '\\n') {{
                    html += '\\n';
                }} else {{
                    html += `<span class="ascii-char" style="color: rgb(${{color[0]}},${{color[1]}},${{color[2]}})">${{char}}</span>`;
                }}
            }}
            asciiArt.innerHTML = html;
        }}

        function interpolateColor(color1, color2, progress) {{
            return [
                Math.round(color1[0] + (color2[0] - color1[0]) * progress),
                Math.round(color1[1] + (color2[1] - color1[1]) * progress),
                Math.round(color1[2] + (color2[2] - color1[2]) * progress)
            ];
        }}
        
        function animate(timestamp) {{
            if (!startTime) startTime = timestamp;
            const elapsed = timestamp - startTime;
            
            if (elapsed >= duration) {{
                // 设置最终状态
                let finalHtml = "";
                for (const [char, color] of targetPixels) {{
                    if (char === '\\n') {{
                        finalHtml += '\\n';
                    }} else {{
                        finalHtml += `<span class="ascii-char" style="color: rgb(${{color[0]}},${{color[1]}},${{color[2]}})">${{char}}</span>`;
                    }}
                }}
                asciiArt.innerHTML = finalHtml;
                return;
            }}
            
            const progress = elapsed / duration;
            let newHtml = "";
            
            // 每帧更新所有字符
            for (let i = 0; i < targetPixels.length; i++) {{
                const [targetChar, targetColor] = targetPixels[i];
                const [initialChar, initialColor] = i < initialPixels.length ? 
                    initialPixels[i] : [' ', [200, 200, 200]];
                
                if (targetChar === '\\n') {{
                    newHtml += '\\n';
                    continue;
                }}
                
                // 随机决定是否更新这个字符
                let displayChar;
                if (Math.random() < progress * 2) {{
                    displayChar = targetChar;
                }} else {{
                    displayChar = "@%#*+=-:. "[Math.floor(Math.random() * 10)];
                }}
                
                // 计算当前颜色
                const color = interpolateColor(initialColor, targetColor, progress);
                newHtml += `<span class="ascii-char" style="color: rgb(${{color[0]}},${{color[1]}},${{color[2]}})">${{displayChar}}</span>`;
            }}
            
            // 更新显示
            asciiArt.innerHTML = newHtml;
            requestAnimationFrame(animate);
        }}
        
        // 开始动画
        initDisplay();
        requestAnimationFrame(animate);
    </script>
</body>
</html>
'''
        
        # 写入HTML文件
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_path 