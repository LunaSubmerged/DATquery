import json
import requests
import os

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from websocket import create_connection

load_dotenv()

def showdown_search(username : str, password : str, userinput : str):

    ws = create_connection("wss://sim3.psim.us/showdown/websocket")

    ws.recv()
    challengeStr = ws.recv()[10:]

    response = requests.post("https://play.pokemonshowdown.com/api/login", f"name={username}&pass={password}&challstr={challengeStr}")
    assertion = json.loads(response.text[1:])["assertion"]

    ws.send(f"|/trn ProfOakBotHelios,0,{assertion}")

    ws.recv()
    ws.recv()

    ws.send(f"|/nds !weak normal | cap, fe, all, bst desc, {userinput}")

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