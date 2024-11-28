import json
import requests
import os

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from websocket import create_connection

load_dotenv()

def showdown_login():
    username = os.environ.get("SHOWDOWN_USER_NAME")
    password = os.environ.get("SHOWDOWN_PASSWORD")
    ws = create_connection("wss://sim3.psim.us/showdown/websocket")

    ws.recv()
    challenge_str = ws.recv()[10:]

    response = requests.post("https://play.pokemonshowdown.com/api/login",
                             f"name={username}&pass={password}&challstr={challenge_str}")
    assertion = json.loads(response.text[1:])["assertion"]

    ws.send(f"|/trn ProfOakBotHelios,0,{assertion}")

    ws.recv()
    ws.recv()
    return ws

def showdown_search_pokemon(user_input : str):
    ws = showdown_login()
    ws.send(f"|/nds !weak normal | cap, fe, all, bst desc, {user_input}")
    ws.recv()
    reply = ws.recv()
    if "/error" in reply:
        return reply.split("/error ", 1)[1]
    html = reply.split("/raw ")[1]
    soup = BeautifulSoup(html, 'html.parser')
    pokemon_names = []
    for psicon in soup.find_all("psicon"):
        pokemon_name = psicon["pokemon"]
        if pokemon_name not in ["Smeargle","Necturna"]:
            pokemon_names.append(pokemon_name)

    return pokemon_names


def showdown_search_moves(user_input : str):
    ws = showdown_login()
    ws.send(f"|/nms {user_input}")
    ws.recv()
    reply = ws.recv()
    if "/error" in reply:
        return reply.split("/error ", 1)[1]
    html = reply.split("/raw ")[1]
    soup = BeautifulSoup(html, 'html.parser')
    moves = []
    for move_link in soup.find_all("a"):
        move = move_link.text
        moves.append(move)

    return moves