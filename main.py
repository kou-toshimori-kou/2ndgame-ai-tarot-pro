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
    "5. 法王": "https://www.sacred-texts.com/tarot/pkt/img/ar05.jpg",
    "6. 恋人": "https://www.sacred-texts.com/tarot/pkt/img/ar06.jpg",
    "7. 戦車": "https://www.sacred-texts.com/tarot/pkt/img/ar07.jpg",
    "8. 力": "https://www.sacred-texts.com/tarot/pkt/img/ar08.jpg",
    "9. 隠者": "https://www.sacred-texts.com/tarot/pkt/img/ar09.jpg",
    "10. 運命の輪": "https://www.sacred-texts.com/tarot/pkt/img/ar10.jpg",
    "11. 正義": "https://www.sacred-texts.com/tarot/pkt/img/ar11.jpg",
    "12. 吊るされた男": "https://www.sacred-texts.com/tarot/pkt/img/ar12.jpg",
    "13. 死神": "https://www.sacred-texts.com/tarot/pkt/img/ar13.jpg",
    "14. 節制": "https://www.sacred-texts.com/tarot/pkt/img/ar14.jpg",
    "15. 悪魔": "https://www.sacred-texts.com/tarot/pkt/img/ar15.jpg",
    "16. 塔": "https://www.sacred-texts.com/tarot/pkt/img/ar16.jpg",
    "17. 星": "https://www.sacred-texts.com/tarot/pkt/img/ar17.jpg",
    "18. 月": "https://www.sacred-texts.com/tarot/pkt/img/ar18.jpg",
    "19. 太陽": "https://www.sacred-texts.com/tarot/pkt/img/ar19.jpg",
    "20. 審判": "https://www.sacred-texts.com/tarot/pkt/img/ar20.jpg",
    "21. 世界": "https://www.sacred-texts.com/tarot/pkt/img/ar21.jpg"
}

# --- データリスト（利守航スペシャル） ---
TAROT_DATA = {
    "0. 愚者": "【意味】始まり、自由、純粋、冒険\n\n【アドバイス】利守航と一緒に、思い切って新しい旅に出かけましょう！",
    "1. 魔術師": "【意味】創造、自信、スキルの発揮\n\n【アドバイス】何かを始めるチャンスです。利守航のアイデアを借りるとうまくいきます。",
    "2. 女教皇": "【意味】知性、直感、静寂\n\n【アドバイス】焦りは禁物です。利守航と静かに語り合う時間を持つと答えが見えます。",
    "3. 女帝": "【意味】豊かさ、母性、繁栄\n\n【アドバイス】利守航に日頃の感謝を伝えてみてください。素晴らしいお返しがあるかも",
    "4. 皇帝": "【意味】責任、安定、リーダーシップ\n\n【アドバイス】迷ったら利守航の決断に従ってみましょう。頼りになるはずです。",
    "5. 法王": "【意味】慈悲、信頼、伝統\n\n【アドバイス】困った時は利守航に助言を求めると、事態は好転します。",
    "6. 恋人": "【意味】選択、愛、調和\n\n【アドバイス】心がワクワクする方を選びましょう。利守航との相性も最高です！",
    "7. 戦車": "【意味】勝利、前進、行動力\n\n【アドバイス】利守航と共に突き進めば、どんな壁も突破できます。",
    "8. 力": "【意味】忍耐、勇気、優しさ\n\n【アドバイス】力ずくではなく、利守航のような優しさと粘り強さで接しましょう。",
    "9. 隠者": "【意味】内省、真理の探究\n\n【アドバイス】一人で悩まず、利守航と深い話をしてみるのも良いでしょう。",
    "10. 運命の輪": "【意味】チャンス、一時的な幸運\n\n【アドバイス】流れに乗る時です。利守航と共に過ごすことで運命を変えます。",
    "11. 正義": "【意味】公平、誠実、バランス\n\n【アドバイス】利守航は公平に見ています。誠実な態度でいれば彼は評価しますよ。",
    "12. 吊るされた男": "【意味】試練、忍耐、視点を変える\n\n【アドバイス】今は動けなくても大丈夫。利守航も浪人を経験しています。",
    "13. 死神": "【意味】終わりと始まり、変化\n\n【アドバイス】古い習慣は捨てましょう。利守航と共に、新しい自分に生まれ変わる時です。",
    "14. 節制": "【意味】調和、バランス、自制\n\n【アドバイス】無理は禁物です。利守航とお茶でもして、リラックスしましょう。",
    "15. 悪魔": "【意味】誘惑、束縛\n\n【アドバイス】悪い誘惑には注意！利守航に止めてもらうよう頼んでおきましょう（笑）",
    "16. 塔": "【意味】崩壊、予期せぬ変化\n\n【アドバイス】ハプニングが起きても大丈夫。利守航がきっと助けに来てくれます。",
    "17. 星": "【意味】希望、夢、ひらめき\n\n【アドバイス】あなたの夢を利守航に語ってみてください。きっと応援してくれます。",
    "18. 月": "【意味】不安、曖昧さ\n\n【アドバイス】先が見えなくて不安な夜は、利守航に連絡してみましょう。",
    "19. 太陽": "【意味】成功、喜び、活力\n\n【アドバイス】運気は最高潮！利守航とパーッと遊びに行くとさらに運気が上がります。",
    "20. 審判": "【意味】復活、決断、目覚め\n\n【アドバイス】諦めていたことに再挑戦する時です。利守航も背中を押しています。",
    "21. 世界": "【意味】完成、達成、満足\n\n【アドバイス】最高のハッピーエンドです。利守航と一緒に喜びを分かち合いましょう！"
}

# --- ユーザー入力 ---
with st.form(key='tarot_form'):
    user_name = st.text_input("お名前（ニックネーム）", placeholder="ここにお名前を入力してください")
    user_input = st.text_area("相談内容（心の中で利守航に問いかけてください）", height=100)
    submit_button = st.form_submit_button(label='運命のカードを引く')

# --- 占いの実行 ---
if submit_button:
    # 名前が空欄の場合は「名無しさん」にする
    if not user_name:
        user_name = "名無し"

    # 演出
    with st.spinner(f'{user_name}さんの運命を、利守航が占っています...'):
        time.sleep(1.5)
        
        # カード抽選
        card_name = random.choice(list(TAROT_DATA.keys()))
        card_result = TAROT_DATA[card_name]
        card_image_url = TAROT_IMAGES[card_name]
        position = random.choice(["正位置", "逆位置"])
        
        # 1. 画面表示
        st.divider()
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(card_image_url, caption=card_name)
        
        with col2:
            st.subheader(f"🎴 結果: {card_name} ({position})")
            st.markdown(card_result)
            
            if position == "逆位置":
                st.caption("※逆位置が出ました。詳しくは利守航までご連絡を。")

        # 2. Gmail通知（相談内容がある場合のみ）
        if user_input:
            send_gmail_notify(user_name, user_input, card_name, position, card_result)
