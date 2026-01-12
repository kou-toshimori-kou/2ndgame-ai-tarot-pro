import streamlit as st
import random
import time
import requests  # 通信用の道具を追加

# --- ページ設定 ---
st.set_page_config(
    page_title="Toshimori Tarot",
    page_icon="🃏",
    layout="centered"
)

# --- LINE通知を送る関数 ---
def send_line_notify(message):
    try:
        url = "https://notify-api.line.me/api/notify"
        token = st.secrets["LINE_TOKEN"] # Secretsからトークンを取得
        headers = {"Authorization": "Bearer " + token}
        payload = {"message": message}
        requests.post(url, headers=headers, data=payload)
    except Exception as e:
        # 通知に失敗してもアプリは止めない（ユーザーにはバレないようにする）
        print(f"LINE通知エラー: {e}")

# --- タイトル ---
st.title("🃏 利守航のタロット占い")
st.markdown("心を落ち着けてボタンを押してください。\n利守航からの運命のメッセージが届きます。")

# --- 画像リスト ---
TAROT_IMAGES = {
    "0. 愚者": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg",
    "1. 魔術師": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
    "2. 女教皇": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg",
    "3. 女帝": "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg",
    "4. 皇帝": "https://upload.wikimedia.org/wikipedia/commons/c/c3/RWS_Tarot_04_Emperor.jpg",
    "5. 法王": "https://upload.wikimedia.org/wikipedia/commons/8/8d/RWS_Tarot_05_Hierophant.jpg",
    "6. 恋人": "https://upload.wikimedia.org/wikipedia/commons/3/33/RWS_Tarot_06_Lovers.jpg",
    "7. 戦車": "https://upload.wikimedia.org/wikipedia/commons/9/9b/RWS_Tarot_07_Chariot.jpg",
    "8. 力": "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg",
    "9. 隠者": "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg",
    "10. 運命の輪": "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg",
    "11. 正義": "https://upload.wikimedia.org/wikipedia/commons/e/e0/RWS_Tarot_11_Justice.jpg",
    "12. 吊るされた男": "https://upload.wikimedia.org/wikipedia/commons/2/2b/RWS_Tarot_12_Hanged_Man.jpg",
    "13. 死神": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg",
    "14. 節制": "https://upload.wikimedia.org/wikipedia/commons/f/f8/RWS_Tarot_14_Temperance.jpg",
    "15. 悪魔": "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg",
    "16. 塔": "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg",
    "17. 星": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg",
    "18. 月": "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg",
    "19. 太陽": "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg",
    "20. 審判": "https://upload.wikimedia.org/wikipedia/commons/d/dd/RWS_Tarot_20_Judgement.jpg",
    "21. 世界": "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg"
}

# --- データリスト（利守航スペシャル） ---
TAROT_DATA = {
    "0. 愚者": "【意味】始まり、自由、純粋、冒険\n\n【アドバイス】利守航と一緒に、思い切って新しい旅に出かけましょう！",
    "1. 魔術師": "【意味】創造、自信、スキルの発揮\n\n【アドバイス】何かを始めるチャンスです。利守航のアイデアを借りるとうまくいきます。",
    "2. 女教皇": "【意味】知性、直感、静寂\n\n【アドバイス】焦りは禁物です。利守航と静かに語り合う時間を持つと答えが見えます。",
    "3. 女帝": "【意味】豊かさ、母性、繁栄\n\n【アドバイス】利守航に日頃の感謝を伝えてみてください。素晴らしいお返しがあるかも？",
    "4. 皇帝": "【意味】責任、安定、リーダーシップ\n\n【アドバイス】迷ったら利守航の決断に従ってみましょう。頼りになるはずです。",
    "5. 法王": "【意味】慈悲、信頼、伝統\n\n【アドバイス】困った時は利守航に助言を求めると、事態は好転します。",
    "6. 恋人": "【意味】選択、愛、調和\n\n【アドバイス】心がワクワクする方を選びましょう。利守航との相性も最高です！",
    "7. 戦車": "【意味】勝利、前進、行動力\n\n【アドバイス】利守航と共に突き進めば、どんな壁も突破できます。",
    "8. 力": "【意味】忍耐、勇気、優しさ\n\n【アドバイス】力ずくではなく、利守航のような優しさと粘り強さで接しましょう。",
    "9. 隠者": "【意味】内省、真理の探究\n\n【アドバイス】一人で悩まず、利守航と深い話をしてみるのも良いでしょう。",
    "10. 運命の輪": "【意味】チャンス、一時的な幸運\n\n【アドバイス】流れに乗る時です。利守航との偶然の再会が運命を変えます。",
    "11. 正義": "【意味】公平、誠実、バランス\n\n【アドバイス】利守航は公平に見ています。誠実な態度でいれば評価されます。",
    "12. 吊るされた男": "【意味】試練、忍耐、視点を変える\n\n【アドバイス】今は動けなくても大丈夫。利守航の変わった視点を取り入れてみてください。",
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
    user_input = st.text_area("相談内容（心の中で利守航に問いかけてください）", height=100)
    submit_button = st.form_submit_button(label='運命のカードを引く')

# --- 占いの実行 ---
if submit_button:
    # 演出
    with st.spinner('利守航がカードを選んでいます...'):
        time.sleep(1.5)
        
        # カードをランダムに選ぶ
        card_name = random.choice(list(TAROT_DATA.keys()))
        card_result = TAROT_DATA[card_name]
        card_image_url = TAROT_IMAGES[card_name]
        position = random.choice(["正位置", "逆位置"])
        
        # ★ここでLINEに通知を送る
        if user_input:
            notification_message = f"\n【相談着信】\n相談内容: {user_input}\n結果: {card_name} ({position})"
            send_line_notify(notification_message)
        
        st.divider()
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(card_image_url, caption=card_name)
        
        with col2:
            st.subheader(f"🎴 結果: {card_name} ({position})")
            st.markdown(card_result)
            
            if position == "逆位置":
                st.caption("※逆位置が出ました。利守航からのメッセージを、少し慎重に受け取ってください。")
