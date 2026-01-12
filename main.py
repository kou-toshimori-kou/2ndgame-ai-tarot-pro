import streamlit as st
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- ページ設定 ---
st.set_page_config(
    page_title="Toshimori Tarot",
    page_icon="🃏",
    layout="centered"
)

# --- Gmail通知を送る関数 ---
def send_gmail_notify(user_name, user_input, card_name, position, advice):
    try:
        # Secretsから設定を読み込む
        gmail_user = st.secrets["GMAIL_USER"]
        gmail_password = st.secrets["GMAIL_PASSWORD"]
        
        # 送り先（自分自身に送る）
        to_email = gmail_user
        
        # メールの件名と本文
        subject = f"【タロット相談】{user_name}様からの依頼"
        body = f"""
        利守航 様
        
        新しいタロット相談が届きました。
        
        ■相談者
        {user_name} 様
        
        ■相談内容
        {user_input}
        
        ■結果
        カード: {card_name} ({position})
        
        ■アドバイス内容
        {advice}
        
        -------------------------
        Toshimori Tarot App
        """
        
        # メール作成
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Gmailサーバーに接続して送信
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        
    except Exception as e:
        print(f"メール送信エラー: {e}")

# --- タイトル ---
# ★ここで改行（\n）を入れています
st.title("🃏 タロット占いの館\n「タロットシモリ」")
st.markdown("心を落ち着けてボタンを押してください。\n利守航からの運命のメッセージが届きます。")

# --- 画像リスト ---
TAROT_IMAGES = {
    "0. 愚者": "https://www.sacred-texts.com/tarot/pkt/img/ar00.jpg",
    "1. 魔術師": "https://www.sacred-texts.com/tarot/pkt/img/ar01.jpg",
    "2. 女教皇": "https://www.sacred-texts.com/tarot/pkt/img/ar02.jpg",
    "3. 女帝": "https://www.sacred-texts.com/tarot/pkt/img/ar03.jpg",
    "4. 皇帝": "https://www.sacred-texts.com/tarot/pkt/img/ar04.jpg",
    "5. 法王": "
