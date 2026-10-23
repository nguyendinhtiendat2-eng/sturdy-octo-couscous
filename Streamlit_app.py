import json
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

if "pending_winner" not in st.session_state:
    st.session_state.pending_winner = None

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
            <div class="title-neon">🎣 HỒ CÂU CHỌN TÊN - 3D CHÂN THỰC 🌟</div>
            <div class="subtitle">TRÒ CHƠI CÂU CÁ ĐỒ HỌA NÂNG CẤP</div>
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

        # Cài đặt file nhạc "Sandwich & Story" từ máy
        st.markdown("### 🎵 Nhạc nền (Sandwich & Story)")
        music_file = st.file_uploader(
            "Tải file nhạc từ máy của bạn (.mp3 / .wav):",
            type=["mp3", "wav"],
        )
        if music_file is not None:
            st.session_state.custom_music = music_file
            st.success("Đã tải nhạc nền thành công!")

        st.session_state.remove_after_pick = st.checkbox(
            "Loại bỏ tên khỏi bảng sau khi câu trúng",
            value=st.session_state.remove_after_pick,
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
    # ----------------- GIAO DIỆN TRÒ CHƠI CÂU CÁ -----------------
    st.markdown("### 🎣 Hồ Câu May Mắn - Sống động & Chân thực")

    # Phát nhạc nền từ file tải lên
    if (
        "custom_music" in st.session_state
        and st.session_state.custom_music is not None
    ):
        st.audio(st.session_state.custom_music, format="audio/mp3", loop=True)

    # Hiển thị bảng quyết định Xóa hoặc Giữ lại nếu vừa câu trúng cá
    if st.session_state.pending_winner:
        winner = st.session_state.pending_winner
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #f39c12, #d35400); padding: 22px; border-radius: 12px; text-align: center; margin-bottom: 15px; border: 2px solid #f1c40f; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
                <h2 style="margin: 0; color: #fff;">🎉 KẾT QUẢ CÂU TRÚNG: <span style="color: #ffeaa7; font-size: 32px;">{winner}</span></h2>
                <p style="margin: 8px 0 0 0; color: #fff; font-size: 16px;">Bạn muốn xử lý tên chú cá này như thế nào?</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            if st.button(
                "🗑️ XÓA TÊN NÀY KHỎI BẢNG",
                type="primary",
                use_container_width=True,
            ):
                if winner in st.session_state.names_list:
                    st.session_state.names_list.remove(winner)
                st.session_state.history.append(winner)
                st.session_state.pending_winner = None
                st.success(
                    f"Đã xóa **{winner}** khỏi bảng và lưu vào lịch sử!"
                )
                st.rerun()
        with col_opt2:
            if st.button(
                "🛡️ GIỮ LẠI TÊN TRONG BẢNG", use_container_width=True
            ):
                st.session_state.history.append(winner)
                st.session_state.pending_winner = None
                st.success(
                    f"Đã giữ lại **{winner}** trong bảng và lưu vào lịch sử!"
                )
                st.rerun()

    names_json_str = json.dumps(
        st.session_state.names_list, ensure_ascii=False
    )

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
                height: 460px;
                background: linear-gradient(to bottom, #87CEEB 0%, #3399ff 35%, #0066cc 70%, #003366 100%);
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
            }}
            .btn:disabled {{
                background: #555 !important;
                cursor: not-allowed;
                opacity: 0.6;
            }}
            .btn-green {{
                background: linear-gradient(135deg, #00b894, #55efc4) !important;
            }}
            .status-text {{
                font-size: 15px;
                font-weight: 600;
                text-align: center;
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
            <canvas id="gameCanvas" width="480" height="460"></canvas>
            <div class="control-panel">
                <button id="actionBtn" class="btn" onclick="handleAction()">🎣 Thả Cần Câu</button>
                <div class="status-text" id="statusText">Trạng thái: Đàn cá đang bơi lội tự nhiên...</div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const actionBtn = document.getElementById('actionBtn');
            const statusText = document.getElementById('statusText');

            let namesList = {names_json_str};
            let gameState = 'IDLE'; 
            let hookY = 110;
            let targetHookY = 320;
            let targetFish = null;
            let currentWinner = "";

            class Fish {{
                constructor(name) {{
                    this.name = name;
                    this.x = Math.random() * canvas.width;
                    this.y = 180 + Math.random() * 240;
                    this.speed = (Math.random() * 1.2 + 0.6) * (Math.random() < 0.5 ? 1 : -1);
                    this.color = ['#ff7675', '#74b9ff', '#55efc4', '#ffeaa7', '#a29bfe'][Math.floor(Math.random() * 5)];
                    this.isTarget = false;
                    this.tailWag = Math.random() * Math.PI;
                }}
                update() {{
                    if (!this.isTarget) {{
                        this.x += this.speed;
                        this.tailWag += 0.15;
                        if (this.x > canvas.width + 40) this.x = -40;
                        if (this.x < -40) this.x = canvas.width + 40;
                    }} else {{
                        // Bơi mượt mà chuẩn xác vào ngay vị trí lưỡi câu ở x=280, y=hookY
                        let dx = 280 - this.x;
                        let dy = hookY - this.y;
                        this.x += dx * 0.12;
                        this.y += dy * 0.12;
                    }}
                }}
                draw() {{
                    ctx.save();
                    ctx.translate(this.x, this.y);
                    if (this.speed < 0 && !this.isTarget) ctx.scale(-1, 1);
                    
                    // Thân cá
                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    ctx.ellipse(0, 0, 26, 13, 0, 0, Math.PI * 2);
                    ctx.fill();

                    // Đuôi cá vẫy tự nhiên
                    ctx.beginPath();
                    let tailOffset = Math.sin(this.tailWag) * 4;
                    ctx.moveTo(-26, 0);
                    ctx.lineTo(-36, -8 + tailOffset);
                    ctx.lineTo(-36, 8 + tailOffset);
                    ctx.closePath();
                    ctx.fill();

                    // Mắt cá
                    ctx.fillStyle = '#fff';
                    ctx.beginPath();
                    ctx.arc(10, -2, 2.5, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#000';
                    ctx.beginPath();
                    ctx.arc(11, -2, 1, 0, Math.PI * 2);
                    ctx.fill();

                    // Tên trên thân cá
                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 11px Segoe UI';
                    ctx.textAlign = 'center';
                    ctx.shadowColor = 'rgba(0,0,0,0.9)';
                    ctx.shadowBlur = 5;
                    ctx.fillText(this.name, 0, -18);

                    ctx.restore();
                }}
            }}

            let poolFishes = [];
            namesList.forEach(name => {{
                poolFishes.push(new Fish(name));
            }});

            function drawScene() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Bờ đất và thảm cỏ phía trên chân thực
                ctx.fillStyle = '#3d2817';
                ctx.fillRect(0, 0, canvas.width, 100);
                ctx.fillStyle = '#27ae60';
                ctx.fillRect(0, 95, canvas.width, 10);

                // Bảng tên gỗ góc trái
                ctx.fillStyle = '#d35400';
                ctx.fillRect(25, 15, 130, 38);
                ctx.strokeStyle = '#f39c12';
                ctx.lineWidth = 2;
                ctx.strokeRect(25, 15, 130, 38);
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 12px Segoe UI';
                ctx.textAlign = 'center';
                ctx.fillText("📜 HỒ CÂU TÊN", 90, 38);

                // Nhân vật người câu cá chân thực góc phải
                ctx.fillStyle = '#2980b9';
                ctx.fillRect(360, 55, 26, 40); // Thân áo
                ctx.fillStyle = '#f5b041';
                ctx.beginPath();
                ctx.arc(373, 43, 10, 0, Math.PI * 2); // Đầu
                ctx.fill();
                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(373, 38, 12, Math.PI, 2 * Math.PI); // Nón
                ctx.fill();

                // Cần câu carbon linh hoạt
                ctx.strokeStyle = '#7f8c8d';
                ctx.lineWidth = 3.5;
                ctx.beginPath();
                ctx.moveTo(373, 55);
                ctx.lineTo(280, 25);
                ctx.stroke();

                // Dây câu kéo thả mềm mại
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.2;
                ctx.beginPath();
                ctx.moveTo(280, 25);
                ctx.lineTo(280, hookY);
                ctx.stroke();

                // Lưỡi câu vàng kim
                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(280, hookY, 4.5, 0, Math.PI * 2);
                ctx.fill();

                // Vẽ đàn cá bơi lội
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
                        statusText.innerHTML = "⏳ Mồi đã chìm xuống, đang chờ cá bơi tới...";
                        
                        targetFish = poolFishes[Math.floor(Math.random() * poolFishes.length)];
                        targetFish.isTarget = true;
                        currentWinner = targetFish.name;

                        setTimeout(() => {{
                            if (gameState === 'WAITING') {{
                                gameState = 'BITING';
                                statusText.innerHTML = '🔥 CÁ CẮN CÂU: <b>' + currentWinner + '</b> - <span style="color:#00ff99;">KÉO LÊN NGAY!</span>';
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
                        actionBtn.innerHTML = "🎉 ĐÃ CÂU ĐƯỢC CÁ!";
                        actionBtn.disabled = true;
                        
                        confetti({{ particleCount: 130, spread: 80, origin: {{ y: 0.6 }} }});
                        statusText.innerHTML = '<span class="winner-display">🎉 Trúng giải: ' + currentWinner + '! Hãy chọn Xóa hoặc Giữ lại ở bảng ngoài.</span>';
                        
                        if (targetFish) {{
                            targetFish.isTarget = false;
                            targetFish.x = -40;
                        }}
                        
                        // Truyền kết quả ra ngoài Streamlit an toàn
                        const url = new URL(window.location.href);
                        url.searchParams.set('winner', currentWinner);
                        window.history.replaceState({{}}, '', url);

                        setTimeout(() => {{
                            window.parent.location.reload();
                        }}, 1500);
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
    """

    components.html(game_html, height=520)

    # Đọc tham số từ URL khi trò chơi bắt được cá thành công
    query_params = st.query_params
    if "winner" in query_params and not st.session_state.pending_winner:
        w_name = query_params["winner"]
        if w_name not
