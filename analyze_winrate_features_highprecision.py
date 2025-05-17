import pandas as pd
from calculate_winrate import simulate_winrate_shift_montecarlo
from utils import generate_deck
import multiprocessing
import os

# --- 設定値 ---
NUM_SIMULATIONS = 100000  # 高精度用
BOARD_PATTERNS = [
    ['Ah', '7d', '2c'],  # Dry board
    ['Jd', 'Th', '9h'],  # Wet board
    ['7s', '7c', '2d'],  # Paired board
    ['5c', '4d', '3h'],  # Low board
    ['Kd', 'Qc', '3s']   # High card board
]
SELECTED_RANGE = []  # 今は全ハンド、あとで現実的レンジにも対応可

# --- 特徴量判定関数 ---
def analyze_features(hand, next_card, board):
    features = {
        'SetCompleted': False,
        'OvercardAppeared': False,
        'StraightCompleted': False,
        'FlushDrawAppeared': False,
        'FlushCompleted': False
    }

    ranks = '2 3 4 5 6 7 8 9 T J Q K A'.split()
    suits = 'c d h s'.split()

    if len(hand) == 2:
        pair_rank = hand[0]
        if next_card[0] == pair_rank:
            features['SetCompleted'] = True

    hand_high_rank = hand[0]
    next_card_rank = next_card[0]
    if ranks.index(next_card_rank) < ranks.index(hand_high_rank):
        features['OvercardAppeared'] = True

    hand_ranks = [hand[0], hand[1]]
    combined_ranks = set(hand_ranks + [card[0] for card in board] + [next_card[0]])
    for i in range(len(ranks) - 4):
        straight_ranks = set(ranks[i:i+5])
        if straight_ranks.issubset(combined_ranks):
            features['StraightCompleted'] = True

    suit_counts = {s: 0 for s in suits}
    for card in board:
        suit_counts[card[1]] += 1
    suit_counts[next_card[1]] += 1

    if any(count >= 3 for count in suit_counts.values()):
        features['FlushDrawAppeared'] = True
    if any(count >= 4 for count in suit_counts.values()):
        features['FlushCompleted'] = True

    return features

# --- シミュレーション関数 ---
def simulate_for_hand(args):
    hand, board = args
    p1_card1 = hand[0] + 's'
    p1_card2 = hand[1] + ('h' if 'o' in hand else 's')

    shift_df = simulate_winrate_shift_montecarlo(p1_card1, p1_card2, board, SELECTED_RANGE, NUM_SIMULATIONS)

    results = []
    for _, row in shift_df.iterrows():
        features = analyze_features(hand, row['Card'], board)
        results.append({
            'Hand': hand,
            'Board': ''.join(board),
            'NextCard': row['Card'],
            'Winrate': row['Winrate'],
            **features
        })
    return results

# --- ハンドリスト生成 ---
def generate_all_hands():
    ranks = 'A K Q J T 9 8 7 6 5 4 3 2'.split()
    hands = []
    for i, r1 in enumerate(ranks):
        for j, r2 in enumerate(ranks):
            if i < j:
                hands.append(f"{r1}{r2}s")
            elif i > j:
                hands.append(f"{r2}{r1}o")
            else:
                hands.append(f"{r1}{r1}")
    return hands

# --- 並列シミュレーション実行 ---
if __name__ == '__main__':
    all_hands = generate_all_hands()
    args_list = [(hand, board) for hand in all_hands for board in BOARD_PATTERNS]

    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        all_results = pool.map(simulate_for_hand, args_list)

    # フラット化してDataFrame化
    flat_results = [item for sublist in all_results for item in sublist]
    df = pd.DataFrame(flat_results)

    # 特徴量ごとの勝率変動影響を集計
    results = []
    features_to_check = ['SetCompleted', 'OvercardAppeared', 'StraightCompleted', 'FlushDrawAppeared', 'FlushCompleted']

    for feature in features_to_check:
        feature_data = df[df[feature]]

        grouped = feature_data.groupby('Hand')['Winrate'].mean().reset_index()
        grouped['Feature'] = feature

        results.append(grouped)

    final_df = pd.concat(results, ignore_index=True)

    # CSV出力
    final_df.to_csv('highprecision_feature_analysis.csv', index=False)

    print("高精度特徴量分析結果を highprecision_feature_analysis.csv に出力しました。")
