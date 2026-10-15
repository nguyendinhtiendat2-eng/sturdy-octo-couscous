import random
import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Game Câu Cá Chọn Tên", page_icon="🎣", layout="wide"
)

# Khởi tạo session state
if "names_list" not in st.session_state:
    st.session_state.names_list = [
        "Nguyễn Văn A",
        "Trần Thị B",
        "Lê Văn C",
        "Phạm Thị D",
        "Hoàng Văn E",
        "Vũ Thị F",
    ]

if "history" not in st.session_state:
    st.session_state.history = []

if "remove_after_pick" not in st.session_state:
    st.session_state.remove_after_pick = False

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = True

# ----------------- MÀN HÌNH CHÍNH (MENU) -----------------
if not st.session_state.game_started:
    st.markdown(
        """
        <style>
            .main-menu {
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                padding: 25px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.8);
                border: 2px solid rgba(255, 100, 0, 0.4);
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .title-neon {
                font-size: 28px;
                font-weight: 900;
                color: #ff7675;
                text-shadow: 0 0 15px rgba(255, 118, 117, 0.8), 0 0 30px rgba(255, 71, 87, 0.6);
                margin-bottom: 5px;
            }
            .subtitle {
                font-size: 14px;
                color: #dfe6e9;
                margin-bottom: 15px;
                letter-spacing: 1px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-menu">
            <div class="title-neon">🎣 HỒ CÂU CHỌN TÊN - 3D STYLE 🌟</div>
            <div class="subtitle">TRÒ CHƠI CÂU CÁ ĐỒ HỌA CẢI TIẾN CAO CẤP</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_menu1, col_menu2 = st.columns([1, 1], gap="small")

    with col_menu1:
        st.markdown("### 📋 Bảng Ghi Tên Người Chơi")
        names_input = st.text_area(
            "Danh sách ứng viên:",
            value="\n".join(st.session_state.names_list),
            height=200,
            label_visibility="collapsed",
        )

        if st.button(
            "💾 Lưu lại danh sách tên",
            use_container_width=True,
            type="secondary",
        ):
            new_names = [
                n.strip() for n in names_input.split("\n") if n.strip()
            ]
            if new_names:
                st.session_state.names_list = new_names
                st.success(
                    f"Đã lưu thành công {len(new_names)} người vào bảng!"
                )
                st.rerun()
            else:
                st.error("Bảng tên không được để trống!")

    with col_menu2:
        st.markdown("### ⚙️ Thiết lập & Vào Game")

        st.markdown(
            f"""
            <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px;">
                <b>👥 Tổng số ứng viên:</b> <span style="color: #00cec9; font-size: 18px;">{len(st.session_state.names_list)} người</span><br>
                <b>🏆 Số lượt đã câu:</b> <span style="color: #fdcb6e; font-size: 18px;">{len(st.session_state.history)} lượt</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.session_state.remove_after_pick = st.checkbox(
            "Loại bỏ tên khỏi bảng sau khi câu trúng",
            value=st.session_state.remove_after_pick,
        )

        st.session_state.sound_enabled = st.toggle(
            "🔊 Bật âm thanh / hiệu ứng", value=st.session_state.sound_enabled
        )

        if st.button(
            "🔥 BẮT ĐẦU VÀO HỒ CÂU 🎣", type="primary", use_container_width=True
        ):
            if not st.session_state.names_list:
                st.error("Bảng tên đang trống! Vui lòng nhập tên trước khi vào.")
            else:
                st.session_state.game_started = True
                st.rerun()

        if st.button("🗑️ Xóa toàn bộ lịch sử câu", use_container_width=True):
            st.session_state.history = []
            st.success("Đã xóa lịch sử!")
            st.rerun()

else:
    # ----------------- GIAO DIỆN TRÒ CHƠI CÂU CÁ (ĐỒ HỌA ĐẸP MẮT) -----------------
    st.markdown("### 🎣 Hồ Câu May Mắn - Đồ Họa Nâng Cấp")

    current_names_json = st.session_state.names_list
    sound_flag = "true" if st.session_state.sound_enabled else "false"

    game_html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <style>
            body {{
                margin: 0;
                background-color: #0e1117;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .game-container {{
                position: relative;
                width: 100%;
                background: linear-gradient(to bottom, #1e3c72, #2a5298);
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                overflow: hidden;
                border: 2px solid rgba(255,255,255,0.1);
            }}
            canvas {{
                display: block;
                width: 100%;
                height: 500px;
                background: linear-gradient(to bottom, #b3e0ff 0%, #3399ff 30%, #0066cc 60%, #003366 100%);
            }}
            .control-panel {{
                padding: 12px;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
            }}
            .btn {{
                width: 100%;
                max-width: 320px;
                background: linear-gradient(135deg, #ff4b4b, #ff7675);
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
            }}
            .btn:disabled {{
                background: #555 !important;
                cursor: not-allowed;
                box-shadow: none;
                opacity: 0.6;
            }}
            .btn-green {{
                background: linear-gradient(135deg, #00b894, #55efc4) !important;
                box-shadow: 0 4px 15px rgba(0, 184, 148, 0.4) !important;
            }}
            .status-text {{
                font-size: 15px;
                font-weight: 600;
                text-align: center;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
            }}
            .winner-display {{
                font-size: 17px;
                color: #ffeaa7;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>

        <div class="game-container">
            <canvas id="gameCanvas" width="500" height="520"></canvas>
            <div class="control-panel">
                <button id="actionBtn" class="btn" onclick="handleAction()">🎣 Thả Cần Câu</button>
                <div class="status-text" id="statusText">Trạng thái: Đàn cá đang bơi lội trong hồ...</div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const actionBtn = document.getElementById('actionBtn');
            const statusText = document.getElementById('statusText');

            let namesList = {current_names_json};
            let soundOn = {sound_flag};
            let gameState = 'IDLE'; 
            let hookY = 130;
            let targetHookY = 350;
            let targetFish = null;
            let currentWinner = "";

            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            function playSound(type) {{
                if (!soundOn) return;
                if (audioCtx.state === 'suspended') {{ audioCtx.resume(); }}
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                
                if (type === 'cast') {{
                    osc.frequency.setValueAtTime(400, audioCtx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(200, audioCtx.currentTime + 0.3);
                    gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                    gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.3);
                }} else if (type === 'bite') {{
                    osc.frequency.setValueAtTime(600, audioCtx.currentTime);
                    osc.frequency.setValueAtTime(800, audioCtx.currentTime + 0.1);
                    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                    gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.25);
                }} else if (type === 'win') {{
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(523.25, audioCtx.currentTime);
                    osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.15);
                    osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.3);
                    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                    gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.5);
                }}
            }}

            class Fish {{
                constructor(name) {{
                    this.name = name;
                    this.x = Math.random() * canvas.width;
                    this.y = 220 + Math.random() * 260;
                    this.speed = (Math.random() * 1.4 + 0.7) * (Math.random() < 0.5 ? 1 : -1);
                    this.color = ['#ff7675', '#74b9ff', '#55efc4', '#ffeaa7', '#a29bfe', '#fab1a0'][Math.floor(Math.random() * 6)];
                    this.isTarget = false;
                    this.tailWag = Math.random() * Math.PI;
                }}
                update() {{
                    if (!this.isTarget) {{
                        this.x += this.speed;
                        this.tailWag += 0.15;
                        if (this.x > canvas.width + 50) this.x = -50;
                        if (this.x < -50) this.x = canvas.width + 50;
                    }} else {{
                        let dx = 320 - this.x;
                        let dy = hookY - this.y;
                        this.x += dx * 0.1;
                        this.y += dy * 0.1;
                    }}
                }}
                draw() {{
                    ctx.save();
                    ctx.translate(this.x, this.y);
                    if (this.speed < 0 && !this.isTarget) ctx.scale(-1, 1);
                    
                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    ctx.ellipse(0, 0, 28, 14, 0, 0, Math.PI * 2);
                    ctx.fill();
                    
                    ctx.strokeStyle = 'rgba(255,255,255,0.6)';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();

                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    let tailOffset = Math.sin(this.tailWag) * 4;
                    ctx.moveTo(-28, 0);
                    ctx.lineTo(-40, -10 + tailOffset);
                    ctx.lineTo(-40, 10 + tailOffset);
                    ctx.closePath();
                    ctx.fill();

                    ctx.fillStyle = '#fff';
                    ctx.beginPath();
                    ctx.arc(12, -3, 3.5, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#000';
                    ctx.beginPath();
                    ctx.arc(13, -3, 1.5, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 12px Segoe UI';
                    ctx.textAlign = 'center';
                    ctx.shadowColor = 'rgba(0,0,0,0.9)';
                    ctx.shadowBlur = 5;
                    ctx.fillText(this.name, 0, -20);

                    ctx.restore();
                }}
            }}

            let poolFishes = [];
            function initPool() {{
                poolFishes = [];
                namesList.forEach(name => {{
                    poolFishes.push(new Fish(name));
                }});
            }}
            initPool();

            function drawScene() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#4e311a';
                ctx.fillRect(0, 0, canvas.width, 120);
                
                ctx.fillStyle = '#2ecc71';
                ctx.beginPath();
                ctx.moveTo(0, 115);
                for(let i=0; i<=canvas.width; i+=20) {{
                    ctx.lineTo(i, 110 + Math.sin(i)*4);
                }}
                ctx.lineTo(canvas.width, 130);
                ctx.lineTo(0, 130);
                ctx.fill();

                ctx.fillStyle = '#6e2c00';
                ctx.fillRect(45, 55, 8, 65);
                ctx.fillRect(135, 55, 8, 65);
                
                let gradientBoard = ctx.createLinearGradient(20, 20, 170, 70);
                gradientBoard.addColorStop(0, '#d35400');
                gradientBoard.addColorStop(1, '#ba4a00');
                ctx.fillStyle = gradientBoard;
                ctx.fillRect(20, 20, 155, 50);
                ctx.strokeStyle = '#f39c12';
                ctx.lineWidth = 3;
                ctx.strokeRect(20, 20, 155, 50);

                ctx.fillStyle = '#fff';
                ctx.font = 'bold 15px Segoe UI';
                ctx.textAlign = 'center';
                ctx.fillText("📜 HỒ CÂU TÊN", 97, 50);

                ctx.fillStyle = '#2980b9';
                ctx.fillRect(380, 75, 30, 45);
                ctx.fillStyle = '#f5b041';
                ctx.beginPath();
                ctx.arc(395, 60, 13, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(395, 55, 16, Math.PI, 2 * Math.PI);
                ctx.fill();

                ctx.strokeStyle = '#7f8c8d';
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.moveTo(395, 75);
                ctx.lineTo(320, 35);
                ctx.stroke();

                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.2;
                ctx.beginPath();
                ctx.moveTo(320, 35);
                ctx.lineTo(320, hookY);
                ctx.stroke();

                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(320, hookY, 5, 0, Math.PI * 2);
                ctx.fill();

                poolFishes.forEach(fish => {{
                    fish.update();
                    fish.draw();
                }});
            }}

            function gameLoop() {{
                drawScene();

                if (gameState === 'CASTING') {{
                    hookY += 6;
                    if (hookY >= targetHookY) {{
                        hookY = targetHookY;
                        gameState = 'WAITING';
                        statusText.innerHTML = "⏳ Đang thả mồi... Cá đang bơi tới!";
                        
                        targetFish = poolFishes[Math.floor(Math.random() * poolFishes.length)];
                        targetFish.isTarget = true;
                        currentWinner = targetFish.name;

                        let waitTime = 1200 + Math.random() * 1200;
                        setTimeout(() => {{
                            if (gameState === 'WAITING') {{
                                gameState = 'BITING';
                                playSound('bite');
                                statusText.innerHTML = '🔥 CÁ CẮN CÂU! [<b>' + currentWinner + '</b>] - <span style="color:#00ff99;">KÉO LÊN NGAY!</span>';
                                actionBtn.innerHTML = "🎣 KÉO CÁ LÊN NGAY!";
                                actionBtn.className = "btn btn-green";
                            }}
                        }}, waitTime);
                    }}
                }} else if (gameState === 'REELING') {{
                    hookY -= 8;
                    if (targetFish) {{
                        targetFish.y = hookY;
                        targetFish.x = 320;
                    }}
                    if (hookY <= 130) {{
                        hookY = 130;
                        gameState = 'CELEBRATING';
                        actionBtn.innerHTML = "⏳ ĐANG CHÚC MỪNG... XIN ĐỢI";
                        actionBtn.disabled = true;
                        
                        playSound('win');
                        confetti({{ particleCount: 150, spread: 90, origin: {{ y: 0.6 }} }});

                        statusText.innerHTML = '<span class="winner-display">🎉 Chúc mừng: ' + currentWinner + ' đã trúng giải!</span>';
                        
                        if (targetFish) {{
                            targetFish.isTarget = false;
                            targetFish.x = -50;
                        }}
                        
                        window.parent.postMessage({{ type: 'streamlit:setComponentValue', value: currentWinner }}, '*');

                        setTimeout(() => {{
                            gameState = 'IDLE';
                            actionBtn.innerHTML = "🎣 Thả Cần Câu";
                            actionBtn.className = "btn";
                            actionBtn.disabled = false;
                            statusText.innerHTML = "Trạng thái: Sẵn sàng cho lượt câu tiếp theo!";
                        }}, 3500);
                    }}
                }}

                requestAnimationFrame(gameLoop);
            }}

            function handleAction() {{
                if (namesList.length === 0) {{
                    alert("Danh sách người chơi trống!");
                    return;
                }}

                if (gameState === 'CELEBRATING') return;

                if (gameState === 'IDLE') {{
                    playSound('cast');
                    gameState = 'CASTING';
                    actionBtn.innerHTML = "Đang thả cần...";
                    actionBtn.disabled = true;
                    statusText.innerHTML = "🎣 Đang thả mồi xuống hồ...";
                    setTimeout(() => {{ actionBtn.disabled = false; }}, 600);
                }} 
                else if (gameState === 'WAITING') {{
                    gameState = 'REELING';
                    statusText.innerHTML = "❌ Kéo quá sớm, cá chưa kịp cắn!";
                    actionBtn.innerHTML = "🎣 Thả Cần Câu";
                    actionBtn.className = "btn";
                    if(targetFish) targetFish.isTarget = false;
                }} 
                else if (gameState === 'BITING'
