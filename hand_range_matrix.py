import streamlit as st

RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

def get_hand_label(i, j):
    if i == j:
        return f"{RANKS[i]}{RANKS[j]}"
    elif i < j:
        return f"{RANKS[i]}{RANKS[j]}s"
    else:
        return f"{RANKS[j]}{RANKS[i]}o"

def display_hand_range_selector():
    selected_hands = set()
    st.markdown("#### プレイヤー2のハンドレンジを選択")

    for i in range(len(RANKS)):
        cols = st.columns(len(RANKS))
        for j in range(len(RANKS)):
            label = get_hand_label(i, j)
            key = f"range_{i}_{j}"
            if cols[j].checkbox(label, key=key):
                selected_hands.add(label)

    return selected_hands
