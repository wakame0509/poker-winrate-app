import streamlit as st
from calculate_winrate import run_monte_carlo_simulation, run_enumeration_simulation, simulate_winrate_shift
from hand_range_matrix import display_hand_range_selector
from utils import parse_card_input, generate_deck, remove_known_cards

st.set_page_config(page_title="テキサスホールデム勝率計算ツール", layout="wide")
st.title("テキサスホールデム勝率計算ツール")

st.sidebar.header("設定")
simulations = st.sidebar.selectbox(
    "モンテカルロ法の試行回数",
    options=[100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000],
    index=0
)

st.subheader("プレイヤーのハンド")
col1, col2 = st.columns(2)
with col1:
    player1_hand = st.text_input("プレイヤー1", value="As Kh")
with col2:
    player2_hand = st.text_input("プレイヤー2（未指定でランダム）", value="")

st.subheader("ボード")
board_input = st.text_input("フロップ・ターン・リバー", value="")

st.subheader("相手のハンドレンジを指定（任意）")
selected_range = display_hand_range_selector()

show_shift = st.checkbox("次のカードごとの勝率変動を表示")

if st.button("勝率を計算"):
    try:
        board = parse_card_input(board_input)
        hero = parse_card_input(player1_hand)
        villain = parse_card_input(player2_hand) if player2_hand else []
        used_cards = hero + board + villain
        deck = remove_known_cards(generate_deck(), used_cards)

        # 使用する計算方法の選定（フロップ以降は数え上げ）
        if len(board) >= 3:
            win, lose, tie = run_enumeration_simulation(hero, board, villain, deck, selected_range)
        else:
            win, lose, tie = run_monte_carlo_simulation(hero, board, villain, deck, selected_range, simulations)

        total = win + lose + tie
        st.success(f"プレイヤー1の勝率: {win / total:.2%}")
        st.info(f"引き分け率: {tie / total:.2%}")
        st.error(f"敗北率: {lose / total:.2%}")

        if show_shift and len(board) in [3, 4]:
            stage = "turn" if len(board) == 3 else "river"
            st.subheader(f"次の{stage.upper()}カードによる勝率変動")
            shift = simulate_winrate_shift(hero, selected_range, board, stage)
            st.dataframe(shift)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
