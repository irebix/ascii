# ASCII Art Animation Generator

这个项目可以创建类似Midjourney官网的ASCII字符动画效果，将代码文本通过动画效果转换为ASCII艺术图像。

## 功能特点

- 图片转ASCII艺术
- 动态过渡动画效果
- 支持自定义动画持续时间
- 终端彩色输出支持

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 准备一张想要转换的目标图片

2. 运行示例程序：

```bash
python demo.py
```

或者在你自己的代码中使用：

```python
from ascii_art import ASCIIArtGenerator

# 创建生成器实例
generator = ASCIIArtGenerator()

# 转换图片为ASCII艺术
ascii_art = generator.image_to_ascii("your_image.jpg")

# 创建动画效果
generator.animate_transition(ascii_art, duration=5)
```

## 参数说明

- `image_to_ascii(image_path, width=100)`: 
  - image_path: 图片路径
  - width: ASCII艺术的宽度（字符数）

- `animate_transition(target_ascii, width=100, height=30, duration=3)`:
  - target_ascii: 目标ASCII艺术
  - width: 动画宽度
  - height: 动画高度
  - duration: 动画持续时间（秒）

## 注意事项

1. 确保输入图片存在且格式正确
2. 终端窗口大小应该足够显示完整的ASCII艺术
3. 建议使用支持彩色输出的现代终端模拟器

## 依赖项

- Pillow: 图像处理
- numpy: 数组运算
- opencv-python: 视频处理
- rich: 终端颜色输出

## 许可证

MIT License 