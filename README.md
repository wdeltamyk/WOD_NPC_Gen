# Character Generators README

## Overview
This project includes character generators for three different supernatural and human types from the 5th Edition: Vampires, Werewolves, and Humans (specifically Hunters). The programs for each character type are placed in their respective folders:

- **Vampires**
- **Humans_Hunters**
- **Werewolves**

Each character generator uses the Behind the Name API to generate character names. Users must replace the placeholder "apikeyhere" in the `.env` file in each folder with their own API key from [Behind the Name](https://www.behindthename.com/). Note that each generator runs independently, to avoid conflicts in the JSON files used by each character type.

## Installation and Setup

1. **Dependencies**: Make sure to install all necessary Python packages listed in `requirements.txt`. These include, but are not limited to:
   - `tkinter` for GUI elements
   - `requests` for API calls
   - `python-dotenv` for managing API keys

2. **API Key Setup**: You must provide an API key to enable name generation. To do this:
   - Navigate to each character type's folder (e.g., `Vampires`, `Humans_Hunters`, `Werewolves`).
   - Edit the `.env` file to replace `apikeyhere` with your Behind the Name API key.

3. **Running the Program**:
   - Each character generator has its own script, named accordingly (e.g., `npcgenvampire.py`, `npcgengarou.py`, `npcgenhuman.py`). Run the desired generator with Python:
     ```
     python <script_name>.py
     ```

## Features

### Common Features
- **Name Generation**: Uses the Behind the Name API to generate character names based on user-specified cultural backgrounds.
- **Attributes and Skills**: Randomly assigns attributes and skills using values from JSON files. The attribute categories include Physical, Social, and Mental.
- **Importance Levels**: Allows users to select a character's importance level (e.g., Cub, Cliath, Fostern for Werewolves; Thug, Minor, Boss for Humans and Vampires), which influences the character's attributes and abilities.
- **Customisation Options**: Allows selection of specific characteristics such as Clan, Sect, Creed, Tribe, or Auspice depending on the character type.

### Vampires (VTM V5)
- Supports clan selection, including classic clans like **Brujah**, **Nosferatu**, and **Toreador**.
- Features blood potency calculations and disciplines generation based on selected clan.
- Includes diablerie as an option, although this feature will be removed in future versions.

### Humans (Hunters)
- Supports **Creed** and **Drive** selection, such as **Judge** or **Avenger**.
- Incorporates attributes, skills, edges and perks, merits and flaws, and safe house generation.

### Werewolves
- Supports **Auspice**, **Tribe**, and **Breed** selections, including choices like **Theurge**, **Fianna**, and **Lupus**.
- Includes the ability to generate character-specific talismans, caerns, and gifts.

## Acknowledgements
A special acknowledgement goes to **Daelso**, the creator of [SchreckNet.live](https://schrecknet.live), who provided the JSON files that formed the foundation for this program. Although this project is not a direct fork of SchreckNet, it owes its existence to the JSON data provided by Daelso.

## License
This project is licensed under the **Apache 2.0 License**. You are free to use, modify, and distribute the software as you wish. Please see the `LICENSE` file for more information.

## Notes
- **Creative Liberties**: Some creative liberties have been taken in adapting the JSON files into character generators. These may not be strictly faithful to 5th Edition rules but serve to enhance the character generation experience.


