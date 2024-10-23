import requests
from datetime import datetime, timedelta


date = []
error_msg = "{'error': {'code': 404, 'message': 'Not Found'}}{'error': {'code': 404, 'message': 'Not Found'}}"


match_info_keys = ['match_id', 'home_team', 'away_team', 'year', 'tournament', 'season', 'home_score', 'away_score']
match_info_dict = dict.fromkeys(match_info_keys)
match_info = []

# match_overview_keys = ['match_id',
#                       'home_ball_possession', 'away_ball_possession',
#                       'home_big_chances', 'away_big_chances',
#                       'home_total_shots', 'away_total_shots',
#                       'home_goalkeeper_saves', 'away_goalkeeper_saves',
#                       'home_corner_kicks', 'away_corner_kicks',
#                       'home_fouls', 'away_fouls',
#                       'home_passes', 'away_passes',
#                       'home_tackles', 'away_tackles',
#                       'home_free_kicks', 'away_free_kicks',
#                       'home_yellow_cards', 'away_yellow_cards']
# match_overview_dict = dict.fromkeys(match_overview_keys)
# match_overview = []

shots_keys = ['match_id',
              'home_total_shots', 'away_total_shots',
              'home_shots_on_target', 'away_shots_on_target',
              'home_hit_woodwork', 'away_hit_woodwork',
              'home_shots_off_target', 'away_shots_off_target',
              'home_blocked_shots', 'away_blocked_shots',
              'home_shots_inside_box', 'away_shots_inside_box',
              'home_shots_outside_box', 'away_shots_outside_box']
shots_dict = dict.fromkeys(shots_keys)
shots = []

attack_keys = ['match_id',
               'home_big_chances_scored', 'away_big_chances_scored',
               'home_fouled_final_third', 'away_fouled_final_third',
               'home_offsides', 'away_offsides']
attack_dict = dict.fromkeys(attack_keys)
attack = []

passes_keys = ['match_id',
               'home_accurate_passes', 'away_accurate_passes',
               'home_throw_ins', 'away_throw_ins',
               'home_final_third_entries', 'away_final_third_entries',
               'home_long_balls', 'away_long_balls',
               'home_crosses', 'away_crosses']
passes_dict = dict.fromkeys(passes_keys)
passes = []

duels_keys = ['match_id',
              'home_duels_won_percent', 'away_duels_won_percent',
              'home_dispossessed', 'away_dispossessed',
              'home_ground_duels_percentage', 'away_ground_duels_percentage',
              'home_aerial_duels_percentage', 'away_aerial_duels_percentage',
              'home_dribbles_percentage', 'away_dribbles_percentage']
duels_dict = dict.fromkeys(duels_keys)
duels = []

defending_keys = ['match_id',
                  'home_tackles_won_percent', 'away_tackles_won_percent',
                  'home_total_tackles', 'away_total_tackles',
                  'home_interceptions', 'away_interceptions',
                  'home_recoveries', 'away_recoveries',
                  'home_clearances', 'away_clearances']
defending_dict = dict.fromkeys(defending_keys)
defending = []

goalkeeping_keys = ['match_id',
                    'home_total_saves', 'away_total_saves',
                    'home_goal_kicks', 'away_goal_kicks']
goalkeeping_dict = dict.fromkeys(goalkeeping_keys)
goalkeeping = []


def dates_from_2008():
    start_date = datetime(2008, 1, 1)
    end_date = datetime(2024, 10, 16)

    temp_date = start_date
    while temp_date <= end_date:
        date.append(temp_date.strftime('%Y-%m-%d'))
        temp_date += timedelta(days=1)


print("Gerando datas...")
dates_from_2008()


def get_info_page(date):
    try:
        print("Pagina obtida, salvando...")
        resp = requests.get(f'https://www.sofascore.com/api/v1/sport/football/scheduled-events/{date}')
        # Verifica se o código de status indica sucesso (200 OK)
        if resp.status_code == 200:
            return resp.json()
        else:
            # Se não for sucesso, retorna uma mensagem de erro
            print(f"Erro ao obter página: {resp.status_code}")
            return error_msg
    except Exception as e:
        print(f"Erro ao tentar acessar a página: {e}")
        return error_msg


def get_statistics_page(id):
    try:
        print("Pagina obtida, salvando...")
        resp = requests.get(f'https://www.sofascore.com/api/v1/event/{id}/statistics')
        # Verifica se o código de status indica sucesso (200 OK)
        if resp.status_code == 200:
            return resp.json()
        else:
            # Se não for sucesso, retorna uma mensagem de erro
            print(f"Erro ao obter página: {resp.status_code}")
            return error_msg
    except Exception as e:
        print(f"Erro ao tentar acessar a página: {e}")
        return error_msg


def get_event_info(page):
    for event in page["events"]:
        if page is not None and event['status']['type'] == 'finished':
            id = event['id']

            home_team = event['homeTeam']['name']
            away_team = event['awayTeam']['name']
            year = event['season']['year']
            season = event['season']['name']
            tournament = event['tournament']['name']
            home_score = event['homeScore']['current']
            away_score = event['awayScore']['current']

            match_info_dict['match_id'] = id
            match_info_dict['home_team'] = home_team
            match_info_dict['away_team'] = away_team
            match_info_dict['year'] = year
            match_info_dict['tournament'] = tournament
            match_info_dict['season'] = season
            match_info_dict['home_score'] = home_score
            match_info_dict['away_score'] = away_score

            # print(match_info_dict)
            print('=================================================')
            statistics_page = get_statistics_page(id)
            print(f"ID DA PAGINA: {id}")
            if statistics_page != error_msg:
                get_statistics(statistics_page)
            # print('=========================================================')
            match_info.append(match_info_dict)


def get_statistics(page):
    for category in page['statistics'][0]['groups']:
        print(category['groupName'])


# get_statistics(get_statistics_page(12921285))
print("obtendo id de eventos...")
get_event_info(get_info_page(date[6000]))

