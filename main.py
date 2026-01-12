import streamlit as st
import random
import time

# --- ページ設定 ---
st.set_page_config(
    page_title="Classic Tarot",
    page_icon="🃏",
    layout="centered"
)

# --- タイトル ---
st.title("🃏 タロット占い（クラシック版）")
st.markdown("心を落ち着けて、ボタンを押してください。運命のカードが示されます。")

# --- カードの画像URLリスト（パブリックドメインのウェイト版） ---
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

# --- カードの意味データ ---
TAROT_DATA = {
    "0. 愚者": "【意味】始まり、自由、純粋、冒険\n【アドバイス】心のままに新しい一歩を踏み出しましょう。",
    "1. 魔術師": "【意味】創造、自信、スキルの発揮\n【アドバイス】あなたには十分な能力があります。自信を持って。",
    "2. 女教皇": "【意味】知性、直感、静寂\n【アドバイス】焦らず、自分の内なる声に耳を傾けてください。",
    "3. 女帝": "【意味】豊かさ、母性、繁栄\n【アドバイス】周囲への感謝と愛を大切にすることで運が開けます。",
    "4. 皇帝": "【意味】責任、安定、リーダーシップ\n【アドバイス】感情に流されず、意志を強く持って決断しましょう。",
    "5. 法王": "【意味】慈悲、信頼、伝統\n【アドバイス】信頼できる人の助言を求めると良いでしょう。",
    "6. 恋人": "【意味】選択、愛、調和\n【アドバイス】直感を信じて、心がワクワクする方を選びましょう。",
    "7. 戦車": "【意味】勝利、前進、行動力\n【アドバイス】迷わず突き進むべき時です。勢いを大切に。",
    "8. 力": "【意味】忍耐、勇気、優しさ\n【アドバイス】力づくではなく、粘り強さと優しさで乗り越えられます。",
    "9. 隠者": "【意味】内省、真理の探究\n【アドバイス】一人静かに考える時間を持ちましょう。",
    "10. 運命の輪": "【意味】チャンス、一時的な幸運\n【アドバイス】流れに身を任せることで、事態は好転します。",
    "11. 正義": "【意味】公平、誠実、バランス\n【アドバイス】感情を挟まず、客観的に判断することが大切です。",
    "12. 吊るされた男": "【意味】試練、忍耐、視点を変える\n【アドバイス】今は動かず、別の角度から物事を見てみましょう。",
    "13. 死神": "【意味】終わりと始まり、変化\n【アドバイス】執着を手放すことで、新しい道が開かれます。",
    "14. 節制": "【意味】調和、バランス、自制\n【アドバイス】極端な行動は避け、穏やかさを保ちましょう。",
    "15. 悪魔": "【意味】誘惑、束縛\n【アドバイス】悪い習慣や甘い誘惑に注意してください。",
    "16. 塔": "【意味】崩壊、予期せぬ変化\n【アドバイス】変化を恐れず、ゼロからやり直す覚悟を持ちましょう。",
    "17. 星": "【意味】希望、夢、ひらめき\n【アドバイス】明るい未来を信じることで、道は開かれます。",
    "18. 月": "【意味】不安、曖昧さ\n【アドバイス】見えないものに怯えず、夜明けを待ちましょう。",
    "19. 太陽": "【意味】成功、喜び、活力\n【アドバイス】ありのままの自分を表現してください。幸運はすぐそこです。",
    "20. 審判": "【意味】復活、決断、目覚め\n【アドバイス】過去を精算し、再挑戦するのに良いタイミングです。",
    "21. 世界": "【意味】完成、達成、満足\n【アドバイス】一つのサイクルが完成します。次のステージへ進みましょう。"
}

# --- ユーザー入力 ---
with st.form(key='tarot_form'):
    user_input = st.text_area("相談内容（心の中で唱えるだけでもOKです）", height=100)
    submit_button = st.form_submit_button(label='運命のカードを引く')

# --- 占いの実行 ---
if submit_button:
    # 演出
    with st.spinner('シャッフル中...'):
        time.sleep(1.5)
        
        # カードをランダムに選ぶ
        card_name = random.choice(list(TAROT_DATA.keys()))
        card_result = TAROT_DATA[card_name]
        card_image_url = TAROT_IMAGES[card_name]
        position = random.choice(["正位置", "逆位置"])
        
        st.divider()
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # ここで実際のタロット画像を表示します
            # 逆位置の場合は画像をひっくり返す設定も可能です（今回はシンプルにそのまま表示）
            st.image(card_image_url, caption=card_name)
        
        with col2:
            st.subheader(f"🎴 結果: {card_name} ({position})")
            st.info(card_result)
            
            if position == "逆位置":
                st.caption("※逆位置が出ました。意味が弱まったり、逆の意味になったりします。注意深く読み解いてください。")
