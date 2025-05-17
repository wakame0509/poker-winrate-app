import streamlit as st

RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
SUITS = ['c', 'd', 'h', 's']

def get_hand_label(i, j):
    if i == j:
        return f"{RANKS[i]}{RANKS[j]}"
    elif i < j:
        return f"{RANKS[i]}{RANKS[j]}s"
    else:
        return f"{RANKS[j]}{RANKS[i]}o"

def generate_suited_combinations(rank1, rank2):
    return [f"{rank1}{suit}{rank2}{suit}" for suit in SUITS]

def generate_offsuited_combinations(rank1, rank2):
    combos = []
    for suit1 in SUITS:
        for suit2 in SUITS:
            if suit1 != suit2:
                combos.append(f"{rank1}{suit1}{rank2}{suit2}")
    return combos

def generate_pair_combinations(rank):
    combos = []
    for i in range(len(SUITS)):
        for j in range(i + 1, len(SUITS)):
            combos.append(f"{rank}{SUITS[i]}{rank}{SUITS[j]}")
    return combos

def display_hand_range_selector():
    st.markdown("#### プレイヤー2のハンドレンジを選択")
    selected_hands = []

    grid_cols = st.columns(13)
    for i in range(13):
        with grid_cols[i]:
            for j in range(13):
                label = get_hand_label(i, j)
                if st.checkbox(label, key=f"hand_{i}_{j}"):
                    if 's' in label:
                        rank1, rank2 = label[0], label[1]
                        combos = generate_suited_combinations(rank1, rank2)
                        for combo in combos:
                            selected_hands.append([combo[:2], combo[2:]])
                    elif 'o' in label:
                        rank1, rank2 = label[0], label[1]
                        combos = generate_offsuited_combinations(rank1, rank2)
                        for combo in combos:
                            selected_hands.append([combo[:2], combo[2:]])
                    else:
                        # ポケットペア
                        rank = label[0]
                        combos = generate_pair_combinations(rank)
                        for combo in combos:
                            selected_hands.append([combo[:2], combo[2:]])

    return selected_hands
