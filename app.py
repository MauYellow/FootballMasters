import requests, time, mysql.connector
from mysql.connector import errorcode
from datetime import datetime, date
from flask import Flask, render_template, redirect, url_for, request
import os
from dotenv import load_dotenv
load_dotenv()

try: 
  cnx = mysql.connector.connect(user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"), 
                              host='127.0.0.1',
                              database=os.getenv("MYSQL_DB"))
  print("MySQL Database connesso correttamente")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()

apifootball_key = os.getenv("apifootball_key")
apifootball_url = os.getenv("apifootball_url") #"https://v3.football.api-sports.io/"
headers = {
    'x-rapidapi-host': apifootball_url,
    'x-rapidapi-key': apifootball_key
    }


app = Flask(__name__, template_folder='templates', static_folder='assets')


oggi = datetime.now()
anno = oggi.year #- 2 # da cambiare
mese = oggi.month
mese = f"{mese:02}"
giorno = oggi.day
ora = oggi.hour
minuto = oggi.minute
current_season = 2024 # Questa deve cambiare automaticamente!
available_fixtures = []

@app.route('/')
def index():
  global current_season
  return render_template('index.html', current_season=current_season)

@app.route('/mai') #**da cancellare
def loading_player_stats():
  current_season = 2024 # Questa la deve cambiare automaticamente!**
  player_id = 129718
  params = {
    "id": player_id, #70100**, #J. Zirkzee, #129718 Bellingham, #276 Neymar, #184 Kane, #627 K Walker, #532 De Ligt, 2935 McGuire, M Mount 19220, 174 Eriksen
    "season": current_season,
  }
  response = requests.get(apifootball_url + "players", headers=headers, params=params)
  response = response.json()
  response = response['response'][0]
  data = response
  #for anno in range(1,5):
  params = {
      "id": player_id,
      "season": current_season - 1
    }
  data_1 = requests.get(apifootball_url + "players", headers=headers, params=params)
  data_1 = data_1.json()
  data_1 = data_1['response'][0]
  params = {
      "id": player_id,
      "season": current_season - 2
  }
  data_2 = requests.get(apifootball_url + "players", headers=headers, params=params)
  data_2 = data_2.json()
  data_2 = data_2['response'][0]
  params = {
      "id": player_id,
      "season": current_season - 3
  }
  data_3 = requests.get(apifootball_url + "players", headers=headers, params=params)
  data_3 = data_3.json()
  data_3 = data_3['response'][0]
  params = {
      "id": player_id,
      "season": current_season - 4
  }
  data_4 = requests.get(apifootball_url + "players", headers=headers, params=params)
  data_4 = data_4.json()
  data_4 = data_4['response'][0]
  #seasons = [str(current_season - i) for i in range(5)]
  return render_template('test_index.html', data=data, data_1=data_1, data_2=data_2, data_3=data_3, data_4=data_4, current_season=current_season) #ho tolto questo, serviva? seasons=seasons, 

@app.route('/player/<int:player_id>')
def player_stats(player_id):
  global current_season
  params = {
        "id": player_id,
        "season": current_season,
    }
  response = requests.get(apifootball_url + "players", headers=headers, params=params)
  response = response.json()
  data = response['response'][0]
  params = {
      "id": player_id,
      "season": current_season - 1
    }
  data_1 = requests.get(apifootball_url + "players", headers=headers, params=params)
  data_1 = data_1.json()
  data_1 = data_1['response'][0]
  params = {
      "id": player_id,
      "season": current_season - 2
  }
  data_2 = requests.get(apifootball_url + "players", headers=headers, params=params)
  data_2 = data_2.json()
  data_2 = data_2['response'][0]
  params = {
      "id": player_id,
      "season": current_season - 3
  }
  data_3 = requests.get(apifootball_url + "players", headers=headers, params=params)
  data_3 = data_3.json()
  data_3 = data_3['response'][0]
  params = {
      "id": player_id,
      "season": current_season - 4
  }
  data_4 = requests.get(apifootball_url + "players", headers=headers, params=params)
  data_4 = data_4.json()
  data_4 = data_4['response'][0]
  print(f"data: {data}")
  print("*******")
  print(f"data_1: {data_1}")

  return render_template("player_stats.html", data=data, data_1=data_1, data_2=data_2, data_3=data_3, data_4=data_4, current_season=current_season) #ho tolto questo, serviva? seasons=seasons, 


