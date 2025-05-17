import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# CSVファイル読み込み（12分類版）
df = pd.read_csv('winrate_shift_stats_12groups.csv')

# 出力フォルダ作成
output_dir = 'winrate_heatmaps'
os.makedirs(output_dir, exist_ok=True)

# カード順序をA〜2c/d/h/s順に固定
ranks = 'A K Q J T 9 8 7 6 5 4 3 2'.split()
suits = 'c d h s'.split()
ordered_cards = [r + s for r in ranks for s in suits]

df['Card'] = pd.Categorical(df['NextCard'], categories=ordered_cards, ordered=True)
df = df.sort_values('Card')

# 12分類の一覧
groups = df['Group'].unique()

# ヒートマップを画像で保存
for group in groups:
    group_df = df[df['Group'] == group]

    plt.figure(figsize=(12, 6))
    sns.barplot(data=group_df, x='Card', y='Winrate', palette="viridis")

    plt.title(f'勝率変動ヒートマップ - {group}')
    plt.ylabel('Winrate (%)')
    plt.xlabel('Next Card')
    plt.xticks(rotation=90)
    plt.tight_layout()

    filename = os.path.join(output_dir, f'winrate_heatmap_{group}.png')
    plt.savefig(filename)
    plt.close()

    print(f"{filename} を保存しました。")

print("すべてのヒートマップを保存しました。")
