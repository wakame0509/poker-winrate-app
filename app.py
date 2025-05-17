import streamlit as st
from calculate_winrate import run_monte_carlo_simulation, run_enumeration_simulation, simulate_winrate_shift, simulate_winrate_shift_montecarlo
from hand_range_matrix import display_hand_range_selector
from utils import parse_card_input, is_mobile

st.set_page_config(page_title="Poker Winrate Calculator v1.3")

st.title("Poker Winrate Calculator v1.3")

st.markdown("### プレイヤー1のハンドを選択")
cols = st.columns(2)
player1_card1 = cols[0].selectbox("カード1", options=parse_card_input(), key="p1_card1")
player1_card2 = cols[1].selectbox("カード2", options=parse_card_input(), key="p1_card2")

st.markdown("### コミュニティカード（任意）")
board_cols = st.columns(5)
board_cards = []
for i in range(5):
    card = board_cols[i].selectbox(f"カード{i+1}", options=[""] + parse_card_input(), key=f"board_card_{i}")
    if card:
        board_cards.append(card)

st.markdown("### モンテカルロ法 試行回数選択")
tries_options = [10_000, 100_000, 200_000, 500_000, 1_000_000]
default_index = tries_options.index(100_000)
num_simulations = st.selectbox("試行回数", tries_options, index=default_index)

st.markdown("### プレイヤー2のハンドレンジを選択")
selected_range = display_hand_range_selector()

# 勝率変動計算モード切り替え
st.markdown("### 勝率変動表示モード")
shift_mode = st.radio("次に来るカードごとの勝率変動は…", ["精密モード（数え上げ法）", "高速モード（モンテカルロ法）"], horizontal=True)

if st.button("勝率を計算"):
    if len(board_cards) < 3:
        st.info("プリフロップ or ポストフロップ段階：モンテカルロ法を使用します。")
        winrate = run_monte_carlo_simulation(player1_card1, player1_card2, board_cards, selected_range, num_simulations)
    else:
        st.info("フロップ以降：数え上げ法で計算します。")
        winrate = run_enumeration_simulation(player1_card1, player1_card2, board_cards, selected_range)

    st.success(f"プレイヤー1の勝率：{winrate:.2f}%")

    if len(board_cards) in [3, 4]:
        st.markdown("### 次に来るカードごとの勝率変動")

        if shift_mode == "精密モード（数え上げ法）":
            shift_df = simulate_winrate_shift(player1_card1, player1_card2, board_cards, selected_range)
        else:
            shift_df = simulate_winrate_shift_montecarlo(player1_card1, player1_card2, board_cards, selected_range, num_simulations=10_000)

        st.dataframe(shift_df)
