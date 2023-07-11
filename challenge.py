from db import database
from elosports.elo import Elo

def get_author_elo(author):
    db = database()
    query = ("SELECT author_elo FROM author WHERE author_id = %s")
    output = db.execute(query, [author])
    return output

def update_author_elo(author, elo):
    db = database()
    query = ("UPDATE author SET author_elo = %s WHERE author_id = %s")
    db.execute(query, [author, elo], expectoutput=False)

def get_challenge():
    db = database()
    result = db.get_random(2)
    return result

def process_result(winner, loser):
    eloLeague = Elo(k = 20)
    winner_elo = get_author_elo(winner)[0][0]
    loser_elo = get_author_elo(loser)[0][0]
    eloLeague.addPlayer(winner, rating = winner_elo)
    eloLeague.addPlayer(loser, rating = loser_elo)
    eloLeague.gameOver(winner = winner, loser = loser, winnerHome=0)
    new_winner_elo = int(eloLeague.ratingDict[winner])
    new_loser_elo = int(eloLeague.ratingDict[loser])
    update_author_elo(winner, new_winner_elo)
    update_author_elo(loser, new_loser_elo)
    return f"Winner {winner} updates elo from {winner_elo} to {new_winner_elo}. Loser {loser} updates elo from {loser_elo} to {new_loser_elo}"