@app.route('/team/<int:team_id>/<int:league_id>') #da riaggiungere data_1 data_2 per le statistiche dei giocatori cliccati (?)
def team_stats(team_id, league_id):
  global current_season
  params = {
        "team": team_id, #497 roma da sostituire con team_id,#165 dortmund
        "league": league_id, #135, #Serie A - va messo in automatico e cambiato**
        "season": current_season,
    }
  response = requests.get(apifootball_url + "teams/statistics", headers=headers, params=params)
  response = response.json()
  data_team = response['response']
  print(f"data_team: {data_team}")
  params = {
        "team": team_id, #497 roma da sostituire con team_id, *qui va messo come variabile!
    }
  response = requests.get(apifootball_url + "players/squads", headers=headers, params=params)
  response = response.json()
  squad = response['response']
  return render_template('team_stats.html', squad=squad, data_team=data_team, current_season=current_season)


@app.route('/matches') #** da cancellare
def redirect_to_default():
  return redirect(url_for('get_matches', league_id=135))

@app.route('/widget_test') # **da cancellare
def widget_test():
  print("Widget Test")
  return render_template('widget_test.html')

@app.route('/termini_e_condizioni')
def termini_e_condizioni():
  global current_season
  return render_template('termini_e_condizioni.html', current_season=current_season)
  

@app.route("/leagues.html") #**perché c'è HTML?
def leagues():
    global current_season
    league = request.args.get("league", "default_value")  # Prende il valore dalla URL
    season = request.args.get("season", f"{current_season}")  # Valore di default
    return render_template("leagues.html", league=league, season=season, current_season=current_season)

@app.route("/standings.html") #**Perché c'è HTML?
def standings():
    global current_season
    league = request.args.get("league", "default_value")  # Prende il valore dalla URL
    season = request.args.get("season", f"{current_season}")  # Valore di default
    return render_template("standings.html", league=league, season=season, current_season=current_season)

@app.route('/topscorer/<int:league_id>')
def get_topscorer(league_id):
  global current_season
  params = {
    "league": league_id,
    "season": current_season
  }
  response = requests.get(apifootball_url + "players/topscorers", headers=headers, params=params)
  response = response.json()
  players = response['response']
  return render_template("topscorer.html", players=players, current_season=current_season)

@app.route('/topassists/<int:league_id>')
def get_topassists(league_id):
  global current_season
  params = {
    "league": league_id,
    "season": current_season
  }
  response = requests.get(apifootball_url + "players/topassists", headers=headers, params=params)
  response = response.json()
  players = response['response']
  return render_template("topassists.html", players=players, current_season=current_season)

@app.route('/topyellowcards/<int:league_id>')
def get_topyellowcards(league_id):
  global current_season
  params = {
    "league": league_id,
    "season": current_season
  }
  response = requests.get(apifootball_url + "players/topyellowcards", headers=headers, params=params)
  response = response.json()
  players = response['response']
  return render_template("topyellowcards.html", players=players, current_season=current_season)

@app.route('/topredcards/<int:league_id>')
def get_topredcards(league_id):
  global current_season
  params = {
    "league": league_id,
    "season": current_season
  }
  response = requests.get(apifootball_url + "players/topredcards", headers=headers, params=params)
  response = response.json()
  players = response['response']
  return render_template("topredcards.html", players=players, current_season=current_season)

@app.route('/bookmakers/<int:fixture_id>', endpoint='bookmakers')
def get_odds(fixture_id):
    global current_season
    bookmaker_ids = {
        "BET365": 8,
        "BWIN": 6,
        "BETFAIR": 3
    }

    wanted_ids = {5, 6, 9, 12, 13, 14, 16, 17, 19, 25}
    odds_by_market = {}

    for name, bm_id in bookmaker_ids.items():
        params = {
            "fixture": fixture_id,
            "bookmaker": bm_id
        }
        response = requests.get(apifootball_url + "odds", headers=headers, params=params).json()
        try:
            bets = response['response'][0]['bookmakers'][0]['bets']
        except (IndexError, KeyError):
            continue

        for bet in bets:
            if bet['id'] not in wanted_ids:
                continue

            market = bet['name']
            if market not in odds_by_market:
                odds_by_market[market] = {}

            for val in bet['values']:
                value = val['value']
                odd = val['odd']
                if value not in odds_by_market[market]:
                    odds_by_market[market][value] = {}
                odds_by_market[market][value][name] = odd  # es: odds_by_market['Goals Over/Under']['Over 2.5']['BET365'] = '1.80'

    return render_template('bookmakers.html', odds=odds_by_market, current_season=current_season)



