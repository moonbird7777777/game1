import streamlit as st
import random

# 设置页面配置
st.set_page_config(
    page_title="躲避游戏",
    page_icon="🎮",
    layout="centered"
)

# 自定义CSS样式
st.markdown("""
<style>
#gameCanvas {
    border: 2px solid #333;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.game-container {
    text-align: center;
    margin: 20px 0;
}

.controls {
    background: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
    margin: 15px 0;
    border-left: 4px solid #ff4b4b;
}

.score {
    font-size: 1.5em;
    font-weight: bold;
    color: #ff4b4b;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def create_game():
    """创建游戏HTML和JavaScript"""
    game_html = """
    <div class="game-container">
        <div class="score">得分: <span id="score">0</span></div>
        <canvas id="gameCanvas" width="800" height="500"></canvas>
        <div class="controls">
            <p>🎮 使用 <strong>← →</strong> 方向键控制小球移动</p>
            <p>🎯 躲避红色障碍物，坚持越久得分越高！</p>
        </div>
    </div>

    <script>
    // 获取Canvas和上下文
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    // 游戏变量
    let score = 0;
    let gameRunning = true;

    // 小球属性
    const ball = {
        x: canvas.width / 2,
        y: canvas.height - 60,
        size: 30,
        speed: 8,
        color: '#2c3e50'
    };

    // 障碍物属性
    const obstacle = {
        x: Math.random() * (canvas.width - 100),
        y: -30,
        width: 100,
        height: 20,
        speed: 5,
        color: '#e74c3c'
    };

    // 键盘控制
    const keys = {};
    window.addEventListener('keydown', (e) => {
        keys[e.key] = true;
    });
    window.addEventListener('keyup', (e) => {
        keys[e.key] = false;
    });

    // 绘制小球
    function drawBall() {
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2);
        ctx.fillStyle = ball.color;
        ctx.fill();
        ctx.closePath();
        
        // 添加小球内部光晕
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.size - 8, 0, Math.PI * 2);
        ctx.fillStyle = '#3498db';
        ctx.fill();
        ctx.closePath();
    }

    // 绘制障碍物
    function drawObstacle() {
        ctx.fillStyle = obstacle.color;
        ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
        
        // 添加障碍物阴影
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.fillRect(obstacle.x, obstacle.y + obstacle.height, obstacle.width, 5);
    }

    // 检测碰撞
    function checkCollision() {
        return ball.x + ball.size > obstacle.x &&
               ball.x - ball.size < obstacle.x + obstacle.width &&
               ball.y + ball.size > obstacle.y &&
               ball.y - ball.size < obstacle.y + obstacle.height;
    }

    // 更新游戏状态
    function update() {
        if (!gameRunning) return;

        // 清除画布
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 移动小球
        if (keys['ArrowLeft'] && ball.x > ball.size) {
            ball.x -= ball.speed;
        }
        if (keys['ArrowRight'] && ball.x < canvas.width - ball.size) {
            ball.x += ball.speed;
        }

        // 移动障碍物
        obstacle.y += obstacle.speed;
        if (obstacle.y > canvas.height) {
            obstacle.y = -obstacle.height;
            obstacle.x = Math.random() * (canvas.width - obstacle.width);
            score += 1;
            document.getElementById('score').textContent = score;
            
            // 每得5分增加难度
            if (score % 5 === 0) {
                obstacle.speed += 0.5;
                ball.speed += 0.3;
            }
        }

        // 检查碰撞
        if (checkCollision()) {
            gameRunning = false;
            showGameOver();
        }

        // 绘制游戏元素
        drawBall();
        drawObstacle();
        
        // 绘制背景网格
        drawGrid();
        
        // 继续游戏循环
        requestAnimationFrame(update);
    }

    // 绘制背景网格
    function drawGrid() {
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.lineWidth = 1;
        
        // 垂直线
        for (let x = 0; x < canvas.width; x += 50) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }
        
        // 水平线
        for (let y = 0; y < canvas.height; y += 50) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }
    }

    // 显示游戏结束
    function showGameOver() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.font = 'bold 48px Arial';
        ctx.fillStyle = '#e74c3c';
        ctx.textAlign = 'center';
        ctx.fillText('游戏结束!', canvas.width / 2, canvas.height / 2 - 50);
        
        ctx.font = '36px Arial';
        ctx.fillStyle = '#ecf0f1';
        ctx.fillText('最终得分: ' + score, canvas.width / 2, canvas.height / 2 + 20);
        
        ctx.font = '24px Arial';
        ctx.fillStyle = '#bdc3c7';
        ctx.fillText('刷新页面重新开始', canvas.width / 2, canvas.height / 2 + 70);
    }

    // 开始游戏
    function startGame() {
        // 绘制初始界面
        ctx.fillStyle = '#34495e';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.font = 'bold 36px Arial';
        ctx.fillStyle = '#ecf0f1';
        ctx.textAlign = 'center';
        ctx.fillText('躲避游戏', canvas.width / 2, canvas.height / 2 - 30);
        
        ctx.font = '20px Arial';
        ctx.fillStyle = '#bdc3c7';
        ctx.fillText('按任意方向键开始游戏', canvas.width / 2, canvas.height / 2 + 30);
        
        // 等待用户输入开始游戏
        function waitForStart(e) {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                window.removeEventListener('keydown', waitForStart);
                update();
            }
        }
        
        window.addEventListener('keydown', waitForStart);
    }

    // 初始化游戏
    startGame();
    </script>
    """
    return game_html

def main():
    # 游戏标题
    st.title("🎮 Streamlit 躲避游戏")
    
    # 游戏说明
    st.markdown("""
    ### 游戏规则：
    - 使用 **← →** 方向键控制小球移动
    - 躲避从上方落下的红色障碍物
    - 每成功躲避一个障碍物得1分
    - 每得5分游戏速度会增加
    - 碰到障碍物游戏结束
    """)
    
    # 创建游戏
    game_html = create_game()
    st.markdown(game_html, unsafe_allow_html=True)
    
    # 游戏提示
    st.info("💡 **提示**: 游戏需要键盘控制，请确保焦点在游戏画面上")

if __name__ == '__main__':
    main()
