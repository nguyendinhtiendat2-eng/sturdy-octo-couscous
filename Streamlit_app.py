import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FinPulse - Quản Lý Tài Chính",
    page_icon="💰",
    layout="wide"
)

# Khởi tạo dữ liệu mẫu nếu chưa có trong session_state
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {"ID": 1, "Ngay": "2026-10-01", "Loai": "Thu nhập", "Danh_Muc": "Lương", "Mo_Ta": "Lương tháng 10", "So_Tien": 15000000},
        {"ID": 2, "Ngay": "2026-10-02", "Loai": "Chi tiêu", "Danh_Muc": "Nhà ở", "Mo_Ta": "Tiền thuê nhà", "So_Tien": 4500000},
        {"ID": 3, "Ngay": "2026-10-05", "Loai": "Chi tiêu", "Danh_Muc": "Ăn uống", "Mo_Ta": "Đi siêu thị", "So_Tien": 1200000},
        {"ID": 4, "Ngay": "2026-10-06", "Loai": "Chi tiêu", "Danh_Muc": "Di chuyển", "Mo_Ta": "Đổ xăng", "So_Tien": 200000},
    ])

# Hàm định dạng tiền tệ VNĐ
def format_vnd(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")

# --- HEADER ---
st.title("💰 FinPulse - Quản Lý Tài Chính Cá Nhân")
st.caption("Ứng dụng theo dõi thu chi và phân tích ngân sách cá nhân đơn giản với Streamlit")
st.divider()

# --- CỘT BÊN CÁNH (SIDEBAR) - THÊM GIAO DỊCH ---
st.sidebar.header("➕ Thêm Giao Dịch Mới")

type_option = st.sidebar.radio("Loại giao dịch:", ["Chi tiêu", "Thu nhập"])

if type_option == "Thu nhập":
    categories = ["Lương", "Thưởng", "Đầu tư", "Khác"]
else:
    categories = ["Ăn uống", "Nhà ở", "Di chuyển", "Mua sắm", "Giải trí", "Khác"]

category = st.sidebar.selectbox("Danh mục:", categories)
description = st.sidebar.text_input("Mô tả:", placeholder="Ví dụ: Ăn trưa, Tiền thưởng...")
amount = st.sidebar.number_input("Số tiền (VNĐ):", min_value=1000, step=10000, value=50000)
tx_date = st.sidebar.date_input("Ngày giao dịch:", datetime.now())

if st.sidebar.button("Thêm Giao Dịch", type="primary", use_container_width=True):
    if description.strip() == "":
        st.sidebar.error("Vui lòng nhập mô tả giao dịch!")
    else:
        new_tx = {
            "ID": int(datetime.now().timestamp()),
            "Ngay": tx_date.strftime("%Y-%m-%d"),
            "Loai": type_option,
            "Danh_Muc": category,
            "Mo_Ta": description,
            "So_Tien": amount
        }
        st.session_state.transactions = pd.concat(
            [pd.DataFrame([new_tx]), st.session_state.transactions],
            ignore_index=True
        )
        st.sidebar.success("Đã thêm giao dịch thành công!")
        st.rerun()

# Button Đặt lại dữ liệu trên Sidebar
if st.sidebar.button("🔄 Đặt lại dữ liệu mẫu", use_container_width=True):
    st.session_state.pop("transactions", None)
    st.rerun()

# --- PHẦN CHÍNH (MAIN DASHBOARD) ---
df = st.session_state.transactions

# 1. Thống kê tổng quan (Metrics)
total_income = df[df["Loai"] == "Thu nhập"]["So_Tien"].sum()
total_expense = df[df["Loai"] == "Chi tiêu"]["So_Tien"].sum()
balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("💵 Tổng Số Dư", format_vnd(balance), delta_color="normal")
col2.metric("📈 Tổng Thu Nhập", format_vnd(total_income))
col3.metric("📉 Tổng Chi Tiêu", format_vnd(total_expense))

st.divider()

# 2. Biểu đồ trực quan
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Cơ cấu chi tiêu theo Danh mục")
    df_expense = df[df["Loai"] == "Chi tiêu"]
    if not df_expense.empty:
        fig_pie = px.pie(
            df_expense,
            names="Danh_Muc",
            values="So_Tien",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu chi tiêu để hiển thị biểu đồ.")

with col_chart2:
    st.subheader("⚖️ So sánh Thu nhập vs Chi tiêu")
    df_summary = pd.DataFrame({
        "Loai": ["Thu nhập", "Chi tiêu"],
        "Tong": [total_income, total_expense]
    })
    fig_bar = px.bar(
        df_summary,
        x="Loai",
        y="Tong",
        color="Loai",
        color_discrete_map={"Thu nhập": "#10b981", "Chi tiêu": "#f43f5e"},
        labels={"Tong": "Số tiền (VNĐ)", "Loai": "Loại"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# 3. Danh sách & Lịch sử giao dịch
st.subheader("📋 Lịch Sử Giao Dịch")

# Bộ lọc
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    search_term = st.text_input("🔍 Tìm kiếm theo mô tả hoặc danh mục:")
with filter_col2:
    filter_type = st.selectbox("Lọc theo loại:", ["Tất cả", "Thu nhập", "Chi tiêu"])

# Lọc dữ liệu
filtered_df = df.copy()
if filter_type != "Tất cả":
    filtered_df = filtered_df[filtered_df["Loai"] == filter_type]

if search_term:
    filtered_df = filtered_df[
        filtered_df["Mo_Ta"].str.contains(search_term, case=False, na=False) |
        filtered_df["Danh_Muc"].str.contains(search_term, case=False, na=False)
    ]

# Định dạng hiển thị bảng
display_df = filtered_df.copy()
display_df["So_Tien"] = display_df["So_Tien"].apply(format_vnd)
display_df = display_df.rename(columns={
    "Ngay": "Ngày",
    "Loai": "Loại",
    "Danh_Muc": "Danh Mục",
    "Mo_Ta": "Mô Tả",
    "So_Tien": "Số Tiền"
})

st.dataframe(
    display_df[["Ngày", "Loại", "Danh Mục", "Mô Tả", "Số Tiền"]],
    use_container_width=True,
    hide_index=True
         )
