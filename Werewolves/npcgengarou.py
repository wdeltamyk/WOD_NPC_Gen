import tkinter as tk
from tkinter import ttk
import random
import requests
import os
from dotenv import load_dotenv
import threading
import time
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WerewolfCharacterGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Werewolf Character Generator")
        master.geometry("600x800")

        # Load JSON data
        self.load_json_data()

        # Create and set up the GUI elements
        self.setup_gui()

    # Validate before loading json values
    def validate_json_data(self):
        if "Attributes" not in self.attributes_data:
            raise KeyError("'Attributes' key not found in attributes data")
        if "skills" not in self.skills_data:
            raise KeyError("'skills' key not found in skills data")
        if "Caern" not in self.caerns_data:
            raise KeyError("'Caern' key not found in caerns data")
        if "Talismans" not in self.talismans_data:
            raise KeyError("'Talismans' key not found in talismans data")
        if "Merits" not in self.merits_data:
            raise KeyError("'Merits' key not found in merits data")
        if "Backgrounds" not in self.backgrounds_data:
            raise KeyError("'Backgrounds' key not found in backgrounds data")

    def load_json_data(self):
        try:
            with open('5eAttributes.json') as f:
                self.attributes_data = json.load(f)
            with open('5eSkills.json') as f:
                self.skills_data = json.load(f)
            with open('5eCaerns.json') as f:
                self.caerns_data = json.load(f)
            with open('5eTalismans.json') as f:
                self.talismans_data = json.load(f)
            with open('5eMerits.json') as f:
                self.merits_data = json.load(f)
            with open('5eBackgrounds.json') as f:
                self.backgrounds_data = json.load(f)
        except FileNotFoundError as e:
            logging.error(f"JSON file not found: {e.filename}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON file: {e.msg}")
            raise

        # Create a dictionary to categorize attributes
        self.attribute_categories = {
            "Physical": self.attributes_data["Attributes"][:3],
            "Social": self.attributes_data["Attributes"][3:6],
            "Mental": self.attributes_data["Attributes"][6:]
        }

        # Validate the JSON data structure
        self.validate_json_data()

    def setup_gui(self):
        # Auspice
        ttk.Label(self.master, text="Auspice:").grid(row=0, column=0, sticky="w")
        self.auspice = ttk.Combobox(self.master, values=["Ragabash", "Theurge", "Philodox", "Galliard", "Ahroun"])
        self.auspice.grid(row=0, column=1)

        # Tribe
        ttk.Label(self.master, text="Tribe:").grid(row=1, column=0, sticky="w")
        self.tribe = ttk.Combobox(self.master, values=[
            "Black Furies", "Bone Gnawers", "Children of Gaia", "Fianna", "Get of Fenris", "Glass Walkers",
            "Red Talons", "Shadow Lords", "Silent Striders", "Silver Fangs", "Uktena", "Wendigo"
        ])
        self.tribe.grid(row=1, column=1)

        # Breed
        ttk.Label(self.master, text="Breed:").grid(row=2, column=0, sticky="w")
        self.breed = ttk.Combobox(self.master, values=["Homid", "Metis", "Lupus"])
        self.breed.grid(row=2, column=1)

        # Skill Focus (Multiple Selection)
        ttk.Label(self.master, text="Skill Focus:").grid(row=3, column=0, sticky="w")
        self.skill_focus = tk.Listbox(self.master, selectmode=tk.MULTIPLE, exportselection=0)
        for idx, focus in enumerate(["Physical", "Social", "Mental"]):
            self.skill_focus.insert(idx, focus)
        self.skill_focus.grid(row=3, column=1)

        # NPC Importance
        ttk.Label(self.master, text="NPC Importance:").grid(row=4, column=0, sticky="w")
        self.importance = ttk.Combobox(self.master, values=["Cub", "Cliath", "Fostern", "Adren", "Athro", "Elder", "Legendary"])
        self.importance.grid(row=4, column=1)

        # Culture (for name generation)
        ttk.Label(self.master, text="Culture:").grid(row=8, column=0, sticky="w")
        self.culture = ttk.Combobox(self.master, values=[
            "New World Mythology", "Ancient Celtic", "Celtic Mythology", "Ancient Egyptian", "Egyptian Mythology", "Anglo-Saxon", "Ancient Germanic", "Ancient Greek", "Greek Mythology", "Hindu Mythology", "Arthurian Romance", "Ancient Near Eastern", "Near Eastern Mythology", "Ancient Roman", "Roman Mythology", "Ancient Scandinavian", "Norse Mythology", "Slavic Mythology", "African", "Afrikaans", "Akan", "Albanian", "Algonquin", "American", "Amharic", "Apache", "Arabic", "Armenian", "Assamese", "Asturian", "Avar", "Aymara", "Azerbaijani", "Balinese", "Bashkir", "Basque", "Belarusian", "Bengali", "Berber", "Bhutanese", "Bosnian", "Breton", "Bulgarian", "Burmese", "Catalan", "Chamorro", "Chechen", "Cherokee", "Chewa", "Cheyenne", "Chinese", "Choctaw", "Circassian", "Comanche", "Comorian", "Cornish", "Corsican", "Cree", "Croatian", "Czech", "Dagestani", "Danish", "Dargin", "Dhivehi", "Dutch", "English", "Esperanto", "Estonian", "Ethiopian", "Ewe", "Gluttakh", "Monstrall", "Orinami", "Romanto", "Simitiq", "Tsang", "Xalaxxi", "Faroese", "Fijian", "Filipino", "Finnish", "Flemish", "French", "Frisian", "Fula", "Ga", "Galician", "Ganda", "Georgian", "German", "Greek", "Greenlandic", "Guarani", "Gujarati", "Hausa", "Hawaiian", "Hindi", "Hmong", "Hungarian", "Ibibio", "Icelandic", "Igbo", "Indian", "Indonesian", "Ingush", "Inuit", "Irish", "Iroquois", "Italian", "Japanese", "Javanese", "Jèrriais", "Kannada", "Kazakh", "Khmer", "Kiga", "Kikuyu", "Kongo", "Korean", "Kurdish", "Kyrgyz", "Lao", "Latvian", "Limburgish", "Lithuanian", "Luhya", "Luo", "Macedonian", "Maguindanao", "Malay", "Malayalam", "Maltese", "Manx", "Maori", "Mapuche", "Marathi", "Mayan", "Mbundu", "Mongolian", "Mwera", "Nahuatl", "Navajo", "Ndebele", "Nepali", "Norman", "Norwegian", "Nuu-chah-nulth", "Occitan", "Odia", "Ojibwe", "Oneida", "Oromo", "Ossetian", "Pashto", "Persian", "Picard", "Pintupi", "Polish", "Portuguese", "Powhatan", "Punjabi", "Quechua", "Rapa Nui", "Romanian", "Russian", "Sami", "Samoan", "Sardinian", "Scots", "Scottish", "Seneca", "Serbian", "Shawnee", "Shona", "Siksika", "Sinhalese", "Sioux", "Slovak", "Slovene", "Somali", "Sorbian", "Sotho", "Spanish", "Sundanese", "Swahili", "Swazi", "Swedish", "Tagalog", "Tahitian", "Tajik", "Tamil", "Tatar", "Tausug", "Telugu", "Thai", "Sicilian", "Pet", "Indigenous American", "Coptic", "Hebrew", "Jewish", "Slavic", "Indigenous Australian", "Mohawk", "Low German", "History", "Theology", "Various", "Mythology", "Biblical (All)", "Mormon", "Astronomy", "Literature", "Popular Culture", "Medieval", "Ancient", "Tibetan", "Tongan", "Tooro", "Tswana", "Tuareg", "Tumbuka", "Tupi", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Urhobo", "Uyghur", "Uzbek", "Vietnamese", "Walloon", "Welsh", "Xhosa", "Yao", "Yolngu", "Yoruba", "Zapotec", "Zulu"
        ])
        self.culture.grid(row=9, column=1)

        # Generate button
        self.generate_button = ttk.Button(self.master, text="Generate Character", command=self.generate_character)
        self.generate_button.grid(row=6, column=0, columnspan=2)

        # Result display with scrollbar
        self.result_frame = ttk.Frame(self.master)
        self.result_frame.grid(row=7, column=0, columnspan=2)
        self.result_text = tk.Text(self.result_frame, height=25, width=70)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar = ttk.Scrollbar(self.result_frame, command=self.result_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=self.scrollbar.set)

    def generate_character(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Generating character...")
        self.generate_button.config(state="disabled")

        auspice = self.auspice.get()
        tribe = self.tribe.get()
        breed = self.breed.get()

        # Get selected skill focuses
        selected_indices = self.skill_focus.curselection()
        skill_focus = [self.skill_focus.get(i) for i in selected_indices]
        if not skill_focus:
            # Default to all focuses if none selected
            skill_focus = ["Physical", "Social", "Mental"]

        importance = self.importance.get()
        culture = self.culture.get()

        # Increase timeout to 60 seconds
        timer = threading.Timer(60.0, self.generation_timeout)
        timer.start()

        thread = threading.Thread(target=self.threaded_character_generation,
                                  args=(auspice, tribe, breed, skill_focus, importance, culture, timer))
        thread.start()

    def generation_timeout(self):
        logging.error("Character generation timed out")
        self.master.after(0, self.update_gui_with_error, "Character generation timed out")

    def threaded_character_generation(self, auspice, tribe, breed, skill_focus, importance, culture, timer):
        try:
            logging.info("Starting character generation")

            logging.info("Generating name")
            name = self.generate_name(culture)
            logging.info(f"Name generated: {name}")

            logging.info("Starting character creation")
            character = {
                "Name": name,
                "Breed": breed,
                "Auspice": auspice,
                "Tribe": tribe
            }

            logging.info("Generating attributes")
            character["Attributes"] = self.generate_attributes(skill_focus, importance)
            logging.info("Attributes generated")

            logging.info("Generating skills")
            character["Skills"] = self.generate_skills(skill_focus, importance)
            logging.info("Skills generated")

            logging.info("Generating gifts")
            character["Gifts"] = self.generate_gifts(auspice, tribe, breed, importance)
            logging.info("Gifts generated")

            logging.info("Generating merits and flaws")
            character["Merits and Flaws"] = self.generate_merits_and_flaws(importance)
            logging.info("Merits and Flaws generated")

            logging.info("Generating backgrounds")
            character["Backgrounds"] = self.generate_backgrounds(importance)
            logging.info("Backgrounds generated")

            logging.info("Generating talismans")
            character["Talismans"] = self.generate_talismans(importance)
            logging.info("Talismans generated")

            logging.info("Generating caern")
            character["Caern"] = self.generate_caern(importance)
            logging.info("Caern generated")

            logging.info("Character creation completed")
            timer.cancel()
            self.master.after(0, self.update_gui_with_character, character)
        except Exception as e:
            logging.error(f"Error in character generation: {str(e)}")
            logging.exception("Exception details:")
            timer.cancel()
            self.master.after(0, self.update_gui_with_error, str(e))

    def update_gui_with_character(self, character):
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        # Display results
        self.result_text.insert(tk.END, self.format_character(character))
        self.generate_button.config(state="normal")  # Re-enable the button

    def update_gui_with_error(self, error_message):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Error generating character: {error_message}")
        self.generate_button.config(state="normal")  # Re-enable the button

    def generate_name(self, culture):
        logging.info(f"Generating name for culture: {culture}")
        try:
            name = self.get_name_from_api(culture)
            if name == "Name generation failed":
                raise ValueError("Name generation failed")
            logging.info(f"Generated name: {name}")
            return name
        except Exception as e:
            logging.error(f"Error in name generation: {e}")
            # Fallback to default culture or random name
            default_culture = "English"
            logging.info(f"Falling back to default culture: {default_culture}")
            name = self.get_name_from_api(default_culture)
            return name if name != "Name generation failed" else "John Doe"

    def get_name_from_api(self, culture):
        # The same as in the original code
        load_dotenv()
        API_KEY = os.getenv('BEHIND_THE_NAME')
        if not API_KEY:
            logging.error("API key for Behind the Name is not set.")
            raise ValueError("API key is missing. Please set it in the .env file.")

        BASE_URL = "https://www.behindthename.com/api/random.json"

        # Define usage codes for cultures
        culture_usage = {
            "New World Mythology": "amem", "Ancient Celtic": "cela", "Celtic Mythology": "celm", "Ancient Egyptian": "egya", "Egyptian Mythology": "egym", "Anglo-Saxon": "enga", "Ancient Germanic": "gmca", "Ancient Greek": "grea", "Greek Mythology": "grem", "Hindu Mythology": "indm", "Arthurian Romance": "litk", "Ancient Near Eastern": "neaa", "Near Eastern Mythology": "neam", "Ancient Roman": "roma", "Roman Mythology": "romm", "Ancient Scandinavian": "scaa", "Norse Mythology": "scam", "Slavic Mythology": "slam", "African": "afr", "Afrikaans": "afk", "Akan": "aka", "Albanian": "alb", "Algonquin": "alg", "American": "usa", "Amharic": "amh", "Apache": "apa", "Arabic": "ara", "Armenian": "arm", "Assamese": "asm", "Asturian": "ast", "Avar": "ava", "Aymara": "aym", "Azerbaijani": "aze", "Balinese": "bal", "Bashkir": "bsh", "Basque": "bas", "Belarusian": "bel", "Bengali": "ben", "Berber": "ber", "Bhutanese": "bhu", "Bosnian": "bos", "Breton": "bre", "Bulgarian": "bul", "Burmese": "bur", "Catalan": "cat", "Chamorro": "cha", "Chechen": "che", "Cherokee": "chk", "Chewa": "cew", "Cheyenne": "chy", "Chinese": "chi", "Choctaw": "cht", "Circassian": "cir", "Comanche": "com", "Comorian": "cmr", "Cornish": "cor", "Corsican": "crs", "Cree": "cre", "Croatian": "cro", "Czech": "cze", "Dagestani": "dgs", "Danish": "dan", "Dargin": "drg", "Dhivehi": "dhi", "Dutch": "dut", "English": "eng", "Esperanto": "esp", "Estonian": "est", "Ethiopian": "eth", "Ewe": "ewe", "Gluttakh": "fntsg", "Monstrall": "fntsm", "Orinami": "fntso", "Romanto": "fntsr", "Simitiq": "fntss", "Tsang": "fntst", "Xalaxxi": "fntsx", "Faroese": "fae", "Fijian": "fij", "Filipino": "fil", "Finnish": "fin", "Flemish": "fle", "French": "fre", "Frisian": "fri", "Fula": "ful", "Ga": "gaa", "Galician": "gal", "Ganda": "gan", "Georgian": "geo", "German": "ger", "Greek": "gre", "Greenlandic": "grn", "Guarani": "gua", "Gujarati": "guj", "Hausa": "hau", "Hawaiian": "haw", "Hindi": "hin", "Hmong": "hmo", "Hungarian": "hun", "Ibibio": "ibi", "Icelandic": "ice", "Igbo": "igb", "Indian": "ind", "Indonesian": "ins", "Ingush": "ing", "Inuit": "inu", "Irish": "iri", "Iroquois": "iro", "Italian": "ita", "Japanese": "jap", "Javanese": "jav", "Jèrriais": "jer", "Kannada": "kan", "Kazakh": "kaz", "Khmer": "khm", "Kiga": "kig", "Kikuyu": "kik", "Kongo": "kon", "Korean": "kor", "Kurdish": "kur", "Kyrgyz": "kyr", "Lao": "lao", "Latvian": "lat", "Limburgish": "lim", "Lithuanian": "lth", "Luhya": "luh", "Luo": "luo", "Macedonian": "mac", "Maguindanao": "mag", "Malay": "mly", "Malayalam": "mlm", "Maltese": "mal", "Manx": "man", "Maori": "mao", "Mapuche": "map", "Marathi": "mrt", "Mayan": "may", "Mbundu": "mbu", "Mongolian": "mon", "Mwera": "mwe", "Nahuatl": "nah", "Navajo": "nav", "Ndebele": "nde", "Nepali": "nep", "Norman": "nrm", "Norwegian": "nor", "Nuu-chah-nulth": "nuu", "Occitan": "occ", "Odia": "odi", "Ojibwe": "oji", "Oneida": "one", "Oromo": "oro", "Ossetian": "oss", "Pashto": "pas", "Persian": "per", "Picard": "pcd", "Pintupi": "pin", "Polish": "pol", "Portuguese": "por", "Powhatan": "pow", "Punjabi": "pun", "Quechua": "que", "Rapa Nui": "rap", "Romanian": "rmn", "Russian": "rus", "Sami": "sam", "Samoan": "smn", "Sardinian": "sar", "Scots": "sct", "Scottish": "sco", "Seneca": "sen", "Serbian": "ser", "Shawnee": "sha", "Shona": "sho", "Siksika": "sik", "Sinhalese": "sin", "Sioux": "sio", "Slovak": "slk", "Slovene": "sln", "Somali": "som", "Sorbian": "sor", "Sotho": "sot", "Spanish": "spa", "Sundanese": "sun", "Swahili": "swa", "Swazi": "swz", "Swedish": "swe", "Tagalog": "tag", "Tahitian": "tah", "Tajik": "taj", "Tamil": "tam", "Tatar": "tat", "Tausug": "tau", "Telugu": "tel", "Thai": "tha", "Sicilian": "sic", "Pet": "pets", "Indigenous American": "ame", "Coptic": "cop", "Hebrew": "heb", "Jewish": "jew", "Slavic": "sla", "Indigenous Australian": "aus", "Mohawk": "moh", "Low German": "sax", "History": "hist", "Theology": "theo", "Various": "vari", "Mythology": "myth", "Biblical (All)": "bibl", "Mormon": "morm", "Astronomy": "astr", "Literature": "lite", "Popular Culture": "popu", "Medieval": "medi", "Ancient": "anci", "Tibetan": "tib", "Tongan": "ton", "Tooro": "too", "Tswana": "tsw", "Tuareg": "tua", "Tumbuka": "tum", "Tupi": "tup", "Turkish": "tur", "Turkmen": "tkm", "Ukrainian": "ukr", "Urdu": "urd", "Urhobo": "urh", "Uyghur": "uyg", "Uzbek": "uzb", "Vietnamese": "vie", "Walloon": "wln", "Welsh": "wel", "Xhosa": "xho", "Yao": "yao", "Yolngu": "yol", "Yoruba": "yor", "Zapotec": "zap", "Zulu": "zul"
        }
        usage = culture_usage.get(culture, "")
        gender = random.choice(["m", "f"])

        params = {
            "key": API_KEY,
            "gender": gender,
            "randomsurname": "yes",
            "number": 2
        }


        if usage:
            params["usage"] = usage

        try:
            logging.debug(f"Sending request with params: {params}")
            response = requests.get(BASE_URL, params=params, timeout=10)

            logging.debug(f"Response status code: {response.status_code}")
            logging.debug(f"Response content: {response.text}")

            if response.status_code == 200:
                data = response.json()
                if "names" in data and len(data["names"]) >= 2:
                    first_name = data["names"][0]
                    last_name = data["names"][1]
                    return f"{first_name} {last_name}".strip()
                elif "names" in data and len(data["names"]) == 1:
                    return data["names"][0].strip()  # Return single name if only one is provided
                else:
                    logging.error("Unexpected response format")
                    return "Name generation failed"
            else:
                logging.error(f"API request failed with status code: {response.status_code}")
                logging.error(f"Response content: {response.text}")
                return "Name generation failed"
        except requests.exceptions.RequestException as e:
            logging.error(f"API request error: {e}")
            return "Name generation failed"
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return "Name generation failed"

    def generate_attributes(self, skill_focuses, importance):
        base_points = {
            "Cub": 12, "Cliath": 15, "Fostern": 18, "Adren": 21,
            "Athro": 24, "Elder": 27, "Legendary": 30
        }
        total_points = base_points.get(importance, 15)

        # Initialize all attributes with 1 point
        attributes = {attr: 1 for category in self.attribute_categories.values() for attr in category}
        remaining_points = total_points - len(attributes)

        # Weights for attribute categories
        weights = {}
        for category in self.attribute_categories:
            weights[category] = 2 if category in skill_focuses else 1

        # Distribute points with weights
        while remaining_points > 0:
            category = random.choices(list(self.attribute_categories.keys()), weights=[weights[c] for c in self.attribute_categories])[0]
            attr = random.choice(self.attribute_categories[category])
            if attributes[attr] < 5:
                attributes[attr] += 1
                remaining_points -= 1

        return attributes

    def generate_skills(self, skill_focuses, importance):
        base_points = {
            "Thug": 20, "Minor": 25, "Important": 30, "Boss": 35,
            "Big Bad": 40, "Legendary": 45
        }
        total_points = base_points.get(importance, 25)

        skills = {skill: 0 for skill in self.skills_data["skills"]}

        # Categorize skills if applicable
        skill_categories = {
            "Physical": ["Athletics", "Brawl", "Drive", "Firearms", "Larceny", "Stealth", "Survival"],
            "Social": ["Animal Ken", "Etiquette", "Insight", "Intimidation", "Leadership", "Performance", "Persuasion", "Streetwise", "Subterfuge"],
            "Mental": ["Academics", "Awareness", "Finance", "Investigation", "Medicine", "Occult", "Politics", "Science", "Technology"]
        }

        # Weights for skill categories
        weights = {}
        for category in skill_categories:
            weights[category] = 2 if category in skill_focuses else 1

        # Distribute points with weights
        while total_points > 0:
            category = random.choices(list(skill_categories.keys()), weights=[weights[c] for c in skill_categories])[0]
            skill = random.choice(skill_categories[category])
            if skills[skill] < 5:
                skills[skill] += 1
                total_points -= 1

        # Remove skills with 0 points
        return {k: v for k, v in skills.items() if v > 0}

    def generate_gifts(self, auspice, tribe, breed, importance):
        # Placeholder function to generate Gifts based on auspice, tribe, and breed
        # For simplicity, select random gifts from these categories

        gifts = {
            "Breed": ["Heightened Senses", "Mother's Touch", "Pulse of the Invisible"],
            "Auspice": {
                "Ragabash": ["Blur of the Milky Eye", "Open Seal", "Scent of Running Water"],
                "Theurge": ["Spirit Speech", "Mother's Touch", "Umbral Sight"],
                "Philodox": ["Resist Pain", "Scent of the True Form", "Truth of Gaia"],
                "Galliard": ["Call of the Wyld", "Heightened Senses", "Mindspeak"],
                "Ahroun": ["Inspiration", "Razor Claws", "Spirit of the Fray"]
            },
            "Tribe": {
                "Black Furies": ["Heightened Senses", "Sense Wyrm", "Curse of Aeolus"],
                "Bone Gnawers": ["Cooking", "Resist Toxin", "Scent of Sweet Honey"],
                # Add other tribes accordingly
            }
        }

        selected_gifts = []

        # Select gifts based on breed
        selected_gifts.append(random.choice(gifts["Breed"]))

        # Select gifts based on auspice
        auspice_gifts = gifts["Auspice"].get(auspice, [])
        if auspice_gifts:
            selected_gifts.append(random.choice(auspice_gifts))

        # Select gifts based on tribe
        tribe_gifts = gifts["Tribe"].get(tribe, [])
        if tribe_gifts:
            selected_gifts.append(random.choice(tribe_gifts))

        # Adjust the number of gifts based on importance
        base_gifts = {
            "Cub": 2, "Cliath": 3, "Fostern": 4, "Adren": 5,
            "Athro": 6, "Elder": 7, "Legendary": 8
        }
        total_gifts = base_gifts.get(importance, 3)
        while len(selected_gifts) < total_gifts:
            # Randomly select more gifts from any category
            all_gifts = gifts["Breed"] + sum(gifts["Auspice"].values(), []) + sum(gifts["Tribe"].values(), [])
            gift = random.choice(all_gifts)
            if gift not in selected_gifts:
                selected_gifts.append(gift)

        return selected_gifts

    def generate_merits_and_flaws(self, importance):
        merits_data = self.merits_data["Merits"]
        merits = {}
        flaws = {}
        for category, data in merits_data.items():
            if "advantages" in data:
                for adv in data["advantages"]:
                    merits[adv["name"]] = adv
            if "flaws" in data:
                for fl in data["flaws"]:
                    flaws[fl["name"]] = fl

        base_merits = {
            "Cub": 1, "Cliath": 2, "Fostern": 3, "Adren": 4,
            "Athro": 5, "Elder": 6, "Legendary": 7
        }
        base_flaws = {
            "Cub": 2, "Cliath": 2, "Fostern": 2, "Adren": 1,
            "Athro": 1, "Elder": 1, "Legendary": 0
        }

        total_merits = base_merits.get(importance, 2)
        total_flaws = base_flaws.get(importance, 2)

        selected_merits = random.sample(list(merits.values()), min(len(merits), total_merits))
        selected_flaws = random.sample(list(flaws.values()), min(len(flaws), total_flaws))

        return {
            "Merits": selected_merits,
            "Flaws": selected_flaws
        }

    def generate_backgrounds(self, importance):
        backgrounds = self.backgrounds_data["Backgrounds"]

        base_points = {
            "Cub": 1, "Cliath": 2, "Fostern": 3, "Adren": 4,
            "Athro": 5, "Elder": 6, "Legendary": 7
        }
        total_backgrounds = base_points.get(importance, 2)

        selected_backgrounds = {}
        for _ in range(total_backgrounds):
            background_name = random.choice(list(backgrounds.keys()))
            background = backgrounds[background_name]
            advantages = background.get("advantages", [])
            if advantages:
                advantage = random.choice(advantages)
                cost = advantage.get("cost", 1)
                selected_backgrounds[advantage["name"]] = cost

        return selected_backgrounds

    def generate_talismans(self, importance):
        talismans_data = self.talismans_data["Talismans"]

        base_points = {
            "Cub": 1, "Cliath": 2, "Fostern": 3, "Adren": 4,
            "Athro": 5, "Elder": 6, "Legendary": 7
        }
        total_talismans = base_points.get(importance, 2)

        selected_talismans = []
        for _ in range(total_talismans):
            talisman_name = random.choice(list(talismans_data.keys()))
            talisman = talismans_data[talisman_name]
            advantages = talisman.get("advantages", [])
            if advantages:
                advantage = random.choice(advantages)
                selected_talismans.append({
                    "Name": advantage["name"],
                    "Description": advantage["desc"],
                    "Cost": advantage["cost"],
                    "Single Use": advantage.get("single_use", False)
                })

        return selected_talismans

    def generate_caern(self, importance):
        caern_data = self.caerns_data["Caern"]

        # For simplicity, select random Bawn Traits and Spiritual Power Traits
        bawn_traits = caern_data.get("Bawn Traits", [])
        spiritual_traits = caern_data.get("Spiritual Power Traits", {}).get("Bawn Traits", [])

        selected_bawn_traits = random.sample(bawn_traits, min(len(bawn_traits), 2))
        selected_spiritual_traits = random.sample(spiritual_traits, min(len(spiritual_traits), 2))

        return {
            "Bawn Traits": selected_bawn_traits,
            "Spiritual Power Traits": selected_spiritual_traits
        }

    def format_character(self, character):
        formatted = ""
        for k, v in character.items():
            if k == "Talismans":
                formatted += f"{k}:\n"
                for talisman in v:
                    formatted += f"  {talisman['Name']} (Cost: {talisman['Cost']}, Single Use: {talisman['Single Use']}):\n"
                    formatted += f"    Description: {talisman['Description']}\n"
            elif k == "Merits and Flaws":
                formatted += "Merits:\n"
                for merit in v["Merits"]:
                    formatted += f"  {merit['name']}: {merit.get('desc', '')}\n"
                formatted += "Flaws:\n"
                for flaw in v["Flaws"]:
                    formatted += f"  {flaw['name']}: {flaw.get('desc', '')}\n"
            elif k == "Caern":
                formatted += f"{k}:\n"
                formatted += f"  Bawn Traits: {', '.join(v['Bawn Traits'])}\n"
                formatted += f"  Spiritual Power Traits: {', '.join(v['Spiritual Power Traits'])}\n"
            elif isinstance(v, dict):
                formatted += f"{k}:\n"
                for sub_k, sub_v in v.items():
                    formatted += f"  {sub_k}: {sub_v}\n"
            elif isinstance(v, list):
                formatted += f"{k}:\n"
                for item in v:
                    formatted += f"  - {item}\n"
            else:
                formatted += f"{k}: {v}\n"
        return formatted

if __name__ == "__main__":
    root = tk.Tk()
    app = WerewolfCharacterGenerator(root)
    root.mainloop()
