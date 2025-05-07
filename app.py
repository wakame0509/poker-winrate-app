import streamlit as st
import random
import itertools
from collections import Counter

RANKS = '23456789TJQKA'
SUITS = 'cdhs'
DECK = [r + s for r in RANKS for s in SUITS]

def evaluate_hand(hand):
    ranks = ' --23456789TJQKA'
    values = sorted([ranks.index(c[0]) for c in hand], reverse=True)
    counts = Counter([c[0] for c in hand])
    suits = [c[1] for c in hand]
    flush = len(set(suits)) == 1
    straight = all(values[i] - 1 == values[i + 1] for i in range(4))
    if straight and flush:
        return (8, values[0])  # Straight flush
    if 4 in counts.values():
        return (7, counts.most_common(1)[0][0])  # Four of a kind
    if sorted(counts.values()) == [2, 3]:
        return (6, counts.most_common(1)[0][0])  # Full house
    if flush:
        return (5, values)  # Flush
    if straight:
        return (4, values[0])  # Straight
    if 3 in counts.values():
        return (3, counts.most_common(1)[0][0])  # Three of a kind
    if list(counts.values()).count(2) == 2:
        return (2, counts.most_common(2))  # Two pair
    if 2 in counts.values():
        return (1, counts.most_common(1)[0][0])  # One pair
    return (0, values)  # High card

def calculate_win_rate(player_hand, community_cards, iterations=1000):
    wins = 0
    ties = 0
    losses = 0

    used_cards = set(player_hand + community_cards)
    remaining_deck = [c for c in DECK if c not in used_cards]

    for _ in range(iterations):
        deck_copy = remaining_deck[:]
        random.shuffle(deck_copy)

        opp_hand = deck_copy[:2]
        num_needed = 5 - len(community_cards)
        board = community_cards + deck_copy[2:2 + num_needed]

        player_best = evaluate_hand(player_hand + board)
        opp_best = evaluate_hand(opp_hand + board)

        if player_best > opp_best:
            wins += 1
        elif player_best < opp_best:
            losses += 1
        else:
            ties += 1

    total = wins + losses + ties
    return wins / total * 100, ties / total * 100, losses / total * 100

st.title("テキサスホールデム 勝率計算 (v1.0相当)")

selected_cards = []

st.subheader("プレイヤー1の手札を選んでください")
cols = st.columns(2)
player_hand = []
for i in range(2):
    with cols[i]:
        card = st.selectbox(f"カード {i + 1}", [''] + DECK, key=f"p1_card_{i}")
        if card and card not in selected_cards:
            player_hand.append(card)
            selected_cards.append(card)

st.subheader("コミュニティカード（任意）")
community_cards = []
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        card = st.selectbox(f"ボード {i + 1}", [''] + DECK, key=f"board_{i}")
        if card and card not in selected_cards:
            community_cards.append(card)
            selected_cards.append(card)

if len(player_hand) == 2:
    if st.button("勝率を計算"):
        with st.spinner("計算中..."):
            win, tie, loss = calculate_win_rate(player_hand, community_cards, iterations=10000)
        st.success(f"勝率: {win:.2f}% / 引き分け: {tie:.2f}% / 敗北: {loss:.2f}%")
else:
    st.info("まずプレイヤー1の手札を2枚選んでください。")
