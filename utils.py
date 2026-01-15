import streamlit as st

def navbar():
    """
    Navbar แบบ Native Streamlit (Top Bar)
    Layout: [ ชื่อ App ] --ว่าง-- [Dashboard] [Sector] [News] [AI Leaderboard]
    """
    # CSS ซ่อน Sidebar และตกแต่ง Navbar
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="collapsedControl"] { display: none; }
        div[data-testid="stPageLink-NavLink"] { justify-content: center; }
        
        /* ปรับแต่งชื่อ App ใน Navbar */
        .nav-app-name {
            font-weight: 700;
            font-size: 38px;
            color: #333333;
            display: flex;
            align-items: center;
            height: 100%;
            font-family: 'Inter', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        # 🔥 UPDATE: เพิ่ม col4 และปรับตัวเลขสัดส่วนนิดหน่อยให้พอดี
        # เดิม: [2.5, 0.5, 1, 1, 1]
        # ใหม่: [2.2, 0.2, 0.9, 0.9, 0.9, 1.1] (ลดช่องว่างลง เพื่อยัดปุ่มที่ 4 ใส่เข้าไป)
        col_brand, col_space, col1, col2, col3, col4 = st.columns([2.2, 0.2, 0.9, 0.9, 0.9, 1.1]) 

        with col_brand:
            st.markdown('<div class="nav-app-name">MarketMind</div>', unsafe_allow_html=True)

        # ช่องว่าง (col_space) ปล่อยเบลอไว้

        with col1:
            st.page_link("Home.py", label="Dashboard", icon="🏠", use_container_width=True)
        
        with col2:
            st.page_link("pages/2_Sector_Detail.py", label="Sector Dive", icon="🔍", use_container_width=True)
        
        with col3:
            st.page_link("pages/3_News_Center.py", label="News Center", icon="📰", use_container_width=True)
            
        # ✅ NEW BUTTON: เพิ่มปุ่มที่ 4 ตรงนี้
        with col4:
            st.page_link("pages/4_LLM_Benchmark.py", label="LLM Benchmark", icon="🏆", use_container_width=True)
            
        st.divider()

# --- ฟังก์ชันคำนวณเฉดสี (Gradient) ---
def get_sentiment_color(score):
    """
    แปลงคะแนน -10 ถึง 10 ให้เป็นรหัสสี Hex:
    -10 (แดงจัด) -> 0 (เหลือง) -> 10 (เขียวจัด)
    """
    RED = (255, 75, 75)     # #FF4B4B
    YELLOW = (250, 202, 43) # #FACA2B
    GREEN = (9, 171, 59)    # #09AB3B

    def interpolate(start, end, factor):
        return int(start + (end - start) * factor)

    if score < 0:
        factor = (score + 10) / 10.0
        factor = max(0.0, min(1.0, factor)) 
        
        r = interpolate(RED[0], YELLOW[0], factor)
        g = interpolate(RED[1], YELLOW[1], factor)
        b = interpolate(RED[2], YELLOW[2], factor)
    else:
        factor = score / 10.0
        factor = max(0.0, min(1.0, factor))
        
        r = interpolate(YELLOW[0], GREEN[0], factor)
        g = interpolate(YELLOW[1], GREEN[1], factor)
        b = interpolate(YELLOW[2], GREEN[2], factor)
        
    return f"#{r:02x}{g:02x}{b:02x}"