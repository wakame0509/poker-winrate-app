import streamlit as st
import random
import numpy as np
from collections import Counter
from itertools import combinations

# カードの定義
suits = ['s', 'h', 'd', 'c']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = [r + s for r in ranks for s in suits]

# 勝率計算関数（モンテカルロ法）
def estimate_win_rate_monte_carlo(player_hand, community_cards, opp_range, iterations=10000):
    wins = 0
    ties = 0
    losses = 0

    for _ in range(iterations):
        used_cards = set(player_hand + community_cards)
        deck_remaining = [card for card in deck if card not in used_cards]

        opp_hand = random.choice(opp_range)
        if any(card in used_cards for card in opp_hand):
            continue
        used_cards.update(opp_hand)

        total_community = community_cards.copy()
        while len(total_community) < 5:
            card = random.choice(deck_remaining)
            if card not in used_cards:
                total_community.append(card)
                used_cards.add(card)

        player_best = get_best_hand(player_hand + total_community)
        opp_best = get_best_hand(opp_hand + total_community)

        if player_best > opp_best:
            wins += 1
        elif player_best == opp_best:
            ties += 1
        else:
            losses += 1

    total = wins + ties + losses
    return round(wins / total * 100, 2), round(ties / total * 100, 2), round(losses / total * 100, 2)

# 役の強さ評価（簡易版）
def get_best_hand(cards):
    values = sorted([ranks.index(card[0]) for card in cards], reverse=True)
    return values[:5]

# UI部分
st.title("テキサスホールデム 勝率計算ツール v1.2前半")

# プレイヤーの手札選択
st.subheader("プレイヤーの手札")
available_cards = deck.copy()
player_cards = []

col1, col2 = st.columns(2)
with col1:
    card1 = st.selectbox("カード1", [""] + available_cards, key="p1")
    if card1 and card1 != "":
        player_cards.append(card1)
        available_cards.remove(card1)
with col2:
    card2 = st.selectbox("カード2", [""] + available_cards, key="p2")
    if card2 and card2 != "":
        player_cards.append(card2)
        if card2 in available_cards:
            available_cards.remove(card2)

# コミュニティカード選択
st.subheader("コミュニティカード")
community_cards = []
for i in range(5):
    card = st.selectbox(f"カード {i+1}", [""] + available_cards, key=f"comm{i}")
    if card and card != "":
        community_cards.append(card)
        if card in available_cards:
            available_cards.remove(card)

# 相手のハンドレンジ指定（簡易：ランダムまたは固定数種）
st.subheader("相手のハンドレンジ選択")
opp_range_option = st.radio("レンジタイプを選択", ["ランダム", "強いハンドのみ"])

def generate_opponent_range(option):
    possible = [list(h) for h in combinations(deck, 2) if h[0] != h[1]]
    if option == "強いハンドのみ":
        filtered = [h for h in possible if h[0][0] == h[1][0] or h[0][1] == h[1][1]]
        return random.sample(filtered, min(len(filtered), 50))
    else:
        return random.sample(possible, min(len(possible), 300))

# 勝率計算実行
if len(player_cards) == 2:
    if st.button("勝率を計算する"):
        opp_range = generate_opponent_range(opp_range_option)
        win, tie, lose = estimate_win_rate_monte_carlo(player_cards, community_cards, opp_range, iterations=10000)
        st.markdown(f"### 勝率: {win}% / 引き分け: {tie}% / 敗北: {lose}%")
else:
    st.info("プレイヤーの2枚のカードを選んでください。")
