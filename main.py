import json
from fastapi import FastAPI, HTTPException, Query, exceptions, Path
from pydantic import BaseModel
from typing import Optional 

app = FastAPI()

class anime_info(BaseModel):
    anime_id: Optional[int] = None
    anime_name: str
    anime_main: str
    anime_status: str

class GameInfo(BaseModel):
    game_id: Optional[int] = None
    game_name: str
    game_type: str
    game_rat: float

    
    
    
with open("anime.json", 'r') as f:
    anime = json.load(f)
    
    
@app.get('/view', status_code=200)
def view_anime():
    return(anime)

@app.get('/animes/{a_id}', status_code=200)
def get_anime(a_id: int):
    animes = [a for a in anime if a['anime_id'] == a_id]
    return animes[0] if len(animes) > 0 else {}

@app.post('/addAnime', status_code=201)
def add_anime(animes: anime_info):
    nanime_id = max([a['anime_id'] for a in anime]) +1
    new_anime = {
        "anime_id": nanime_id,
        "anime_name": animes.anime_name,
        "anime_main": animes.anime_main,
        "anime_status": animes.anime_status
            }
    
    anime.append(new_anime)
    
    with open('anime.json', 'w') as f:
        json.dump(anime, f)
        
    return new_anime
    
@app.put('/changeanime', status_code=200)
def change_anime(animes: anime_info):
    """
    PUT endpoint to update an existing anime by ID.
    """
    anime_id = animes.anime_id
    
    anime_index = None
    for i, a in enumerate(anime):
        if a['anime_id'] == anime_id:
            anime_index = i
            break

    if anime_index is not None:
        anime[anime_index]["anime_name"] = animes.anime_name
        anime[anime_index]["anime_main"] = animes.anime_main
        anime[anime_index]["anime_status"] = animes.anime_status

        with open('anime.json', 'w') as f:
            json.dump(anime, f)

        return anime[anime_index]
    else:
        raise HTTPException(status_code=404, detail=f"Anime with id {anime_id} does not exist")
    
@app.delete('/deleteAnime/{a_id}', status_code=204)  
def delete_anime(a_id: int):
    global anime  # Use the global keyword to access the outer scope variable

    # Find the index of the anime with the specified anime_id
    anime_index = None
    for i, a in enumerate(anime):
        if a['anime_id'] == a_id:
            anime_index = i
            break

    if anime_index is not None:
        # Remove the anime with the specified anime_id
        del anime[anime_index]
        
        # Write the changes back to the JSON file
        with open('anime.json', 'w') as f:
            json.dump(anime, f)
    else:
        raise HTTPException(status_code=404, detail=f"There is no anime with the id number {a_id}")
    
    
    
    
    
    
#This for games function

# Load existing data from the JSON file
with open("game.json", 'r') as file:
    json_data = json.load(file)

# Access the "game" key in the JSON object
game = json_data if isinstance(json_data, list) else json_data.get("game", [])


@app.get('/viewGame', status_code=200)
def view_game():
    return game

@app.get('/games/{g_id}', status_code=200)
def get_game(g_id: int):
    print(f"Looking for game with ID: {g_id}")

    if not game:
        print("Game list is empty!")
        return {}

    games = [g for g in game if g['game_id'] == g_id]

    if len(games) > 0:
        print(f"Found game: {games[0]}")
        return games[0]
    else:
        print("Game not found!")
        return {}

@app.post('/addGame', status_code=201)
def add_game(games: GameInfo):
    ngame_id = max([g['game_id'] for g in game]) + 1
    new_game = {
        "game_id": ngame_id,
        "game_name": games.game_name,
        "game_type": games.game_type,
        "game_rat": games.game_rat
    }

    game.append(new_game)

    with open('game.json', 'w') as file:
        json.dump(game, file)

    return new_game

@app.put('/changeGame', status_code=200)
def change_game(games: GameInfo):
    """
    PUT endpoint to update an existing game by ID.
    """
    game_id = games.game_id
    
    game_index = None
    for i, g in enumerate(game):
        if g['game_id'] == game_id:
            game_index = i
            break

    if game_index is not None:
        game[game_index]["game_name"] = games.game_name
        game[game_index]["game_type"] = games.game_type
        game[game_index]["game_rat"] = games.game_rat

        with open('game.json', 'w') as file:
            json.dump(game, file)

        return game[game_index]
    else:
        raise HTTPException(status_code=404, detail=f"Game with id {game_id} does not exist")

@app.delete('/deleteGame/{g_id}', status_code=204)
def delete_game(g_id: int):
    global game  # Use the global keyword to access the outer scope variable

    # Find the index of the game with the specified game_id
    game_index = None
    for i, g in enumerate(game):
        if g['game_id'] == g_id:
            game_index = i
            break

    if game_index is not None:
        # Remove the game with the specified game_id
        del game[game_index]
        
        # Write the changes back to the JSON file
        with open('game.json', 'w') as file:
            json.dump(game, file)
    else:
        raise HTTPException(status_code=404, detail=f"There is no game with the id number {g_id}")

