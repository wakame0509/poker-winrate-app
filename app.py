import streamlit as st
from PIL import Image
import os
import random

from calculate_winrate import calculate_winrate_montecarlo, calculate_winrate_enumeration
from hand_range_matrix import display_hand_range_selector
from utils import get_card_image_path, get_deck, remove_selected_cards_from_deck, parse_range_to_hands

# --- UI設定 ---
st.set_page_config(page_title="テキサスホールデム勝率計算ツール", layout="wide")
st.title("テキサスホールデム勝率計算ツール")

# --- 定数と初期化 ---
suits = ['s', 'h', 'd', 'c']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = get_deck()

# --- セッション状態初期化 ---
if "selected_cards" not in st.session_state:
    st.session_state.selected_cards = []

# --- カード選択UI ---
def card_selector(label, key_prefix):
    selected = []
    cols = st.columns(2)
    for i in range(2):
        with cols[i]:
            rank = st.selectbox(f"{label} Rank {i+1}", ranks, key=f"{key_prefix}_rank_{i}")
            suit = st.selectbox(f"{label} Suit {i+1}", suits, key=f"{key_prefix}_suit_{i}")
            card = rank + suit
            selected.append(card)
    return selected

# --- 自分のハンド選択 ---
st.subheader("自分のハンド")
player_hand = card_selector("プレイヤー", "player")

# --- ハンドレンジ選択 ---
st.subheader("相手のハンドレンジ")
selected_range = display_hand_range_selector()

# --- ボード選択 ---
st.subheader("ボードカード（任意）")
board_cards = []
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        rank = st.selectbox(f"Board Rank {i+1}", [""] + ranks, key=f"board_rank_{i}")
        suit = st.selectbox(f"Board Suit {i+1}", [""] + suits, key=f"board_suit_{i}")
        if rank and suit:
            board_cards.append(rank + suit)

# --- モンテカルロ試行回数選択 ---
st.subheader("モンテカルロ試行回数")
num_simulations = st.selectbox("回数を選択", [100000, 200000, 300000, 400000, 500000,
                                           600000, 700000, 800000, 900000, 1000000], index=0)

# --- 勝率計算ボタン ---
if st.button("勝率計算を実行"):
    all_selected = player_hand + board_cards
    if len(set(all_selected)) != len(all_selected):
        st.error("同じカードが複数選ばれています。")
    else:
        st.write("計算中...")
        # モード分岐：フロップ以降は数え上げ、それ以前はモンテカルロ
        if len(board_cards) >= 3:
            result = calculate_winrate_enumeration(player_hand, selected_range, board_cards)
        else:
            result = calculate_winrate_montecarlo(player_hand, selected_range, board_cards, num_simulations)
        st.success("計算完了！")
        st.write(result)
