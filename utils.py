import eval7
import streamlit as st

def evaluate_hand(cards):
    """7枚のカードからハンド評価値を返す"""
    hand_value = eval7.evaluate(cards)
    return hand_value

def generate_deck():
    """52枚のデッキを生成"""
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    """既知のカードをデッキから除外"""
    return [card for card in deck if card not in known_cards]

def generate_possible_hands(deck, board_needed=2):
    """可能な手札・ボードの組み合わせを生成"""
    possible_hands = []
    for i in range(len(deck)):
        for j in range(i + 1, len(deck)):
            if board_needed == 2:
                possible_hands.append([deck[i], deck[j]])
            elif board_needed == 1:
                possible_hands.append([deck[i]])
            elif board_needed == 3:
                for k in range(j + 1, len(deck)):
                    possible_hands.append([deck[i], deck[j], deck[k]])
    return possible_hands

def parse_card_input():
    """カード選択用の文字列リストを返す"""
    ranks = '2 3 4 5 6 7 8 9 T J Q K A'.split()
    suits = 'c d h s'.split()
    return [r + s for r in ranks for s in suits]

def is_mobile():
    """
    モバイル判定：画面幅で推測する簡易版
    クエリパラメータ 'width' を使い、幅768px以下ならモバイル扱い
    """
    query_params = st.experimental_get_query_params()
    width_param = query_params.get('width', [None])[0]
    if width_param:
        try:
            width = int(width_param)
            return width < 768  # スマホ・タブレット想定
        except ValueError:
            return False
    return False
