import streamlit as st
import random
import time
import google.generativeai as genai

# --- ページ設定 ---
st.set_page_config(
    page_title="Gemini Tarot Pro",
    page_icon="🔮",
    layout="centered"
)

# --- APIキーの設定 ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("APIキーが設定されていません。")

# --- AIモデルの準備（ここを安定版の gemini-pro にしました） ---
model = genai.GenerativeModel('gemini-pro')

# --- タイトルと説明 ---
st.title("🔮 AIタロット占い Pro")
st.markdown("""
星の巡りとAIの叡智が、あなたの迷いを照らします。
心を落ち着けて、相談内容を入力してください。
""")

# --- 大アルカナ22枚のリスト ---
TAROT_CARDS = [
    "0. 愚者", "1. 魔術師", "2. 女教皇", "3. 女帝", "4. 皇帝", "5. 法王",
    "6. 恋人", "7. 戦車", "8. 力", "9. 隠者", "10. 運命の輪", "11. 正義",
    "12. 吊るされた男", "13. 死神", "14. 節制", "15. 悪魔", "16. 塔",
    "17. 星", "18. 月", "19. 太陽", "20. 審判", "21. 世界"
]

# --- ユーザー入力 ---
with st.form(key='consultation_form'):
    user_input = st.text_area("相談内容（例：転職すべきか迷っています...）", height=100)
    submit_button = st.form_submit_button(label='運命のカードを引く')

# --- 占いの実行 ---
if submit_button:
    if not user_input:
        st.warning("相談内容を入力してください。")
    else:
        # カード抽選
        card = random.choice(TAROT_CARDS)
        position = random.choice(["正位置", "逆位置"])
        
        st.divider()
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image("https://placehold.co/200x350/222/FFF?text=Tarot", caption=f"{card}")
        
        with col2:
            st.subheader(f"🎴 結果: {card} ({position})")
            
            # AIへの指示
            prompt = f"""
            あなたは神秘的で思慮深い、ベテランのタロット占い師です。
            以下の相談者に対して、引いたカードの意味を元に、具体的で前向きなアドバイスをしてください。
            
            相談内容: {user_input}
            引いたカード: {card}
            位置: {position}
            
            回答の構成:
            1. **カードの象徴**: このカードが持つ本来の意味（簡潔に）
            2. **現状の読み解き**: 相談内容とカードを照らし合わせた現状分析
            3. **未来への導き**: 具体的な行動アドバイス（優しく、背中を押すように）
            """
            
            # AI生成中...
            with st.spinner('星の声を聴いています...（AI生成中）'):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
