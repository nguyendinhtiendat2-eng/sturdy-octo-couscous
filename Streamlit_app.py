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

# Sidebar quản lý danh sách
with st.sidebar:
    st.header("⚙️ Cài đặt Game Câu Cá")
    names_input = st.text_area(
        "Nhập danh sách tên (mỗi dòng 1 tên):",
        value="\n".join(st.session_state.names_list),
        height=150,
    )

    if st.button("💾 Cập nhật danh sách", use_container_width=True):
        new_names = [
            n.strip() for n in names_input.split("\n") if n.strip()
        ]
        if new_names:
            st.session_state.names_list = new_names
            st.success(f"Đã cập nhật {len(new_names)} người chơi!")
            st.rerun()

    st.session_state.remove_after_pick = st.checkbox(
        "Loại bỏ tên sau khi câu được",
        value=st.session_state.remove_after_pick,
    )

    if st.button("🗑️ Xóa lịch sử", use_container_width=True):
        st.session_state.history = []
        st.success("Đã xóa lịch sử!")
        st.rerun()

# ----------------- MÀN HÌNH CHÍNH (MENU) -----------------
if not st.session_state.game_started:
    st.markdown(
        """
        <style>
            .main-menu {
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.8);
                border: 2px solid rgba(255, 100, 0, 0.4);
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .title-neon {
                font-size: 38px;
                font-weight: 900;
                color: #ff7675;
                text-shadow: 0 0 15px rgba(255, 118, 117, 0.8), 0 0 30px rgba(255, 71, 87, 0.6);
                margin-bottom: 5px;
            }
            .subtitle {
                font-size: 16px;
                color: #dfe6e9;
                margin-bottom: 30px;
                letter-spacing: 1px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-menu">
            <div class="title-neon">🎣 HỒ CÂU CHỌN TÊN 🌟</div>
            <div class="subtitle">GIAO DIỆN CHỌN NGƯỜI NGẪU NHIÊN QUA TRÒ CHƠI CÂU CÁ</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
    with col_m2:
        st.markdown(
            f"""
            <div style="text-align: center; margin: 20px 0;">
                <b>👥 Tổng số ứng viên sẵn sàng:</b> <span style="color: #00cec9; font-size: 22px;">{len(st.session_state.names_list)} người</span><br>
                <b>🏆 Số lượt đã câu:</b> <span style="color: #fdcb6e; font-size: 22px;">{len(st.session_state.history)} lượt</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.session_state.sound_enabled = st.toggle(
            "🔊 Bật âm thanh / hiệu ứng", value=st.session_state.sound_enabled
        )

        if st.button(
            "🔥 BẮT ĐẦU VÀO HỒ CÂU 🎣", type="primary", use_container_width=True
        ):
            if not st.session_state.names_list:
                st.error("Danh sách trống! Vui lòng thêm tên ở thanh bên.")
            else:
                st.session_state.game_started = True
                st.rerun()

else:
    # ----------------- GIAO DIỆN TRÒ CHƠI CÂU CÁ -----------------
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3>🎣 Hồ Câu May Mắn - Thả Cần Bắt Tên</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current_names_json = st.session_state.names_list
    sound_flag = "true" if st.session_state.sound_enabled else "false"

    game_html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
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
                justify-content: center;
            }}
            .game-container {{
                position: relative;
                width: 100%;
                max-width: 800px;
                background: linear-gradient(to bottom, #1e3c72, #2a5298);
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                overflow: hidden;
                border: 2px solid rgba(255,255,255,0.1);
            }}
            canvas {{
                display: block;
                background: linear-gradient(to bottom, #70a1ff 0%, #1e90ff 25%, #0984e3 40%, #002d62 100%);
            }}
            .control-panel {{
                padding: 15px;
                background: rgba(0, 0, 0, 0.6);
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            }}
            .btn {{
                background: linear-gradient(135deg, #ff4b4b, #ff7675);
                color: white;
                border: none;
                padding: 12px 28px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
            }}
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(255, 75, 75, 0.6);
            }}
            .btn-green {{
                background: linear-gradient(135deg, #00b894, #55efc4) !important;
                box-shadow: 0 4px 15px rgba(0, 184, 148, 0.4) !important;
            }}
            .status-text {{
                font-size: 16px;
                font-weight: 600;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
            }}
            .winner-display {{
                font-size: 18px;
                color: #ffeaa7;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>

        <div class="game-container">
            <canvas id="gameCanvas" width="800" height="420"></canvas>
            <div class="control-panel">
                <button id="actionBtn" class="btn" onclick="handleAction()">🎣 Thả Cần Câu</button>
                <div class="status-text" id="statusText">Trạng thái: Đàn cá đang bơi quanh hồ...</div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const actionBtn = document.getElementById('actionBtn');
            const statusText = document.getElementById('statusText');

            let namesList = {current_names_json};
            let soundOn = {sound_flag};
            let gameState = 'IDLE'; // IDLE, CASTING, WAITING, BITING, REELING
            let hookY = 60;
            let targetHookY = 220;
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

            // Class Đại diện cho những chú cá bơi xung quanh hồ
            class Fish {{
                constructor(name) {{
                    this.name = name;
                    this.x = Math.random() * canvas.width;
                    this.y = 130 + Math.random() * 250;
                    this.speed = (Math.random() * 1.2 + 0.6) * (Math.random() < 0.5 ? 1 : -1);
                    this.color = ['#ff7675', '#74b9ff', '#55efc4', '#ffeaa7', '#a29bfe', '#fab1a0'][Math.floor(Math.random() * 6)];
                    this.isTarget = false;
                }}
                update() {{
                    if (!this.isTarget) {{
                        this.x += this.speed;
                        if (this.x > canvas.width + 50) this.x = -50;
                        if (this.x < -50) this.x = canvas.width + 50;
                    }} else {{
                        // Khi được chọn, bơi thẳng đến vị trí lưỡi câu (x = 520, y = hookY)
                        let dx = 520 - this.x;
                        let dy = hookY - this.y;
                        this.x += dx * 0.08;
                        this.y += dy * 0.08;
                    }}
                }}
                draw() {{
                    ctx.save();
                    ctx.translate(this.x, this.y);
                    if (this.speed < 0 && !this.isTarget) ctx.scale(-1, 1);
                    
                    // Thân cá nhỏ gọn
                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    ctx.ellipse(0, 0, 30, 15, 0, 0, Math.PI * 2);
                    ctx.fill();

                    // Đuôi cá
                    ctx.beginPath();
                    ctx.moveTo(-30, 0);
                    ctx.lineTo(-42, -8);
                    ctx.lineTo(-42, 8);
                    ctx.closePath();
                    ctx.fill();

                    // Mắt cá
                    ctx.fillStyle = '#000';
                    ctx.beginPath();
                    ctx.arc(14, -3, 2.5, 0, Math.PI * 2);
                    ctx.fill();

                    // TÊN HIỂN THỊ TRÊN THÂN CÁ
                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 12px Segoe UI';
                    ctx.textAlign = 'center';
                    ctx.shadowColor = 'rgba(0,0,0,0.9)';
                    ctx.shadowBlur = 4;
                    ctx.fillText(this.name, 0, -20);

                    ctx.restore();
                }}
            }}

            // Khởi tạo đàn cá bơi xung quanh hồ tương ứng với danh sách tên
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

                // 1. Bờ đất phía trên
                ctx.fillStyle = '#3d2817';
                ctx.fillRect(0, 0, canvas.width, 80);
                
                ctx.fillStyle = '#27ae60';
                ctx.fillRect(0, 75, canvas.width, 10);

                // 2. NGƯỜI CÂU TRÊN BỜ (Cầm cần câu)
                ctx.fillStyle = '#e17055';
                ctx.fillRect(660, 40, 24, 38); // Thân người
                
                ctx.fillStyle = '#ffeaa7';
                ctx.beginPath();
                ctx.arc(672, 28, 12, 0, Math.PI * 2);
                ctx.fill(); // Đầu người
                
                // Cần câu dài hướng ra mặt nước
                ctx.strokeStyle = '#d35400';
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.moveTo(672, 40);
                ctx.lineTo(520, 10);
                ctx.stroke();

                // 3. Dây câu thả xuống nước
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(520, 10);
                ctx.lineTo(520, hookY);
                ctx.stroke();

                // Lưỡi câu vàng
                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(520, hookY, 5, 0, Math.PI * 2);
                ctx.fill();

                // 4. Cập nhật và vẽ toàn bộ đàn cá bơi xung quanh
                poolFishes.forEach(fish => {{
                    fish.update();
                    fish.draw();
                }});
            }}

            function gameLoop() {{
                drawScene();

                if (gameState === 'CASTING') {{
                    hookY += 5;
                    if (hookY >= targetHookY) {{
                        hookY = targetHookY;
                        gameState = 'WAITING';
                        statusText.innerHTML = "⏳ Đang thả mồi... Đàn cá đang bơi lại!";
                        
                        // Chọn ngẫu nhiên 1 con cá từ đàn làm con mồi cắn câu
                        targetFish = poolFishes[Math.floor(Math.random() * poolFishes.length)];
                        targetFish.isTarget = true;
                        currentWinner = targetFish.name;

                        // Sau 1.5 giây cá bơi tới mồi và cắn
                        setTimeout(() => {{
                            if (gameState === 'WAITING') {{
                                gameState = 'BITING';
                                playSound('bite');
                                statusText.innerHTML = `🔥 CÁ CẮN CÂU! [<b>${{currentWinner}}</b>] - <span style='color:#00ff99;'>BẤM KÉO LÊN NGAY!</span>`;
                                actionBtn.innerHTML = "🎣 KÉO CÁ LÊN NGAY!";
                                actionBtn.className = "btn btn-green";
                            }}
                        }}, 1500);
                    }}
                }} else if (gameState === 'REELING') {{
                    hookY -= 7;
                    if (targetFish) {{
                        targetFish.y = hookY; // Cá dính câu kéo lên theo lưỡi
                        targetFish.x = 520;
                    }}
                    if (hookY <= 60) {{
                        hookY = 60;
                        gameState = 'IDLE';
                        actionBtn.innerHTML = "🎣 Thả Cần Câu";
                        actionBtn.className = "btn";
                        
                        playSound('win');
                        confetti({{ particleCount: 120, spread: 80, origin: {{ y: 0.6 }} }});

                        statusText.innerHTML = `<span class="winner-display">🎉 Chúc mừng: ${{currentWinner}} đã trúng giải!</span>`;
                        
                        // Tái tạo lại con cá đó bơi tiếp vào đàn
                        if (targetFish) {{
                            targetFish.isTarget = false;
                            targetFish.x = -50;
                        }}
                        
                        window.parent.postMessage({{ type: 'streamlit:setComponentValue', value: currentWinner }}, '*');
                    }}
                }}

                requestAnimationFrame(gameLoop);
            }}

            function handleAction() {{
                if (namesList.length === 0) {{
                    alert("Danh sách người chơi trống!");
                    return;
                }}

                if (gameState === 'IDLE') {{
                    playSound('cast');
                    gameState = 'CASTING';
                    actionBtn.innerHTML = "Đang thả cần...";
                    actionBtn.disabled = true;
                    statusText.innerHTML = "🎣 Đang thả mồi xuống hồ...";
                    setTimeout(() => {{ actionBtn.disabled = false; }}, 500);
                }} 
                else if (gameState === 'WAITING') {{
                    gameState = 'REELING';
                    statusText.innerHTML = "❌ Kéo quá sớm, cá chưa kịp cắn!";
                    actionBtn.innerHTML = "🎣 Thả Cần Câu";
                    actionBtn.className = "btn";
                    if(targetFish) targetFish.isTarget = false;
                }} 
                else if (gameState === 'BITING') {{
                    gameState = 'REELING';
                    actionBtn.innerHTML = "Đang kéo lên...";
                    actionBtn.className = "btn";
                }}
            }}

            gameLoop();
        </script>
    </body>
    </html>
    """

    components.html(game_html, height=480)

    st.markdown("---")
    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        st.subheader("📜 Lịch sử câu cá")
        if st.session_state.history:
            for idx, item in enumerate(
                reversed(st.session_state.history), 1
            ):
                st.markdown(
                    f"**{idx}.** Trúng tên: <span style='color: #fdcb6e; font-weight: bold;'>{item}</span>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("Chưa có lượt câu nào.")

    with col_c2:
        st.subheader("⚙️ Điều khiển nhanh")
        if st.button("⬅️ Quay lại Menu chính"):
            st.session_state.game_started = False
            st.rerun()

        manual_winner = st.selectbox(
            "Chọn thủ công phòng hờ:", st.session_state.names_list
        )
        if st.button("🎉 Lưu kết quả thủ công"):
            if manual_winner:
                st.session_state.history.append(manual_winner)
                if st.session_state.remove_after_pick:
                    st.session_state.names_list.remove(manual_winner)
                st.success(f"Đã lưu: **{manual_winner}**!")
                st.rerun()
      
