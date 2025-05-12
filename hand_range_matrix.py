import streamlit as st

RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

def get_hand_label(i, j):
    if i == j:
        return f"{RANKS[i]}{RANKS[j]}"
    elif i < j:
        return f"{RANKS[i]}{RANKS[j]}s"
    else:
        return f"{RANKS[j]}{RANKS[i]}o"

def render_hand_range_matrix():
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


def expand_hand_range_labels(selected_labels):
    """
    「AKs」や「QJo」などのラベルを、実際の2枚のカードの組み合わせに展開する。
    例：AKs → ['AsKs', 'AdKd', 'AhKh', 'AcKc']
    """
    suits = ['s', 'h', 'd', 'c']
    all_combos = []

    for label in selected_labels:
        rank1 = label[0]
        rank2 = label[1]
        suited = 's' in label
        offsuit = 'o' in label
        pairs = rank1 == rank2

        if pairs:
            for i in range(len(suits)):
                for j in range(i + 1, len(suits)):
                    all_combos.append(f"{rank1}{suits[i]},{rank2}{suits[j]}")
        elif suited:
            for suit in suits:
                all_combos.append(f"{rank1}{suit},{rank2}{suit}")
        elif offsuit:
            for suit1 in suits:
                for suit2 in suits:
                    if suit1 != suit2:
                        all_combos.append(f"{rank1}{suit1},{rank2}{suit2}")
        else:
            # 指定なし（両方）
            for suit1 in suits:
                for suit2 in suits:
                    if rank1 != rank2 or suit1 != suit2:
                        all_combos.append(f"{rank1}{suit1},{rank2}{suit2}")

    return all_combos
