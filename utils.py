import eval7

def evaluate_hand(cards):
    hand_value = eval7.evaluate(cards)
    return hand_value

def generate_deck():
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    return [card for card in deck if card not in known_cards]

def generate_possible_hands(deck, board_needed=2):
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
    ranks = '2 3 4 5 6 7 8 9 T J Q K A'.split()
    suits = 'c d h s'.split()
    return [r + s for r in ranks for s in suits]

def is_mobile():
    import streamlit as st
    user_agent = st.get_option('browser.userAgent')
    if user_agent and ('Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent):
        return True
    return False
