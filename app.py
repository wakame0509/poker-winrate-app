import streamlit as st
import itertools
import random

# カードのスートとランク
suits = ['s', 'h', 'd', 'c']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = [r + s for r in ranks for s in suits]

# 使用済みカード管理
def get_available_cards(selected_cards):
    return [card for card in deck if card not in selected_cards]

st.title("テキサスホールデム 勝率計算ツール v1.1")

# セッション状態の初期化
if "selected_cards" not in st.session_state:
    st.session_state.selected_cards = []

def card_selector(label):
    options = get_available_cards(st.session_state.selected_cards)
    card = st.selectbox(label, ["--"] + options, key=label)
    if card != "--" and card not in st.session_state.selected_cards:
        st.session_state.selected_cards.append(card)
    return card

# プレイヤー1と2のハンド
st.subheader("プレイヤー1のハンド")
p1_card1 = card_selector("P1 Card 1")
p1_card2 = card_selector("P1 Card 2")

st.subheader("プレイヤー2のハンド")
p2_card1 = card_selector("P2 Card 1")
p2_card2 = card_selector("P2 Card 2")

# ボードカード
st.subheader("ボード（任意）")
flop1 = card_selector("Flop 1")
flop2 = card_selector("Flop 2")
flop3 = card_selector("Flop 3")
turn = card_selector("Turn")
river = card_selector("River")

# 勝率計算（簡易モンテカルロ法）
def simulate(p1, p2, board, n_sim=10000):
    from collections import Counter

    wins = Counter()
    known = p1 + p2 + board
    remaining = [c for c in deck if c not in known]
    needed = 5 - len(board)

    for _ in range(n_sim):
        sampled = random.sample(remaining, needed)
        full_board = board + sampled

        # ランダムな評価（プレースホルダ）
        p1_score = random.random()
        p2_score = random.random()

        if p1_score > p2_score:
            wins['P1'] += 1
        elif p2_score > p1_score:
            wins['P2'] += 1
        else:
            wins['Tie'] += 1

    total = sum(wins.values())
    return {k: round(v / total * 100, 2) for k, v in wins.items()}

if st.button("勝率を計算"):
    if "--" in [p1_card1, p1_card2, p2_card1, p2_card2]:
        st.warning("すべてのハンドを選択してください。")
    else:
        p1 = [p1_card1, p1_card2]
        p2 = [p2_card1, p2_card2]
        board = [c for c in [flop1, flop2, flop3, turn, river] if c != "--"]
        result = simulate(p1, p2, board)
        st.success("勝率計算結果:")
        st.write(f"プレイヤー1: {result.get('P1', 0)}%")
        st.write(f"プレイヤー2: {result.get('P2', 0)}%")
        st.write(f"引き分け: {result.get('Tie', 0)}%")

# リセットボタン
if st.button("カードをリセット"):
    st.session_state.selected_cards = []
    st.experimental_rerun()
