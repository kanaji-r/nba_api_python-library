from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import BoxScoreSummaryV2

# チーム名を指定
team_name = 'Los Angeles Lakers'

# チームIDを取得
team_id = teams.find_teams_by_full_name(team_name)[0]['id']

# 直近過去3試合の試合IDを取得
gamelog = teamgamelog.TeamGameLog(team_id=team_id).get_data_frames()[0]
game_ids = gamelog['Game_ID'].head(3).tolist()

# 試合IDを指定
for game_id in game_ids:

    # BoxScoreSummaryV2を使って試合データを取得
    boxscore_summary = BoxScoreSummaryV2(game_id=game_id).get_data_frames()

    # チーム名を取得
    team_info = boxscore_summary[1]
    team_name_1 = team_info['TEAM_ABBREVIATION'].iloc[0]
    team_name_2 = team_info['TEAM_ABBREVIATION'].iloc[1]

    # 総合得点と各クォーターの得点を取得する
    team_stats = boxscore_summary[5]
    team_score_1 = team_stats['PTS'].iloc[0]
    team_score_2 = team_stats['PTS'].iloc[1]

    q1_score_1 = team_stats['PTS_QTR1'].iloc[0]
    q2_score_1 = team_stats['PTS_QTR2'].iloc[0]
    q3_score_1 = team_stats['PTS_QTR3'].iloc[0]
    q4_score_1 = team_stats['PTS_QTR4'].iloc[0]
    q1_score_2 = team_stats['PTS_QTR1'].iloc[1]
    q2_score_2 = team_stats['PTS_QTR2'].iloc[1]
    q3_score_2 = team_stats['PTS_QTR3'].iloc[1]
    q4_score_2 = team_stats['PTS_QTR4'].iloc[1]

    # オーバータイムのスコアを取得
    if team_stats['PTS_OT1'].iloc[0] == 0:
        print(f'{team_name_1} {team_score_1} - {team_score_2} {team_name_2}')
    else:
        ot_scores = []
        for i in team_stats:
            ot_score_1 = team_stats[f'PTS_OT{i+1}'].iloc[0]
            ot_score_2 = team_stats[f'PTS_OT{i+1}'].iloc[1]
            ot_scores.append(f'OT{i+1}: {ot_score_1}-{ot_score_2}')
        print(f'{team_name_1} {team_score_1} ({", ".join(ot_scores)}) - {team_score_2} {team_name_2}')
    print(f'Q1: {q1_score_1}-{q1_score_2}, Q2: {q2_score_1}-{q2_score_2}, Q3: {q3_score_1}-{q3_score_2}, Q4: {q4_score_1}-{q4_score_2}')