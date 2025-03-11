// 动画完成后开始故障艺术过渡效果
setTimeout(() => {
    // 创建一个故障艺术过渡效果
    const originalImage = document.getElementById('originalImage');
    const glitchCanvas = document.createElement('canvas');
    glitchCanvas.width = canvas.width;
    glitchCanvas.height = canvas.height;
    glitchCanvas.style.position = 'absolute';
    glitchCanvas.style.zIndex = '2';
    glitchCanvas.style.maxWidth = '100%';
    glitchCanvas.style.maxHeight = '100%';
    glitchCanvas.style.width = 'auto';
    glitchCanvas.style.height = 'auto';
    glitchCanvas.style.objectFit = 'contain';
    document.getElementById('container').appendChild(glitchCanvas);
    
    const glitchCtx = glitchCanvas.getContext('2d');
    
    // 加载原始图片到一个临时Canvas以便操作像素
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext('2d');
    
    const img = new Image();
    img.onload = () => {
        // 先绘制ASCII艺术到临时Canvas
        tempCtx.drawImage(canvas, 0, 0);
        const asciiImageData = tempCtx.getImageData(0, 0, canvas.width, canvas.height);
        
        // 清除临时Canvas
        tempCtx.clearRect(0, 0, canvas.width, canvas.height);
        
        // 绘制原始图片到临时Canvas
        tempCtx.drawImage(img, 0, 0, canvas.width, canvas.height);
        const originalImageData = tempCtx.getImageData(0, 0, canvas.width, canvas.height);
        
        // 开始故障艺术过渡动画
        const transitionDuration = 800; // 0.8秒，更快的过渡
        const transitionStartTime = Date.now();
        const glitchFrames = 30; // 增加故障效果的帧数，使闪烁更快
        let lastGlitchTime = 0;
        
        // 监听窗口大小变化
        window.addEventListener('resize', () => {
            glitchCanvas.width = canvas.width;
            glitchCanvas.height = canvas.height;
            
            // 重新绘制当前状态
            if (Date.now() - transitionStartTime < transitionDuration) {
                // 过渡还在进行中，重新绘制当前状态
                const progress = (Date.now() - transitionStartTime) / transitionDuration;
                updateTransition(progress);
            } else {
                // 过渡已完成，显示原始图片
                originalImage.style.opacity = '1';
            }
        });
        
        function applyGlitchEffect(imageData, intensity) {
            const data = new Uint8ClampedArray(imageData.data);
            const width = imageData.width;
            const height = imageData.height;
            
            // 随机选择几个水平条带进行位移
            const numStrips = Math.floor(10 + intensity * 20); // 增加条带数量
            
            for (let i = 0; i < numStrips; i++) {
                // 随机选择一个条带的位置和高度
                const stripY = Math.floor(Math.random() * height);
                const stripHeight = Math.floor(Math.random() * 15) + 1; // 增加条带高度
                const stripDisplacement = Math.floor((Math.random() - 0.5) * width * 0.3 * intensity); // 增加位移量
                
                // 位移条带
                for (let y = stripY; y < stripY + stripHeight && y < height; y++) {
                    for (let x = 0; x < width; x++) {
                        const sourceX = (x + stripDisplacement + width) % width;
                        const sourceIndex = (y * width + sourceX) * 4;
                        const targetIndex = (y * width + x) * 4;
                        
                        data[targetIndex] = imageData.data[sourceIndex];
                        data[targetIndex + 1] = imageData.data[sourceIndex + 1];
                        data[targetIndex + 2] = imageData.data[sourceIndex + 2];
                        data[targetIndex + 3] = imageData.data[sourceIndex + 3];
                    }
                }
            }
            
            // 随机RGB通道偏移
            if (Math.random() < intensity * 0.9) { // 增加概率
                const channelShift = Math.floor(intensity * 10); // 增加偏移量
                for (let i = 0; i < data.length; i += 4) {
                    // 随机选择一个通道进行偏移
                    const channel = Math.floor(Math.random() * 3);
                    if (channel === 0) {
                        data[i] = Math.min(255, data[i] + channelShift);
                    } else if (channel === 1) {
                        data[i + 1] = Math.min(255, data[i + 1] + channelShift);
                    } else {
                        data[i + 2] = Math.min(255, data[i + 2] + channelShift);
                    }
                }
            }
            
            // 随机噪点
            if (Math.random() < intensity * 0.8) { // 增加概率
                const noiseAmount = Math.floor(data.length * 0.02 * intensity); // 增加噪点数量
                for (let i = 0; i < noiseAmount; i++) {
                    const randomIndex = Math.floor(Math.random() * data.length / 4) * 4;
                    data[randomIndex] = Math.random() * 255;
                    data[randomIndex + 1] = Math.random() * 255;
                    data[randomIndex + 2] = Math.random() * 255;
                }
            }
            
            return new ImageData(data, width, height);
        }
        
        function transitionUpdate() {
            const now = Date.now();
            const progress = (now - transitionStartTime) / transitionDuration;
            
            if (progress >= 1) {
                // 过渡完成，直接显示原始图片（不使用叠化）
                // 先应用一次最强烈的故障效果
                const finalGlitchEffect = applyGlitchEffect(originalImageData, 1.0);
                glitchCtx.putImageData(finalGlitchEffect, 0, 0);
                
                // 短暂延迟后移除故障画布，直接显示原始图片
                setTimeout(() => {
                    glitchCanvas.remove();
                    // 直接显示原始图片，不使用透明度过渡
                    originalImage.style.transition = 'none';
                    originalImage.style.opacity = '1';
                }, 100);
                
                return;
            }
            
            updateTransition(progress);
            
            // 继续动画
            requestAnimationFrame(transitionUpdate);
        }
        
        function updateTransition(progress) {
            // 清除过渡Canvas
            glitchCtx.clearRect(0, 0, canvas.width, canvas.height);
            
            // 创建一个新的ImageData对象
            let newImageData;
            
            // 直接应用故障效果，不使用叠化
            const now = Date.now();
            const timeSinceLastGlitch = now - lastGlitchTime;
            const glitchInterval = 1000 / glitchFrames; // 控制故障效果的频率
            
            if (timeSinceLastGlitch >= glitchInterval) {
                lastGlitchTime = now;
                
                // 根据进度决定使用哪个图像数据
                let baseImageData;
                if (progress < 0.5) {
                    // 前半段使用ASCII艺术
                    baseImageData = asciiImageData;
                } else {
                    // 后半段使用原始图片
                    baseImageData = originalImageData;
                }
                
                // 应用故障效果，随着过渡进行增加强度
                const glitchIntensity = Math.sin(progress * Math.PI) * 0.8 + 0.2; // 使用正弦曲线，中间强度最大
                newImageData = applyGlitchEffect(baseImageData, glitchIntensity);
            } else {
                // 重用上一帧
                newImageData = glitchCtx.getImageData(0, 0, canvas.width, canvas.height);
            }
            
            // 将新的图像数据绘制到过渡Canvas上
            glitchCtx.putImageData(newImageData, 0, 0);
        }
        
        // 开始过渡动画
        canvas.style.opacity = '0';
        transitionUpdate();
    };
    
    img.src = originalImage.src;
}, 100); 