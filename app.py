import streamlit as st
import random
from treys import Card, Deck, Evaluator
import numpy as np

st.set_page_config(layout="wide")
st.title("テキサスホールデム 勝率計算ツール（ヘッズアップ、6人テーブル）")

# --- ユーザー入力用 UI ---
st.markdown("### プレイヤー1のハンドを選択")
col1, col2 = st.columns(2)
ranks = '23456789TJQKA'
suits = 'shdc'
options = [r + s for r in ranks for s in suits]

with col1:
    card1 = st.selectbox("カード1", options, key="p1_card1")
with col2:
    card2 = st.selectbox("カード2", [c for c in options if c != card1], key="p1_card2")

st.markdown("---")
st.markdown("### フロップ / ターン / リバー（任意）")
flop1 = st.selectbox("フロップ1", ["--"] + options, key="flop1")
flop2 = st.selectbox("フロップ2", ["--"] + options, key="flop2")
flop3 = st.selectbox("フロップ3", ["--"] + options, key="flop3")
turn = st.selectbox("ターン", ["--"] + options, key="turn")
river = st.selectbox("リバー", ["--"] + options, key="river")

community_cards = [flop1, flop2, flop3, turn, river]
community_cards = [c for c in community_cards if c != "--"]

# --- 勝率シミュレーション ---
def simulate(player_hand, known_community, iterations=1000):
    evaluator = Evaluator()
    wins, ties = 0, 0
    p1_cards = [Card.new(c) for c in player_hand]
    known_board = [Card.new(c) for c in known_community]
    used_cards = set(player_hand + known_community)

    for _ in range(iterations):
        deck = [r + s for r in ranks for s in suits if r + s not in used_cards]
        random.shuffle(deck)

        # プレイヤー2のランダムハンド
        p2_hand = deck[:2]
        used = used_cards.union(p2_hand)

        # 残りのボードカードをランダムに埋める
        missing = 5 - len(known_board)
        rem_board = [Card.new(c) for c in deck[2:2+missing]]
        full_board = known_board + rem_board

        p2_cards = [Card.new(c) for c in p2_hand]

        p1_score = evaluator.evaluate(full_board, p1_cards)
        p2_score = evaluator.evaluate(full_board, p2_cards)

        if p1_score < p2_score:
            wins += 1
        elif p1_score == p2_score:
            ties += 1
        # else: player 1 loses

    return wins / iterations, ties / iterations

if st.button("勝率を計算"):
    with st.spinner("計算中..."):
        winrate, tirerate = simulate([card1, card2], community_cards, iterations=3000)
        st.success(f"勝率：{winrate*100:.2f}%　引き分け：{tirerate*100:.2f}%")
