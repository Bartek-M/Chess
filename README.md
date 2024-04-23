# Chess

Multiplayer **Chess** game created using **Python**. It uses **pygame** for UI and game play with **socket** server to handle connections and game management. It supports independent clients on different machines on different networks.

> If you find any bugs, feel free to create a new **issue** on this repository.

## Requirements 
- Python 3.8 or above

## Setup
Install required dependencies
```bash
pip install -r requirements.txt
```

> **NOTE:** This app needs `.env` configuration file. Using `.env.example` create `.env` file and change it according to your needs. Without this, application may not work properly. 

## Running
```bash
python main.py
python server.py
```

## Usage
**CTRL + Q**<br>
Leave current game

**Game Codes**<br>
Unique codes for joining existing games, which are in the waiting queue or not yet started.

- If no game is found and there are any waiting games, player will join the oldest.
- If no game is found and there aren't any waiting games, new public game will be created.
- If game code was set as **new**, new private game will be created.

**Public / Private Games**
- Public games are put into the waiting queue and everyone can join them.
- Private game are not put into the waiting queue and only players with correct codes can join them. 

> **NOTE:** Player name and game code are only used for multiplayer games and do not affect local gameplay. 

## License
NOT FOR COMMERCIAL USE 

> If you intend to use any of my code, for commercial use, please contact me and get my permission.