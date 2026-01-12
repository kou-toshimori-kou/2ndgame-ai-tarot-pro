import streamlit as st
import random
import time
import requests

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
        if "LINE_TOKEN" in st.secrets:
            token = st.secrets["LINE_TOKEN"]
            headers = {"Authorization": "Bearer " + token}
            payload = {"message": message}
            requests.post(url, headers=headers, data=payload)
    except Exception as e:
        print(f"LINE通知エラー: {e}")

# --- タイトル ---
st.title("🃏 利守航のタロット占い")
st.markdown("心を落ち着けてボタンを押してください。\n利守航からの運命のメッセージが届きます。")

# --- 画像リスト（完全に別の安定したソースに変更） ---
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
    "15. 悪魔": "【意味】誘惑
