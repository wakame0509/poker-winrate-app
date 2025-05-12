import streamlit as st

SUITS = ['s', 'h', 'd', 'c']
RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

def generate_hand_matrix():
    matrix = []
    for i, r1 in enumerate(RANKS):
        row = []
        for j, r2 in enumerate(RANKS):
            if i < j:
                hand = r1 + r2 + "s"  # suited
            elif i > j:
                hand = r2 + r1 + "o"  # offsuit
            else:
                hand = r1 + r2  # pair
            row.append(hand)
        matrix.append(row)
    return matrix

def select_hand_range():
    st.write("### ハンドレンジ選択（任意）")
    matrix = generate_hand_matrix()
    selected = []

    for i, row in enumerate(matrix):
        cols = st.columns(len(row))
        for j, hand in enumerate(row):
            if cols[j].checkbox(hand, key=f"{i}-{j}"):
                selected.append(hand)
    
    return selected
