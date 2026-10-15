import random
import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Game Câu Cá Chọn Tên", page_icon="🎣", layout="wide"
)

# Khởi tạo session state cho danh sách tên và lịch sử
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

# Sidebar: Cài đặt và Quản lý danh sách tên
with st.sidebar:
    st.header("⚙️ Cài đặt Game Câu Cá")

    st.subheader("📝 Danh sách người chơi")
    names_input = st.text_area(
        "Nhập tên (mỗi tên một dòng):",
        value="\n".join(st.session_state.names_list),
        height=150,
    )

    if st.button("💾 Cập nhật danh sách", use_container_width=True):
        new_names = [
            name.strip() for name in names_input.split("\n") if name.strip()
        ]
        if new_names:
            st.session_state.names_list = new_names
            st.success(
                f"Đã cập nhật thành công {len(new_names)} người chơi! 🎉"
            )
            st.rerun()
        else:
            st.error("Danh sách không được để trống!")

    st.session_state.remove_after_pick = st.checkbox(
        "Loại bỏ tên sau khi câu được",
        value=st.session_state.remove_after_pick,
        help="Nếu chọn, tên đã trúng sẽ bị xóa khỏi danh sách cho các lượt tiếp theo.",
    )

    if st.button("🗑️ Xóa lịch sử câu", use_container_width=True):
        st.session_state.history = []
        st.success("Đã xóa lịch sử!")
        st.rerun()

    st.markdown("---")
    st.markdown("### 🚀 Hướng dẫn lên GitHub & Streamlit")
    with st.expander("Xem chi tiết"):
        st.markdown(
            """
        1. **Tạo file `app.py`**: Dán đoạn code này vào.
        2. **Tạo file `requirements.txt`**:
           ```text
           streamlit
           ```
        3. **Đẩy lên GitHub**: Tạo repository mới trên GitHub và push 2 file `app.py` và `requirements.txt` lên.
        4. **Deploy trên Streamlit Cloud**: Truy cập [share.streamlit.io](https://share.streamlit.io), chọn Repo của bạn và bấm **Deploy**.
        """
        )

# Giao diện chính
st.title("🎣 Game Câu Cá Chọn Tên (Streamlit + GitHub)")
st.markdown(
    "Thả cần xuống hồ, chờ cá cắn câu và xem thần may mắn gọi tên ai nhé!"
)

# Chuẩn bị dữ liệu tên truyền qua HTML/JS dưới dạng chuỗi phân tách bởi dấu phẩy
current_names_json = st.session_state.names_list

if not current_names_json:
    st.warning(
        "⚠️ Danh sách tên đang trống! Hãy thêm tên ở thanh bên trái (Sidebar) để bắt đầu câu cá."
    )