def get_odds(fixture_id):
  global current_season
  params = {
    "fixture": fixture_id,
    "bookmaker": 8 #3 betfair, 6 bwin, 1 10bet, 8 bet365
  }
  response = requests.get(apifootball_url + "odds", headers=headers, params=params)
  response = response.json()
  odds = response['response'][0]['bookmakers'][0]['bets']
  #print(odds)
  #for odd in odds:
  #  print(f"{odd['id']}, {odd['name']}, {odd['values']}")
# parsing della risposta AP
  needed_ids = {17, 16, 12, 13, 14, 19, 9, 6, 5, 25}
  filtered_odds = [bet for bet in odds if bet['id'] in needed_ids]
  print(filtered_odds)
  #print(response)
  return render_template('bookmakers.html', odds=odds, current_season=current_season)
#get_odds(1223969)

@app.route('/matches/<int:league_id>')
def get_matches(league_id):
    global current_season
    print("Apertura pagina /matches")
    available_fixtures = []
    available_matchJSON = []
    selected_date = request.args.get('date', date.today().isoformat())  # Se non specificata, usa oggi 
    params = {
        "date": selected_date,
        "league": league_id,
        "season": current_season #"status": "NS",  # Not Started**
    }
    
    response = requests.get(apifootball_url + "fixtures", headers=headers, params=params)
    response = response.json()
    response = response['response']
    
    for match in response:
        print(f"""
        {match['league']['name']} - {match['fixture']['venue']['name']} a {match['fixture']['venue']['city']}, {match['league']['round']}° giornata.
        {match['teams']['home']['name']} - {match['teams']['away']['name']}
        Id partita: {match['fixture']['id']}, Id campionato: {params['league']}
        """)
        
        # Formattare la data della partita
        match_date = match['fixture']['date']
        formatted_date = datetime.fromisoformat(match_date).strftime('%d %B %Y, %H:%M')
        
        # Aggiungi la data formattata nel JSON
        match['fixture']['formatted_date'] = formatted_date
        
        available_fixtures.append(match['fixture']['id'])
        available_matchJSON.append(match)
        print("---")
    print(f"Fixtures Available: {available_fixtures}")
    #print(f"Available Match JSON: {available_matchJSON}")
    return render_template('matches.html', available_fixtures=available_fixtures, available_matchJSON=available_matchJSON, selected_date=selected_date, current_season=current_season)


