import streamlit as st
import random
import numpy as np
from itertools import combinations
from collections import Counter
from eval7 import Card, evaluate

# 試行回数選択
sim_count = st.sidebar.selectbox("モンテカルロ試行回数", [100000 * i for i in range(1, 11)], index=0)

# カード選択
def card_selector(label, used_cards):
    suits = ['s', 'h', 'd', 'c']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    options = [r + s for r in ranks for s in suits if r + s not in used_cards]
    return st.selectbox(label, [""] + options)

# 入力
st.title("テキサスホールデム 勝率計算 (v1.2 完全版)")
used_cards = set()

col1, col2 = st.columns(2)
with col1:
    p1_card1 = card_selector("プレイヤー1 - カード1", used_cards)
    if p1_card1: used_cards.add(p1_card1)
    p1_card2 = card_selector("プレイヤー1 - カード2", used_cards)
    if p1_card2: used_cards.add(p1_card2)

with col2:
    opp_hand_range = st.multiselect("相手ハンド（省略可、指定しない場合はランダム）", [])
    p2_card1 = card_selector("プレイヤー2 - カード1", used_cards)
    if p2_card1: used_cards.add(p2_card1)
    p2_card2 = card_selector("プレイヤー2 - カード2", used_cards)
    if p2_card2: used_cards.add(p2_card2)

flop1 = card_selector("フロップ1", used_cards)
if flop1: used_cards.add(flop1)
flop2 = card_selector("フロップ2", used_cards)
if flop2: used_cards.add(flop2)
flop3 = card_selector("フロップ3", used_cards)
if flop3: used_cards.add(flop3)

turn = card_selector("ターン", used_cards)
if turn: used_cards.add(turn)
river = card_selector("リバー", used_cards)
if river: used_cards.add(river)

def valid_cards(*cards):
    return all(cards) and len(set(cards)) == len(cards)

# 勝率計算
if st.button("勝率計算"):

    if not valid_cards(p1_card1, p1_card2):
        st.error("プレイヤー1のカードを2枚選んでください。")
    else:
        st.write("計算中…")
        deck = [Card(r + s) for r in '23456789TJQKA' for s in 'shdc']
        p1 = [Card(p1_card1), Card(p1_card2)]
        if p2_card1 and p2_card2:
            p2 = [Card(p2_card1), Card(p2_card2)]
        else:
            p2 = None

        known = [c for c in [flop1, flop2, flop3, turn, river] if c]
        known_cards = [Card(c) for c in known]
        excluded = p1 + known_cards
        if p2:
            excluded += p2

        for c in excluded:
            if c in deck:
                deck.remove(c)

        wins = 0
        ties = 0
        losses = 0

        for _ in range(sim_count):
            random.shuffle(deck)
            community = known_cards.copy()
            needed = 5 - len(community)
            community += deck[:needed]

            if not p2:
                opp = deck[needed:needed + 2]
            else:
                opp = p2

            p1_score = evaluate(p1 + community)
            p2_score = evaluate(opp + community)

            if p1_score > p2_score:
                wins += 1
            elif p1_score == p2_score:
                ties += 1
            else:
                losses += 1

        total = wins + ties + losses
        win_pct = 100 * wins / total
        tie_pct = 100 * ties / total
        loss_pct = 100 * losses / total

        st.success(f"勝率: {win_pct:.2f}%, 引き分け: {tie_pct:.2f}%, 敗北: {loss_pct:.2f}%")