else:
    # Mã nguồn HTML, CSS, JavaScript cho Game Câu Cá + Hiệu ứng Pháo giấy (Confetti)
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
                background: linear-gradient(to bottom, #87CEEB 0%, #4682B4 40%, #104E8B 100%);
                cursor: pointer;
            }}
            .control-panel {{
                padding: 15px;
                background: rgba(0, 0, 0, 0.4);
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            }}
            .btn {{
                background: #ff4b4b;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                box-shadow: 0 4px 10px rgba(255, 75, 75, 0.4);
            }}
            .btn:hover {{
                background: #ff2b2b;
                transform: translateY(-2px);
                box-shadow: 0 6px 15px rgba(255, 75, 75, 0.6);
            }}
            .btn:disabled {{
                background: #555;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }}
            .status-text {{
                font-size: 18px;
                font-weight: 600;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
            }}
            .winner-display {{
                font-size: 20px;
                color: #FFD700;
                font-weight: bold;
                text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
            }}
        </style>
    </head>
    <body>

        <div class="game-container">
            <canvas id="gameCanvas" width="800" height="450"></canvas>
            <div class="control-panel">
                <button id="actionBtn" class="btn" onclick="handleAction()">🎣 Thả Cần Câu</button>
                <div class="status-text" id="statusText">Trạng thái: Sẵn sàng câu cá!</div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const actionBtn = document.getElementById('actionBtn');
            const statusText = document.getElementById('statusText');

            let names = {current_names_json};
            let gameState = 'IDLE'; // IDLE, CASTING, WAITING, BITING, HOOKED, REELING
            let hookY = -50;
            let targetHookY = 150;
            let fishPool = [];
            let currentWinner = "";
            let biteTimer = null;

            // Khởi tạo đàn cá bơi lội
            class Fish {{
                constructor() {{
                    this.reset();
                }}
                reset() {{
                    this.x = Math.random() * canvas.width;
                    this.y = 200 + Math.random() * 200;
                    this.speed = (Math.random() * 1.5 + 0.8) * (Math.random() < 0.5 ? 1 : -1);
                    this.size = 25 + Math.random() * 15;
                    this.color = ['#ff7675', '#74b9ff', '#55efc4', '#ffeaa7', '#a29bfe'][Math.floor(Math.random() * 5)];
                }}
                update() {{
                    this.x += this.speed;
                    if (this.x > canvas.width + 50) this.x = -50;
                    if (this.x < -50) this.x = canvas.width + 50;
                }}
                draw() {{
                    ctx.save();
                    ctx.translate(this.x, this.y);
                    if (this.speed < 0) ctx.scale(-1, 1);
                    
                    // Thân cá
                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    ctx.ellipse(0, 0, this.size, this.size / 2, 0, 0, Math.PI * 2);
                    ctx.fill();

                    // Đuôi cá
                    ctx.beginPath();
                    ctx.moveTo(-this.size, 0);
                    ctx.lineTo(-this.size - 12, -10);
                    ctx.lineTo(-this.size - 12, 10);
                    ctx.closePath();
                    ctx.fill();
                    
                    ctx.restore();
                }}
            }}

            for (let i = 0; i < 7; i++) {{
                fishPool.push(new Fish());
            }}

            function drawBackground() {{
                // Vẽ mặt nước
                ctx.fillStyle = "rgba(255, 255, 255, 0.15)";
                ctx.fillRect(0, 0, canvas.width, 100);

                // Gợn sóng mặt nước
                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
                ctx.lineWidth = 2;
                ctx.beginPath();
                for (let i = 0; i < canvas.width; i += 40) {{
                    ctx.moveTo(i, 100);
                    ctx.quadraticCurveTo(i + 20, 95, i + 40, 100);
                }}
                ctx.stroke();
            }}

            function drawHook() {{
                if (gameState !== 'IDLE') {{
                    // Dây câu từ cần cẩu góc trên phải
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(canvas.width - 100, 0);
                    ctx.lineTo(canvas.width - 100, hookY);
                    ctx.stroke();

                    // Lưỡi câu
                    ctx.fillStyle = '#f1c40f';
                    ctx.beginPath();
                    ctx.arc(canvas.width - 100, hookY, 6, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}

            function gameLoop() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                drawBackground();

                // Cập nhật và vẽ cá
                fishPool.forEach(fish => {{
                    fish.update();
                    fish.draw();
                }});

                drawHook();

                // Xử lý chuyển động lưỡi câu
                if (gameState === 'CASTING') {{
                    hookY += 4;
                    if (hookY >= targetHookY) {{
                        hookY = targetHookY;
                        gameState = 'WAITING';
                        statusText.innerHTML = "⏳ Đang chờ cá cắn câu...";
                        
                        // Đợi ngẫu nhiên từ 1.5s đến 3s để cá cắn
                        let waitTime = 1500 + Math.random() * 1500;
                        biteTimer = setTimeout(() => {{
                            if (names.length === 0) {{
                                alert("Hết tên trong danh sách!");
                                resetGame();
                                return;
                            }}
                            gameState = 'BITING';
                            statusText.innerHTML = "🔥 CÁ CẮN CÂU RỒI! BẤM 'KÉO LÊN' NHANH!";
                            actionBtn.innerHTML = "🎣 KÉO CÁ LÊN NGAY!";
                            actionBtn.style.background = "#2ecc71";
                        }}, waitTime);
                    }}
                }} else if (gameState === 'REELING') {{
                    hookY -= 8;
                    if (hookY <= -50) {{
                        hookY = -50;
                        gameState = 'IDLE';
                        actionBtn.innerHTML = "🎣 Thả Cần Câu";
                        actionBtn.disabled = false;
                        
                        // Hiệu ứng pháo giấy ăn mừng
                        confetti({{
                            particleCount: 100,
                            spread: 70,
                            origin: {{ y: 0.6 }}
                        }});

                        statusText.innerHTML = `<span class="winner-display">🎉 Chúc mừng: ${currentWinner} đã trúng giải!</span>`;
                        
                        // Gửi kết quả về Streamlit thông qua URL query param hoặc console log
                        window.parent.postMessage({type: 'streamlit:setComponentValue', value: currentWinner}, '*');
                    }}
                }}

                requestAnimationFrame(gameLoop);
            }}

            function handleAction() {{
                if (names.length === 0) {{
                    alert("Danh sách người chơi đang trống!");
                    return;
                }}

                if (gameState === 'IDLE') {{
                    // Bắt đầu thả cần
                    gameState = 'CASTING';
                    actionBtn.innerHTML = "Đang thả cần...";
                    actionBtn.disabled = true;
                    statusText.innerHTML = "🎣 Đang thả mồi xuống hồ...";
                }} else if (gameState === 'WAITING') {{
                    // Kéo lên sớm -> hụt
                    clearTimeout(biteTimer);
                    gameState = 'REELING';
                    currentWinner = "Hụt mất rồi (Kéo sớm quá)!";
                    statusText.innerHTML = "❌ Kéo quá sớm, cá chưa kịp cắn!";
                }} else if (gameState === 'BITING') {{
                    // Bấm đúng lúc cá cắn -> Chọn ngẫu nhiên 1 người
                    clearTimeout(biteTimer);
                    const randomIndex = Math.floor(Math.random() * names.length);
                    currentWinner = names[randomIndex];
                    
                    gameState = 'REELING';
                    actionBtn.innerHTML = "Đang kéo lên...";
                    actionBtn.style.background = "#ff4b4b";
                }}
            }}

            function resetGame() {{
                gameState = 'IDLE';
                hookY = -50;
                actionBtn.innerHTML = "🎣 Thả Cần Câu";
                actionBtn.disabled = false;
                statusText.innerHTML = "Trạng thái: Sẵn sàng câu cá!";
            }}

            gameLoop();
        </script>
    </body>
    </html>
    """

    # Hiển thị component game HTML5
    winner_name = components.html(game_html, height=520)

    # Xử lý kết quả trả về từ game khi có người trúng giải
    # (Streamlit component nhận diện tương tác qua session state hoặc thông báo)
    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📜 Lịch sử câu cá các lượt trước")
        if st.session_state.history:
            for idx, item in enumerate(
                reversed(st.session_state.history), 1
            ):
                st.write(
                    f"**{idx}.** Trúng tên: <span style='color: #FFD700; font-weight: bold;'>{item}</span>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("Chưa có lượt câu nào được ghi nhận.")

    with col2:
        st.subheader("🎯 Thống kê nhanh")
        st.metric(
            label="Tổng số ứng viên", value=len(st.session_state.names_list)
        )
        st.metric(label="Tổng số lượt câu", value=len(st.session_state.history))

    # Nút mô phỏng nhận kết quả trực tiếp nếu muốn test nhanh thủ công ngoài canvas
    with st.expander("🛠️ Bảng điều khiển thủ công phòng hờ"):
        manual_winner = st.selectbox(
            "Chọn nhanh người chiến thắng:", st.session_state.names_list
        )
        if st.button("🎉 Xác nhận người thắng thủ công"):
            if (
                manual_winner
                and manual_winner not in st.session_state.history
            ):
                st.session_state.history.append(manual_winner)
                if st.session_state.remove_after_pick:
                    st.session_state.names_list.remove(manual_winner)
                st.success(
                    f"Đã lưu kết quả thủ công cho: **{manual_winner}**!"
                )
                st.rerun()
          