@app.route('/prediction/<int:match_id>')
def prediction(match_id):
  global current_season
  params = {
    "fixture": match_id
  }
  response = requests.get(apifootball_url + "predictions", headers=headers, params=params)
  response = response.json()
  response = response['response'][0]
  home_team_id = response['teams']['home']['id']
  away_team_id = response['teams']['away']['id']
  league_id = response['league']['id']
  winner = response['predictions']['winner']['name']
  team_home = response['teams']['home']['name']
  form_home = response['teams']['home']['league']['form']
  flag_home = response['teams']['home']['logo']
  team_away = response['teams']['away']['name']
  form_away = response['teams']['away']['league']['form']
  flag_away = response['teams']['away']['logo']
  comparison_form_home = response['comparison']['form']['home']
  spider_home_lista = [
    int(float(response['comparison']['att']['home'].replace('%', ''))),
    int(float(response['comparison']['def']['home'].replace('%', ''))),
    int(float(response['comparison']['poisson_distribution']['home'].replace('%', ''))),
    int(float(response['comparison']['h2h']['home'].replace('%', ''))),
    int(float(response['comparison']['form']['home'].replace('%', ''))),
    int(float(response['comparison']['total']['home'].replace('%', '')))
]
  spider_away_lista = [
    int(float(response['comparison']['att']['away'].replace('%', ''))),
    int(float(response['comparison']['def']['away'].replace('%', ''))),
    int(float(response['comparison']['poisson_distribution']['away'].replace('%', ''))),
    int(float(response['comparison']['h2h']['away'].replace('%', ''))),
    int(float(response['comparison']['form']['away'].replace('%', ''))),
    int(float(response['comparison']['total']['away'].replace('%', '')))
]
  history_home = response['teams']['home']['league']
  history_away = response['teams']['away']['league']
  prediction = response['predictions']
  precedenti_matchJSON = response['h2h']
  params = {
    "league": league_id,
    "season": current_season,
    "team": home_team_id
  }
  response = requests.get(apifootball_url + "teams/statistics", headers=headers, params=params)
  response = response.json()
  cards_home = response['response']['cards']
  goal_minute_home = response['response']['goals']['for']['minute']
  goal_minute_home_subiti = response['response']['goals']['against']['minute']
  games_played_home = response['response']['fixtures']['played']['total']
  params = {
    "league": league_id,
    "season": current_season,
    "team": away_team_id
  }
  response = requests.get(apifootball_url + "teams/statistics", headers=headers, params=params)
  response = response.json()
  cards_away = response['response']['cards']
  goal_minute_away = response['response']['goals']['for']['minute']
  goal_minute_subiti_away = response['response']['goals']['against']['minute']
  games_played_away = response['response']['fixtures']['played']['total']
  # -- Player Statistics Home -- #
  home_top_players = []
  home_master_stats = {}
  home_tot_yellowcard = 0
  home_tot_fouls = 0
  home_tot_shots = 0
  home_tot_shots_in_goal = 0
  home_tot_saves = 0

  #------Lsta giocatori Attuali
  params = {
        "team": home_team_id, #497 roma da sostituire con team_id, *qui va messo come variabile!
    }
  response = requests.get(apifootball_url + "players/squads", headers=headers, params=params)
  home_current_team = [p['name'] for p in response.json()['response'][0]['players']]
  #print(f"Home Current Team: {home_current_team}")
  params = {
        "team": away_team_id, #497 roma da sostituire con team_id, *qui va messo come variabile!
    }
  response = requests.get(apifootball_url + "players/squads", headers=headers, params=params)
  away_current_team = [p['name'] for p in response.json()['response'][0]['players']]
  #------Fine Lista giocatori Attuali

  params = {
    "season": current_season,
    "team": home_team_id,
    "page": 1
  }
  response = requests.get(apifootball_url + "players", headers=headers, params=params)
  response = response.json()
  #print(f" Response Players: {response}")
  for player in response['response']:
    if player['player']['name'] in home_current_team:
      player_stats = {
      "player_name": player['player']['name'],
      "player_appareances": player['statistics'][0]['games']['appearences'],
      "player_assists": player['statistics'][0]['goals']['assists'],
      "player_photo": player['player']['photo'],
      "player_goal": player['statistics'][0]['goals']['total'] if player['statistics'] else 0,
      "player_chance_score_goal": str(round(((player['statistics'][0]['goals']['total'] if player['statistics'] and player['statistics'][0]['goals']['total'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_assist": player['statistics'][0]['goals']['assists'] if player['statistics'] else 0,
      "player_chance_provide_assist": str(round(((player['statistics'][0]['goals']['assists'] if player['statistics'] and player['statistics'][0]['goals']['assists'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_yellowcard": player['statistics'][0]['cards']['yellow'] if player['statistics'] else 0,
      "player_chance_yellowcard": str(round(((player['statistics'][0]['cards']['yellow'] if player['statistics'] and player['statistics'][0]['cards']['yellow'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_fouls": player['statistics'][0]['fouls']['committed'] if player['statistics'] else 0,
      "player_shots": player['statistics'][0]['shots']['total'] if player['statistics'] else 0,
      "player_shots_in_goal": player['statistics'][0]['shots']['on'] if player['statistics'] else 0,
      "player_saves": player['statistics'][0]['goals']['saves'] if player['statistics'] else 0,

    }
      home_top_players.append(player_stats)
      home_tot_yellowcard = home_tot_yellowcard + (player['statistics'][0]['cards']['yellow'] if player['statistics'] and player['statistics'][0]['cards']['yellow'] is not None else 0)
      home_tot_fouls = home_tot_fouls + (player['statistics'][0]['fouls']['committed'] if player['statistics'] and player['statistics'][0]['fouls']['committed'] is not None else 0)
      home_tot_shots = home_tot_shots + (player['statistics'][0]['shots']['total'] if player['statistics'] and player['statistics'][0]['shots']['total'] is not None else 0)
      home_tot_shots_in_goal = home_tot_shots_in_goal + (player['statistics'][0]['shots']['on'] if player['statistics'] and player['statistics'][0]['shots']['on'] is not None else 0)
      home_tot_saves = home_tot_saves + (player['statistics'][0]['goals']['saves'] if player['statistics'] and player['statistics'][0]['goals']['saves'] is not None else 0)
    #time.sleep(5)
    #print("Attendo 5 secondi")
  for page in range(2, response['paging']['total'] + 1):
    params = {
    "season": current_season,
    "team": home_team_id,
    "page": page
  }
    response = requests.get(apifootball_url + "players", headers=headers, params=params)
    response = response.json()
    
    #print(f"Result Players: {response}")
      #print(f"Pagina: {response}")
    for player in response['response']:
      if player['player']['name'] in home_current_team:
        player_stats = {
      "player_name": player['player']['name'],
      "player_appareances": player['statistics'][0]['games']['appearences'],
      "player_assists": player['statistics'][0]['goals']['assists'],
      "player_photo": player['player']['photo'],
      "player_goal": player['statistics'][0]['goals']['total'] if player['statistics'] else 0,
      "player_chance_score_goal": str(round(((player['statistics'][0]['goals']['total'] if player['statistics'] and player['statistics'][0]['goals']['total'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",      "player_assist": player['statistics'][0]['goals']['assists'] if player['statistics'] else 0,
      "player_chance_provide_assist": str(round(((player['statistics'][0]['goals']['assists'] or 0) / (player['statistics'][0]['games']['appearences'] or 1)) * 100)) + "%" if player['statistics'] else "0%",
      "player_yellowcard": player['statistics'][0]['cards']['yellow'] if player['statistics'] else 0,
      "player_chance_yellowcard": str(round(((player['statistics'][0]['cards']['yellow'] if player['statistics'] and player['statistics'][0]['cards']['yellow'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_fouls": player['statistics'][0]['fouls']['committed'] if player['statistics'] else 0,
      "player_shots": player['statistics'][0]['shots']['total'] if player['statistics'] else 0,
      "player_shots_in_goal": player['statistics'][0]['shots']['on'] if player['statistics'] else 0,
      "player_saves": player['statistics'][0]['goals']['saves'] if player['statistics'] else 0,
    }
        home_top_players.append(player_stats)
        home_tot_yellowcard = home_tot_yellowcard + (player['statistics'][0]['cards']['yellow'] if player['statistics'] and player['statistics'][0]['cards']['yellow'] is not None else 0)
        home_tot_fouls = home_tot_fouls + (player['statistics'][0]['fouls']['committed'] if player['statistics'] and player['statistics'][0]['fouls']['committed'] is not None else 0)
        home_tot_shots = home_tot_shots + (player['statistics'][0]['shots']['total'] if player['statistics'] and player['statistics'][0]['shots']['total'] is not None else 0)
        home_tot_shots_in_goal = home_tot_shots_in_goal + (player['statistics'][0]['shots']['on'] if player['statistics'] and player['statistics'][0]['shots']['on'] is not None else 0)
        home_tot_saves = home_tot_saves + (player['statistics'][0]['goals']['saves'] if player['statistics'] and player['statistics'][0]['goals']['saves'] is not None else 0)
      
      #time.sleep(5)
      #print("Attendo 5 secondi")
    time.sleep(1)
    #print("Sleep 1")
    #print(f"** Home Top Players: {home_top_players}")
  #-- Fill Master_Stats_Home
  #print(f"Home Top Players List: {home_top_players}")
  home_master_stats['tot_yellowcard'] = home_tot_yellowcard
  home_master_stats['tot_yellowcard_per_match'] = round(home_tot_yellowcard / games_played_home, 2) if games_played_home else 0
  home_master_stats['tot_fouls_committed'] = home_tot_fouls
  home_master_stats['tot_fouls_committed_per_match'] = round(home_tot_fouls / games_played_home, 2) if games_played_home else 0
  home_master_stats['tot_shots'] = home_tot_shots
  home_master_stats['tot_shots_per_match'] = round(home_tot_shots / games_played_home, 2) if games_played_home else 0
  home_master_stats['tot_shots_in_goal'] = home_tot_shots_in_goal
  home_master_stats['tot_shots_in_goal_per_match'] = round(home_tot_shots_in_goal / games_played_home, 2) if games_played_home else 0
  home_master_stats['tot_saves'] = home_tot_saves
  home_master_stats['tot_saves_per_match'] = round( home_tot_saves / games_played_home , 2) if games_played_home else 0
  #print(f"**Home_Master_stats: {home_master_stats}")
  #-- Fine Fill Master_Stats_Home

  home_top_players_goal = max(home_top_players, key=lambda p: p["player_goal"] or 0)
  #print(f"home_top_players_goal {home_top_players_goal}")
  home_top_players_assist = max(home_top_players, key=lambda p: p['player_assist'] or 0)
  home_top_players_yellowcard = max(home_top_players, key=lambda p: p['player_yellowcard'] or 0)
  #Player Statistics Away
  away_top_players = []
  away_master_stats = {}
  away_tot_yellowcard = 0
  away_tot_fouls = 0
  away_tot_shots = 0
  away_tot_shots_in_goal = 0
  away_tot_saves = 0
  params = {
    "season": current_season,
    "team": away_team_id,
    "page": 1
  }
  response = requests.get(apifootball_url + "players", headers=headers, params=params)
  response = response.json()
  for player in response['response']:
    if player['player']['name'] in away_current_team:
      player_stats_away = {
      "player_name": player['player']['name'],
      "player_appareances": player['statistics'][0]['games']['appearences'],
      "player_assists": player['statistics'][0]['goals']['assists'],
      "player_photo": player['player']['photo'],
      "player_goal": player['statistics'][0]['goals']['total'] if player['statistics'] else 0,
      "player_chance_score_goal": str(round(((player['statistics'][0]['goals']['total'] if player['statistics'] and player['statistics'][0]['goals']['total'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_assist": player['statistics'][0]['goals']['assists'] if player['statistics'] else 0,
      "player_chance_provide_assist": str(round(((player['statistics'][0]['goals']['assists'] if player['statistics'] and player['statistics'][0]['goals']['assists'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_yellowcard": player['statistics'][0]['cards']['yellow'] if player['statistics'] else 0,
      "player_chance_yellowcard": str(round(((player['statistics'][0]['cards']['yellow'] if player['statistics'] and player['statistics'][0]['cards']['yellow'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_fouls": player['statistics'][0]['fouls']['committed'] if player['statistics'] else 0,
      "player_shots": player['statistics'][0]['shots']['total'] if player['statistics'] else 0,
      "player_shots_in_goal": player['statistics'][0]['shots']['on'] if player['statistics'] else 0,
      "player_saves": player['statistics'][0]['goals']['saves'] if player['statistics'] else 0,
    }
      away_top_players.append(player_stats_away)
      away_tot_yellowcard = away_tot_yellowcard + (player['statistics'][0]['cards']['yellow'] if player['statistics'] and player['statistics'][0]['cards']['yellow'] is not None else 0)
      away_tot_fouls = away_tot_fouls + (player['statistics'][0]['fouls']['committed'] if player['statistics'] and player['statistics'][0]['fouls']['committed'] is not None else 0)
      away_tot_shots = away_tot_shots + (player['statistics'][0]['shots']['total'] if player['statistics'] and player['statistics'][0]['shots']['total'] is not None else 0)
      away_tot_shots_in_goal = away_tot_shots_in_goal + (player['statistics'][0]['shots']['on'] if player['statistics'] and player['statistics'][0]['shots']['on'] is not None else 0)
      away_tot_saves = away_tot_saves + (player['statistics'][0]['goals']['saves'] if player['statistics'] and player['statistics'][0]['goals']['saves'] is not None else 0)
  for page in range(2,response['paging']['total'] + 1):
    params = {
    "season": current_season,
    "team": away_team_id,
    "page": page
  }
    response = requests.get(apifootball_url + "players", headers=headers, params=params)
    response = response.json()
    for player in response['response']:
      if player['player']['name'] in away_current_team:
        player_stats_away = {
      "player_name": player['player']['name'],
      "player_appareances": player['statistics'][0]['games']['appearences'],
      "player_assists": player['statistics'][0]['goals']['assists'],
      "player_photo": player['player']['photo'],
      "player_goal": player['statistics'][0]['goals']['total'] if player['statistics'] else 0,
      "player_chance_score_goal": str(round(((player['statistics'][0]['goals']['total'] if player['statistics'] and player['statistics'][0]['goals']['total'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_assist": player['statistics'][0]['goals']['assists'] if player['statistics'] else 0,
      "player_chance_provide_assist": str(round(((player['statistics'][0]['goals']['assists'] if player['statistics'] and player['statistics'][0]['goals']['assists'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_yellowcard": player['statistics'][0]['cards']['yellow'] if player['statistics'] else 0,
      "player_chance_yellowcard": str(round(((player['statistics'][0]['cards']['yellow'] if player['statistics'] and player['statistics'][0]['cards']['yellow'] is not None else 0) / (player['statistics'][0]['games']['appearences'] if player['statistics'][0]['games']['appearences'] not in [None, 0] else 1)) * 100)) + "%",
      "player_fouls": player['statistics'][0]['fouls']['committed'] if player['statistics'] else 0,
      "player_shots": player['statistics'][0]['shots']['total'] if player['statistics'] else 0,
      "player_shots_in_goal": player['statistics'][0]['shots']['on'] if player['statistics'] else 0,
      "player_saves": player['statistics'][0]['goals']['saves'] if player['statistics'] else 0,
      }
        away_top_players.append(player_stats_away)
        away_tot_yellowcard = away_tot_yellowcard + (player['statistics'][0]['cards']['yellow'] if player['statistics'] and player['statistics'][0]['cards']['yellow'] is not None else 0)
        away_tot_fouls = away_tot_fouls + (player['statistics'][0]['fouls']['committed'] if player['statistics'] and player['statistics'][0]['fouls']['committed'] is not None else 0)
        away_tot_shots = away_tot_shots + (player['statistics'][0]['shots']['total'] if player['statistics'] and player['statistics'][0]['shots']['total'] is not None else 0)
        away_tot_shots_in_goal = away_tot_shots_in_goal + (player['statistics'][0]['shots']['on'] if player['statistics'] and player['statistics'][0]['shots']['on'] is not None else 0)
        away_tot_saves = away_tot_saves + (player['statistics'][0]['goals']['saves'] if player['statistics'] and player['statistics'][0]['goals']['saves'] is not None else 0)

  away_top_players_goal = max(away_top_players, key=lambda p: p["player_goal"] or 0)
  away_top_players_assist = max(away_top_players, key=lambda p: p['player_assist'] or 0)
  away_top_players_yellowcard = max(away_top_players, key=lambda p: p['player_yellowcard'] or 0)

  away_master_stats['tot_yellowcard'] = away_tot_yellowcard
  away_master_stats['tot_yellowcard_per_match'] = round(away_tot_yellowcard / games_played_away, 2) if games_played_away else 0
  away_master_stats['tot_fouls_committed'] = away_tot_fouls
  away_master_stats['tot_fouls_committed_per_match'] = round(away_tot_fouls / games_played_away, 2) if games_played_away else 0
  away_master_stats['tot_shots'] = away_tot_shots
  away_master_stats['tot_shots_per_match'] = round(away_tot_shots / games_played_away, 2) if games_played_away else 0
  away_master_stats['tot_shots_in_goal'] = away_tot_shots_in_goal
  away_master_stats['tot_shots_in_goal_per_match'] = round(away_tot_shots_in_goal / games_played_away, 2) if games_played_away else 0
  away_master_stats['tot_saves'] = away_tot_saves
  away_master_stats['tot_saves_per_match'] = round( away_tot_saves / games_played_away , 2) if games_played_away else 0
  
  print(f"Away_Master_Stats: {away_master_stats}")
  
  #Studio Ultimo Scontro Diretto
  params = {
      "fixture": precedenti_matchJSON[0]['fixture']['id']
    }
  response = requests.get(apifootball_url + "fixtures/statistics", headers=headers, params=params)
  response = response.json()
  response = response['response']
  last_match = response
  #print(f"Last_Match: {last_match}")
  return render_template('prediction.html', current_season=current_season, league_id=league_id, home_team_id=home_team_id, away_team_id=away_team_id, away_master_stats=away_master_stats, last_match=last_match, cards_away=cards_away, cards_home=cards_home, match_id=match_id, home_master_stats=home_master_stats, away_top_players_yellowcard=away_top_players_yellowcard, away_top_players_goal=away_top_players_goal, away_top_players_assist=away_top_players_assist, home_top_players_yellowcard=home_top_players_yellowcard, home_top_players_goal=home_top_players_goal, home_top_players_assist=home_top_players_assist, winner=winner, team_home=team_home, form_home=form_home, flag_home=flag_home, team_away=team_away, form_away=form_away, flag_away=flag_away, comparison_form_home=comparison_form_home, spider_home_lista=spider_home_lista, spider_away_lista=spider_away_lista, history_home=history_home, history_away=history_away, prediction=prediction, precedenti_matchJSON=precedenti_matchJSON, goal_minute_home=goal_minute_home, goal_minute_away=goal_minute_away, goal_minute_home_subiti=goal_minute_home_subiti, goal_minute_subiti_away=goal_minute_subiti_away)


def get_updates():
  response = requests.get(f"https://api.telegram.org/bot{botkey}/getUpdates")
  if response.status_code == 200:
    updates = response.json()
    print("Aggiornamenti ricevuti:", updates)
  else:
    print(f"Errore nel recupero degli aggiornamenti. Status code: {response.status_code}")
    print(response.text)


def get_fixtures():
  global current_season
  #leggi bene qui ler funzioni "all" e "live", possono essere utili per ridurre le chiamate API -> https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures
  #si possono prendere anche i colori delle bandiere della liga
  #si possono prendere anche le bandiere delle squadre
  available_fixtures = []
  params = {
    "date": f"{anno}-{mese}-{giorno}",
    "league": 135, #203(turca), #39 (premier league), #135, (italia)
    "season": current_season,
    "status": "NS",
  }
  response = requests.get(apifootball_url + "fixtures", headers=headers, params=params)
  response = response.json()
  response = response['response']
  for match in response:
    print(f"""
    {match['league']['name']} - {match['fixture']['venue']['name']} a {match['fixture']['venue']['city']}, {match['league']['round']}° giornata.
    {match['teams']['home']['name']} - {match['teams']['away']['name']}
    Id partita: {match['fixture']['id']}, Id campionato: {params['league']}
    """)
    available_fixtures.append(match['fixture']['id'])
    print("---")
  print(f"Fixtures Available: {available_fixtures}")
  return available_fixtures

def get_api_status():
  try:
    response = requests.get(url=apifootball_url + "status", headers=headers)
    response = response.json()
    print(f"{response}")
    print(f"Limite API calls: {response['response']['requests']['current']}/{response['response']['requests']['limit_day']}")
  except TypeError as e:
    print(f"*** Error Limite API calls: {e}")
  #print(response[0])

def get_countries():
  params = { "name": "Italy" }
  response = requests.get(apifootball_url + "countries", headers=headers, params=params)
  response = response.json()
  print(f"Paese scelto: {response['response'][0]['name']}, codice: {response['response'][0]['code']}, bandiera: {response['response'][0]['flag']}")
  
def get_league_info():
  params = { "id": "135" } #135 è italia
  response = requests.get(apifootball_url + "leagues", headers=headers, params=params)
  response = response.json()
  print(f"Info Competizione: {response['response'][0]['league']['name']}")

def get_fixture_lineup():
  #puoi anche prendere i colori del portiere e dei giocatori
  for fixture in available_fixtures:
    params = {
    "fixture": f"{fixture}",
    }
    try:
      response = requests.get(apifootball_url + "fixtures/lineups", headers=headers, params=params)
      response = response.json()
      response = response['response']
      for team in range(0,1):
      #print(response)
        print(f"""
{response[team]['team']['name']}, Formazione {response[team]['formation']}
{response[team]['startXI'][0]['player']['number']}. {response[team]['startXI'][0]['player']['name']}
{response[team]['startXI'][1]['player']['number']}. {response[team]['startXI'][1]['player']['name']}
{response[team]['startXI'][2]['player']['number']}. {response[team]['startXI'][2]['player']['name']}
{response[team]['startXI'][3]['player']['number']}. {response[team]['startXI'][3]['player']['name']}
{response[team]['startXI'][4]['player']['number']}. {response[team]['startXI'][4]['player']['name']}
{response[team]['startXI'][5]['player']['number']}. {response[team]['startXI'][5]['player']['name']}
{response[team]['startXI'][6]['player']['number']}. {response[team]['startXI'][6]['player']['name']}
{response[team]['startXI'][7]['player']['number']}. {response[team]['startXI'][7]['player']['name']}
{response[team]['startXI'][8]['player']['number']}. {response[team]['startXI'][8]['player']['name']}
{response[team]['startXI'][9]['player']['number']}. {response[team]['startXI'][9]['player']['name']}
{response[team]['startXI'][10]['player']['number']}. {response[team]['startXI'][10]['player']['name']}
          """)
    except IndexError as Exception:
      print("Formazione ancora non disponibile, le formazioni ufficiali sono disponibili 20-40 minuti prima del match")

def get_fixture_injuries():
  #è possibile anche prendere quelli di tutta la league
  #è possibile prendere anche la foto dell'infortunato
  for fixture in available_fixtures:
    params = {
    "fixture": fixture,
    }
    response = requests.get(apifootball_url + "injuries", headers=headers, params=params)
    response = response.json()
    response = response['response']
    for player in response:
      print(f"Infortunato: {player['player']['name']} ({player['team']['name']}) per {player['player']['reason']}")
      print("---")

def get_h2h():
  #con la chiamata fixtures/statistics è possibile vedere le statistiche degli scontri diretti scorsi (tiri, dribbling, gol, possesso, ecc..) e fare una media?
  global current_season
  params= {
    "h2h": "33-34",
    "last": 2,
    #"next": 1,
    #"status": "NS"
  }
  response = requests.get(apifootball_url + "fixtures/headtohead", headers=headers, params=params)
  response = response.json()
  response = response['response']
  print(f"Ultime {params['last']} partite:")
  for h2h in response:
    print(f"""
{h2h['fixture']['venue']['name']}, {h2h['league']['name']} {h2h['league']['season']}
{h2h['teams']['home']['name']} - {h2h['teams']['away']['name']}  {h2h['score']['fulltime']['home']}-{h2h['score']['fulltime']['away']}
""")


time.sleep(1)
get_api_status()

if __name__ == '__main__':
    app.run(debug=True) #True per fare le modifiche sul sito automaticamente