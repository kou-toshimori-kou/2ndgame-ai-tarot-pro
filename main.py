import streamlit as st
import random
import time

# --- ページ設定（アプリのタブ名やアイコン） ---
st.set_page_config(
    page_title="Gemini Tarot Pro",
    page_icon="🔮",
    layout="centered"
)

# --- タイトルと説明 ---
st.title("🔮 AIタロット占い Pro")
st.markdown("""
ようこそ。ここは星の巡りとAIの叡智が交わる場所です。
あなたの悩みを入力し、カードを引いてください。
""")

# --- 大アルカナ22枚のリスト ---
TAROT_CARDS = [
    "0. 愚者", "1. 魔術師", "2. 女教皇", "3. 女帝", "4. 皇帝", "5. 法王",
    "6. 恋人", "7. 戦車", "8. 力", "9. 隠者", "10. 運命の輪", "11. 正義",
    "12. 吊るされた男", "13. 死神", "14. 節制", "15. 悪魔", "16. 塔",
    "17. 星", "18. 月", "19. 太陽", "20. 審判", "21. 世界"
]

# --- ユーザー入力エリア ---
with st.form(key='consultation_form'):
    user_input = st.text_area("相談内容を入力してください（心の迷い、知りたいこと）", height=100)
    submit_button = st.form_submit_button(label='運命のカードを引く')

# --- 占いの実行処理 ---
if submit_button:
    if not user_input:
        st.warning("まずは相談内容を教えてください。")
    else:
        # 演出：カードをシャッフルしているような待機時間
        with st.spinner('星の配置を読み解いています...'):
            time.sleep(2)  # 2秒間の演出
            
            # カードと正位置・逆位置をランダム決定
            card = random.choice(TAROT_CARDS)
            position = random.choice(["正位置", "逆位置"])
            
            # --- 結果表示エリア ---
            st.divider()
            st.subheader(f"🎴 出たカード: {card} ({position})")
            
            # ここに将来、Gemini ProのAPIからの回答が入ります
            # 今はプレースホルダー（仮の表示）を表示
            st.success("【システム準備完了】ここにGemini Proによる高度な鑑定結果が表示されます。")
            
            # デバッグ用：AIに送る予定の「プロンプト」を表示（開発者向け確認）
            st.code(f"""
            あなたはベテランの占い師です。以下の情報で占ってください。
            相談内容: {user_input}
            引いたカード: {card}
            位置: {position}
            """, language="text")
