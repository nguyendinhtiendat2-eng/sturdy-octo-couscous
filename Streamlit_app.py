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
            <div class="title-neon">🎣 HỒ CÂU CHỌN TÊN - LITE 🌟</div>
            <div class="subtitle">TRÒ CHƠI CÂU CÁ TỐI ƯU, MƯỢT MÀ & ỔN ĐỊNH</div>
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
    # ----------------- GIAO DIỆN TRÒ CHƠI CÂU CÁ (TỐI ƯU NHẸ NHÀNG) -----------------
    st.markdown("### 🎣 Hồ Câu May Mắn - Giao Diện Ổn Định")

    names_list_py = st.session_state.names_list
    sound_flag_js = "true" if st.session_state.sound_enabled else "false"

    # Sử dụng chuỗi thô Python (không dùng f-string) kết hợp gán trực tiếp dữ liệu JSON để triệt tiêu hoàn toàn lỗi cú pháp
    import json

    names_json_str = json.dumps(names_list_py, ensure_ascii=False)

    game_html = (
        """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <style>
            body {
                margin: 0;
                background-color: #0e1117;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .game-container {
                position: relative;
                width: 100%;
                background: linear-gradient(to bottom, #1e3c72, #2a5298);
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                overflow: hidden;
                border: 2px solid rgba(255,255,255,0.1);
            }
            canvas {
                display: block;
                width: 100%;
                height: 460px;
                background: linear-gradient(to bottom, #87CEEB 0%, #3399ff 35%, #0066cc 70%, #003366 100%);
            }
            .control-panel {
                padding: 12px;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
            }
            .btn {
                width: 100%;
                max-width: 300px;
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
            }
            .btn:disabled {
                background: #555 !important;
                cursor: not-allowed;
                opacity: 0.6;
            }
            .btn-green {
                background: linear-gradient(135deg, #00b894, #55efc4) !important;
            }
            .status-text {
                font-size: 15px;
                font-weight: 600;
                text-align: center;
            }
            .winner-display {
                font-size: 17px;
                color: #ffeaa7;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <div class="game-container">
            <canvas id="gameCanvas" width="480" height="480"></canvas>
            <div class="control-panel">
                <button id="actionBtn" class="btn" onclick="handleAction()">🎣 Thả Cần Câu</button>
                <div class="status-text" id="statusText">Trạng thái: Sẵn sàng thả mồi...</div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const actionBtn = document.getElementById('actionBtn');
            const statusText = document.getElementById('statusText');

            let namesList = """
        + names_json_str
        + f""" ;
            let soundOn = {sound_flag_js};
            let gameState = 'IDLE'; 
            let hookY = 110;
            let targetHookY = 320;
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
                    osc.start(); osc.stop(audioCtx.currentTime + 0.3);
                }} else if (type === 'bite') {{
                    osc.frequency.setValueAtTime(600, audioCtx.currentTime);
                    osc.frequency.setValueAtTime(800, audioCtx.currentTime + 0.1);
                    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.25);
                }} else if (type === 'win') {{
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(523.25, audioCtx.currentTime);
                    osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.15);
                    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.4);
                }}
            }}

            class Fish {{
                constructor(name) {{
                    this.name = name;
                    this.x = Math.random() * canvas.width;
                    this.y = 180 + Math.random() * 240;
                    this.speed = (Math.random() * 1.2 + 0.6) * (Math.random() < 0.5 ? 1 : -1);
                    this.color = ['#ff7675', '#74b9ff', '#55efc4', '#ffeaa7', '#a29bfe'][Math.floor(Math.random() * 5)];
                    this.isTarget = false;
                }}
                update() {{
                    if (!this.isTarget) {{
                        this.x += this.speed;
                        if (this.x > canvas.width + 40) this.x = -40;
                        if (this.x < -40) this.x = canvas.width + 40;
                    }} else {{
                        let dx = 280 - this.x;
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
                    ctx.ellipse(0, 0, 24, 12, 0, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    ctx.moveTo(-24, 0);
                    ctx.lineTo(-34, -8);
                    ctx.lineTo(-34, 8);
                    ctx.closePath();
                    ctx.fill();

                    ctx.fillStyle = '#fff';
                    ctx.beginPath();
                    ctx.arc(10, -2, 2.5, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 11px Segoe UI';
                    ctx.textAlign = 'center';
                    ctx.shadowColor = 'rgba(0,0,0,0.8)';
                    ctx.shadowBlur = 4;
                    ctx.fillText(this.name, 0, -16);

                    ctx.restore();
                }}
            }}

            let poolFishes = [];
            namesList.forEach(name => {{
                poolFishes.push(new Fish(name));
            }});

            function drawScene() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Bờ đất
                ctx.fillStyle = '#4e311a';
                ctx.fillRect(0, 0, canvas.width, 100);
                ctx.fillStyle = '#2ecc71';
                ctx.fillRect(0, 95, canvas.width, 10);

                // Bảng tên
                ctx.fillStyle = '#d35400';
                ctx.fillRect(20, 15, 140, 40);
                ctx.strokeStyle = '#f39c12';
                ctx.lineWidth = 2;
                ctx.strokeRect(20, 15, 140, 40);
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 13px Segoe UI';
                ctx.textAlign = 'center';
                ctx.fillText("📜 HỒ CÂU TÊN", 90, 40);

                // Người câu
                ctx.fillStyle = '#2980b9';
                ctx.fillRect(360, 60, 26, 40);
                ctx.fillStyle = '#f5b041';
                ctx.beginPath();
                ctx.arc(373, 48, 10, 0, Math.PI * 2);
                ctx.fill();

                // Cần câu & Dây
                ctx.strokeStyle = '#7f8c8d';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(373, 60);
                ctx.lineTo(280, 25);
                ctx.stroke();

                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(280, 25);
                ctx.lineTo(280, hookY);
                ctx.stroke();

                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(280, hookY, 4, 0, Math.PI * 2);
                ctx.fill();

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
                        statusText.innerHTML = "⏳ Đang chờ cá cắn câu...";
                        
                        targetFish = poolFishes[Math.floor(Math.random() * poolFishes.length)];
                        targetFish.isTarget = true;
                        currentWinner = targetFish.name;

                        setTimeout(() => {{
                            if (gameState === 'WAITING') {{
                                gameState = 'BITING';
                                playSound('bite');
                                statusText.innerHTML = '🔥 CÁ CẮN CÂU: <b>' + currentWinner + '</b> - <span style="color:#00ff99;">KÉO LÊN!</span>';
                                actionBtn.innerHTML = "🎣 KÉO CÁ LÊN NGAY!";
                                actionBtn.className = "btn btn-green";
                            }}
                        }}, 1200);
                    }}
                }} else if (gameState === 'REELING') {{
                    hookY -= 7;
                    if (targetFish) {{
                        targetFish.y = hookY;
                        targetFish.x = 280;
                    }}
                    if (hookY <= 110) {{
                        hookY = 110;
                        gameState = 'CELEBRATING';
                        actionBtn.innerHTML = "⏳ ĐANG CHÚC MỪNG...";
                        actionBtn.disabled = true;
                        
                        playSound('win');
                        confetti({{ particleCount: 120, spread: 70, origin: {{ y: 0.6 }} }});

                        statusText.innerHTML = '<span class="winner-display">🎉 Chúc mừng: ' + currentWinner + ' đã trúng giải!</span>';
                        
                        if (targetFish) {{
                            targetFish.isTarget = false;
                            targetFish.x = -40;
                        }}
                        
                        window.parent.postMessage({{ type: 'streamlit:setComponentValue', value: currentWinner }}, '*');

                        setTimeout(() => {{
                            gameState = 'IDLE';
                            actionBtn.innerHTML = "🎣 Thả Cần Câu";
                            actionBtn.className = "btn";
                            actionBtn.disabled = false;
                            statusText.innerHTML = "Trạng thái: Sẵn sàng lượt tiếp theo!";
                        }}, 3000);
                    }}
                }}

                requestAnimationFrame(gameLoop);
            }}

            function handleAction() {{
                if (namesList.length === 0) {{
                    alert("Danh sách trống!");
                    return;
                }}
                if (gameState === 'CELEBRATING') return;

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
                    statusText.innerHTML = "❌ Kéo quá sớm, hụt mất rồi!";
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
    """,
        height=540,
    )

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
        st.subheader("⚙️ Điều khiển")
        if st.button("⬅️ Quay lại Menu & Sửa Bảng Tên"):
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
      
