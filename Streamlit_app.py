import random
import streamlit as st

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

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "current_winner" not in st.session_state:
    st.session_state.current_winner = None

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
            <div class="title-neon">🎣 HỒ CÂU CHỌN TÊN - SIÊU MƯỢT 🌟</div>
            <div class="subtitle">TRÒ CHƠI CÂU CÁ CHỌN NGƯỜI NGẪU NHIÊN</div>
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
    # ----------------- GIAO DIỆN TRÒ CHƠI CÂU CÁ TRỰC QUAN -----------------
    st.markdown("### 🎣 Hồ Câu May Mắn - Trực Quan Sống Động")

    # Hiển thị khu vực hồ nước phong cách hoạt hình
    st.markdown(
        """
        <div style="background: linear-gradient(to bottom, #1e3c72, #2a5298); padding: 25px; border-radius: 15px; text-align: center; border: 2px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
            <h2 style="color: #87CEEB; margin-top: 0;">🌊 Hồ Nước Xanh Mát & Đàn Cá Bơi Lội 🐟</h2>
            <p style="color: #fff; font-size: 16px;">Nhấn nút <b>"Thả Cần Câu"</b> để thu hút một chú cá mang tên ứng viên bơi đến cắn câu!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Nếu vừa câu trúng cá, hiển thị ngay bảng quyết định Xóa hoặc Giữ lại
    if st.session_state.current_winner:
        winner = st.session_state.current_winner
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #f39c12, #d35400); padding: 22px; border-radius: 12px; text-align: center; margin-bottom: 20px; border: 2px solid #f1c40f; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
                <h2 style="margin: 0; color: #fff;">🎉 CÁ CẮN CÂU! NGƯỜI TRÚNG GIẢI LÀ: <span style="color: #ffeaa7; font-size: 32px;">{winner}</span></h2>
                <p style="margin: 8px 0 0 0; color: #fff; font-size: 16px;">Bạn muốn xử lý tên chú cá này như thế nào cho các lượt tiếp theo?</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button(
                "🗑️ XÓA TÊN NÀY KHỎI BẢNG",
                type="primary",
                use_container_width=True,
            ):
                if winner in st.session_state.names_list:
                    st.session_state.names_list.remove(winner)
                st.session_state.history.append(winner)
                st.session_state.current_winner = None
                st.success(
                    f"Đã xóa **{winner}** khỏi bảng và lưu vào lịch sử!"
                )
                st.rerun()
        with col_btn2:
            if st.button(
                "🛡️ GIỮ LẠI TÊN TRONG BẢNG", use_container_width=True
            ):
                st.session_state.history.append(winner)
                st.session_state.current_winner = None
                st.success(
                    f"Đã giữ lại **{winner}** trong bảng và lưu vào lịch sử!"
                )
                st.rerun()
    else:
        # Nút điều khiển thả cần câu
        col_action1, col_action2, col_action3 = st.columns([1, 2, 1])
        with col_action2:
            if not st.session_state.names_list:
                st.warning(
                    "⚠️ Bảng tên hiện đang trống! Vui lòng quay lại menu để thêm tên."
                )
            else:
                if st.button(
                    "🎣 THẢ CẦN CÂU NGAY",
                    type="primary",
                    use_container_width=True,
                ):
                    if st.session_state.names_list:
                        chosen_name = random.choice(
                            st.session_state.names_list
                        )
                        st.session_state.current_winner = chosen_name
                        st.balloons()  # Hiệu ứng pháo hoa bóng bay chúc mừng
                        st.rerun()

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
            st.session_state.current_winner = None
            st.rerun()

        manual_winner = st.selectbox(
            "Chọn thủ công phòng hờ:", st.session_state.names_list
        )
        if st.button("🎉 Lưu kết quả thủ công"):
            if manual_winner:
                st.session_state.current_winner = manual_winner
                st.rerun()
      
