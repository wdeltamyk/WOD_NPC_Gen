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

class VTMCharacterGenerator:
    def __init__(self, master):
        self.master = master
        master.title("VTM V5 Character Generator")
        master.geometry("600x800")

        # Load JSON data
        self.load_json_data()

        # Create and set up the GUI elements
        self.setup_gui()

    # Validate before loading json values
    def validate_json_data(self):
        if "Disciplines" not in self.disciplines_data:
            raise KeyError("'Disciplines' key not found in disciplines data")
        for discipline, data in self.disciplines_data["Disciplines"].items():
            if "skills" not in data:
                raise KeyError(f"'skills' key not found for discipline {discipline}")
        if "clans" not in self.clan_disciplines_data:
            raise KeyError("'clans' key not found in clan disciplines data")

    def load_json_data(self):
        try:
            with open('5eAttributes.json') as f:
                self.attributes_data = json.load(f)
            with open('5eSkills.json') as f:
                self.skills_data = json.load(f)
            with open('5eDisciplines.json') as f:
                self.disciplines_data = json.load(f)
            with open('5eClanDiscs.json') as f:
                self.clan_disciplines_data = json.load(f)
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
        # Generation
        ttk.Label(self.master, text="Generation:").grid(row=0, column=0, sticky="w")
        self.generation = ttk.Combobox(self.master, values=list(range(1, 17)))
        self.generation.grid(row=0, column=1)
        self.generation.set(13)  # Default to 13th generation

        # Clan
        ttk.Label(self.master, text="Clan:").grid(row=1, column=0, sticky="w")
        self.clan = ttk.Combobox(self.master, values=["Brujah", "Gangrel", "Nosferatu", "Malkavian", "Toreador", "Tremere", "Ventrue", "Caitiff", "Thin Blood", "Hecata", "Assamite", "Setite", "Tzimisce", "Salubri", "Lasombra", "Ravnos"])
        self.clan.grid(row=1, column=1)

        # Skill Focus (Multiple Selection)
        ttk.Label(self.master, text="Skill Focus:").grid(row=2, column=0, sticky="w")
        self.skill_focus = tk.Listbox(self.master, selectmode=tk.MULTIPLE, exportselection=0)
        for idx, focus in enumerate(["Physical", "Social", "Mental"]):
            self.skill_focus.insert(idx, focus)
        self.skill_focus.grid(row=2, column=1)

        # Sect
        ttk.Label(self.master, text="Sect:").grid(row=3, column=0, sticky="w")
        self.sect = ttk.Combobox(self.master, values=["Camarilla", "Anarchs", "Autarkis", "Sabbat", "Hecata", "Black Hand", "Ashirra"])
        self.sect.grid(row=3, column=1)

        # Diablerist
        ttk.Label(self.master, text="Diablerist:").grid(row=4, column=0, sticky="w")
        self.diablerist = ttk.Combobox(self.master, values=["Yes", "No"])
        self.diablerist.grid(row=4, column=1)
        self.diablerist.set("No")

        # NPC Importance
        ttk.Label(self.master, text="NPC Importance:").grid(row=5, column=0, sticky="w")
        self.importance = ttk.Combobox(self.master, values=["Thug", "Minor", "Important", "Boss", "Big Bad", "Ancient", "Mythical"])
        self.importance.grid(row=5, column=1)

        # Culture (for name generation)
        ttk.Label(self.master, text="Culture:").grid(row=8, column=0, sticky="w")
        self.culture = ttk.Combobox(self.master, values=[
            "New World Mythology", "Ancient Celtic", "Celtic Mythology", "Ancient Egyptian", "Egyptian Mythology", "Anglo-Saxon", "Ancient Germanic", "Ancient Greek", "Greek Mythology", "Hindu Mythology", "Arthurian Romance", "Ancient Near Eastern", "Near Eastern Mythology", "Ancient Roman", "Roman Mythology", "Ancient Scandinavian", "Norse Mythology", "Slavic Mythology", "African", "Afrikaans", "Akan", "Albanian", "Algonquin", "American", "Amharic", "Apache", "Arabic", "Armenian", "Assamese", "Asturian", "Avar", "Aymara", "Azerbaijani", "Balinese", "Bashkir", "Basque", "Belarusian", "Bengali", "Berber", "Bhutanese", "Bosnian", "Breton", "Bulgarian", "Burmese", "Catalan", "Chamorro", "Chechen", "Cherokee", "Chewa", "Cheyenne", "Chinese", "Choctaw", "Circassian", "Comanche", "Comorian", "Cornish", "Corsican", "Cree", "Croatian", "Czech", "Dagestani", "Danish", "Dargin", "Dhivehi", "Dutch", "English", "Esperanto", "Estonian", "Ethiopian", "Ewe", "Gluttakh", "Monstrall", "Orinami", "Romanto", "Simitiq", "Tsang", "Xalaxxi", "Faroese", "Fijian", "Filipino", "Finnish", "Flemish", "French", "Frisian", "Fula", "Ga", "Galician", "Ganda", "Georgian", "German", "Greek", "Greenlandic", "Guarani", "Gujarati", "Hausa", "Hawaiian", "Hindi", "Hmong", "Hungarian", "Ibibio", "Icelandic", "Igbo", "Indian", "Indonesian", "Ingush", "Inuit", "Irish", "Iroquois", "Italian", "Japanese", "Javanese", "Jèrriais", "Kannada", "Kazakh", "Khmer", "Kiga", "Kikuyu", "Kongo", "Korean", "Kurdish", "Kyrgyz", "Lao", "Latvian", "Limburgish", "Lithuanian", "Luhya", "Luo", "Macedonian", "Maguindanao", "Malay", "Malayalam", "Maltese", "Manx", "Maori", "Mapuche", "Marathi", "Mayan", "Mbundu", "Mongolian", "Mwera", "Nahuatl", "Navajo", "Ndebele", "Nepali", "Norman", "Norwegian", "Nuu-chah-nulth", "Occitan", "Odia", "Ojibwe", "Oneida", "Oromo", "Ossetian", "Pashto", "Persian", "Picard", "Pintupi", "Polish", "Portuguese", "Powhatan", "Punjabi", "Quechua", "Rapa Nui", "Romanian", "Russian", "Sami", "Samoan", "Sardinian", "Scots", "Scottish", "Seneca", "Serbian", "Shawnee", "Shona", "Siksika", "Sinhalese", "Sioux", "Slovak", "Slovene", "Somali", "Sorbian", "Sotho", "Spanish", "Sundanese", "Swahili", "Swazi", "Swedish", "Tagalog", "Tahitian", "Tajik", "Tamil", "Tatar", "Tausug", "Telugu", "Thai", "Sicilian", "Pet", "Indigenous American", "Coptic", "Hebrew", "Jewish", "Slavic", "Indigenous Australian", "Mohawk", "Low German", "History", "Theology", "Various", "Mythology", "Biblical (All)", "Mormon", "Astronomy", "Literature", "Popular Culture", "Medieval", "Ancient", "Tibetan", "Tongan", "Tooro", "Tswana", "Tuareg", "Tumbuka", "Tupi", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Urhobo", "Uyghur", "Uzbek", "Vietnamese", "Walloon", "Welsh", "Xhosa", "Yao", "Yolngu", "Yoruba", "Zapotec", "Zulu"
        ])
        self.culture.grid(row=9, column=1)

        # Generate button
        self.generate_button = ttk.Button(self.master, text="Generate Character", command=self.generate_character)
        self.generate_button.grid(row=7, column=0, columnspan=2)

        # Result display with scrollbar
        self.result_frame = ttk.Frame(self.master)
        self.result_frame.grid(row=8, column=0, columnspan=2)
        self.result_text = tk.Text(self.result_frame, height=25, width=70)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar = ttk.Scrollbar(self.result_frame, command=self.result_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=self.scrollbar.set)

    def generate_character(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Generating character...")
        self.generate_button.config(state="disabled")

        generation = int(self.generation.get())
        clan = self.clan.get()

        # Get selected skill focuses
        selected_indices = self.skill_focus.curselection()
        skill_focus = [self.skill_focus.get(i) for i in selected_indices]
        if not skill_focus:
            # Default to all focuses if none selected
            skill_focus = ["Physical", "Social", "Mental"]

        sect = self.sect.get()
        diablerist = self.diablerist.get() == "Yes"
        importance = self.importance.get()
        culture = self.culture.get()

        # Increase timeout to 60 seconds
        timer = threading.Timer(60.0, self.generation_timeout)
        timer.start()

        thread = threading.Thread(target=self.threaded_character_generation,
                                  args=(generation, clan, skill_focus, sect, diablerist, importance, culture, timer))
        thread.start()

    def generation_timeout(self):
        logging.error("Character generation timed out")
        self.master.after(0, self.update_gui_with_error, "Character generation timed out")

    def threaded_character_generation(self, generation, clan, skill_focus, sect, diablerist, importance, culture, timer):
        try:
            logging.info("Starting character generation")

            logging.info("Generating name")
            name = self.generate_name(culture)
            logging.info(f"Name generated: {name}")

            logging.info("Starting character creation")
            character = {
                "Name": name,
                "Generation": generation,
                "Clan": clan,
                "Sect": sect
            }

            logging.info("Calculating blood potency")
            character["Blood Potency"] = self.calculate_blood_potency(generation, importance)
            logging.info(f"Blood Potency calculated: {character['Blood Potency']}")

            logging.info("Generating attributes")
            character["Attributes"] = self.generate_attributes(skill_focus, importance)
            logging.info("Attributes generated")

            logging.info("Generating skills")
            character["Skills"] = self.generate_skills(skill_focus, importance)
            logging.info("Skills generated")

            logging.info("Generating disciplines")
            character["Disciplines"] = self.generate_disciplines(clan, diablerist, importance)
            logging.info("Disciplines generated")

            logging.info("Calculating humanity")
            character["Humanity"] = self.generate_humanity(importance)
            logging.info(f"Humanity calculated: {character['Humanity']}")

            logging.info("Generating advantages")
            character["Advantages"] = self.generate_advantages(sect, importance)
            logging.info("Advantages generated")

            logging.info("Generating flaws")
            character["Flaws"] = self.generate_flaws(importance)
            logging.info("Flaws generated")

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

    def calculate_blood_potency(self, generation, importance):
        base_potency = max(1, 16 - generation)
        importance_bonus = {
            "Thug": 0, "Minor": 1, "Important": 2, "Boss": 3,
            "Big Bad": 4, "Ancient": 5, "Mythical": 6
        }
        return min(10, base_potency + importance_bonus.get(importance, 0))

    def generate_attributes(self, skill_focuses, importance):
        base_points = {
            "Thug": 12, "Minor": 15, "Important": 18, "Boss": 21,
            "Big Bad": 24, "Ancient": 27, "Mythical": 30
        }
        total_points = base_points.get(importance, 15)

        # Initialize all attributes with 1 point
        attributes = {attr: 1 for category in self.attribute_categories.values() for attr in category}
        remaining_points = total_points - len(attributes)

        # Weights for attribute categories
        weights = {}
        for category in self.attribute_categories:
            weights[category] = 2 if category in skill_focuses else 1

        attributes_list = list(attributes.keys())

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

        # Categorize skills if applicable (assuming skills can be categorized)
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

    def generate_disciplines(self, clan, diablerist, importance):
        try:
            clan_disciplines = self.clan_disciplines_data["clans"].get(clan, {}).get("disciplines", [])
            if not clan_disciplines:
                raise KeyError
        except KeyError:
            logging.error(f"Clan {clan} not found in clan disciplines data or has no disciplines")
            clan_disciplines = ["Random1", "Random2", "Random3"]

        base_points = {
            "Thug": 4, "Minor": 5, "Important": 6, "Boss": 7,
            "Big Bad": 8, "Ancient": 9, "Mythical": 10
        }
        total_points = base_points.get(importance, 4)

        disciplines = {}

        all_disciplines = list(self.disciplines_data["Disciplines"].keys())

        # Prioritize clan disciplines
        for disc in clan_disciplines:
            if total_points <= 0:
                break
            if disc.startswith("Random"):
                disc = random.choice(all_disciplines)

            if disc not in disciplines:
                level = min(5, random.randint(1, total_points))
                disciplines[disc] = {
                    "level": level,
                    "skills": self.get_discipline_skills(disc, level)
                }
                total_points -= level

        # If diablerist, add a random non-clan discipline
        if diablerist and total_points > 0:
            rare_disciplines = [d for d in all_disciplines if d not in disciplines]
            if rare_disciplines:
                extra_disc = random.choice(rare_disciplines)
                level = min(3, total_points)
                disciplines[extra_disc] = {
                    "level": level,
                    "skills": self.get_discipline_skills(extra_disc, level)
                }
                total_points -= level

        # If points remain, distribute among existing disciplines
        while total_points > 0:
            disc = random.choice(list(disciplines.keys()))
            if disciplines[disc]["level"] < 5:
                disciplines[disc]["level"] += 1
                total_points -= 1

        return disciplines

    def get_discipline_skills(self, discipline, level):
        try:
            discipline_skills = self.disciplines_data["Disciplines"][discipline]["skills"]
            return [random.choice(skill_level) for skill_level in discipline_skills[:level]]
        except KeyError:
            logging.error(f"Discipline {discipline} not found in disciplines data")
            return []
        except IndexError:
            logging.error(f"Not enough skill levels for discipline {discipline}")
            return []

    def generate_humanity(self, importance):
        base_humanity = {
            "Thug": 7, "Minor": 6, "Important": 5, "Boss": 4,
            "Big Bad": 3, "Ancient": 2, "Mythical": 1
        }
        return base_humanity.get(importance, 6)

    def generate_advantages(self, sect, importance):
        all_advantages = ["Allies", "Contacts", "Fame", "Herd", "Influence", "Resources", "Status"]
        num_advantages = {
            "Thug": 1, "Minor": 2, "Important": 3, "Boss": 4,
            "Big Bad": 5, "Ancient": 6, "Mythical": 7
        }

        advantages = {}
        for _ in range(num_advantages.get(importance, 2)):
            adv = random.choice(all_advantages)
            advantages[adv] = random.randint(1, 5)

        # Add sect-specific advantage
        if sect in ["Camarilla", "Anarchs", "Autarkis", "Sabbat", "Hecata", "Black Hand", "Ashirra"]:
            advantages[f"{sect} Status"] = random.randint(1, 3)

        return advantages

    def generate_flaws(self, importance):
        all_flaws = ["Addiction", "Enemy", "Haunted", "Hunted", "Infamous", "Indebted", "Suspect"]
        num_flaws = {
            "Thug": 3, "Minor": 2, "Important": 2, "Boss": 1,
            "Big Bad": 1, "Ancient": 1, "Mythical": 0
        }

        flaws = {}
        for _ in range(num_flaws.get(importance, 2)):
            flaw = random.choice(all_flaws)
            flaws[flaw] = random.randint(1, 3)

        return flaws

    def format_character(self, character):
        formatted = ""
        for k, v in character.items():
            if k == "Disciplines":
                formatted += f"{k}:\n"
                for disc, details in v.items():
                    formatted += f"  {disc} (Level {details['level']}):\n"
                    for skill in details['skills']:
                        formatted += f"    - {skill}\n"
            elif isinstance(v, dict):
                formatted += f"{k}:\n"
                for sub_k, sub_v in v.items():
                    formatted += f"  {sub_k}: {sub_v}\n"
            else:
                formatted += f"{k}: {v}\n"
        return formatted

if __name__ == "__main__":
    root = tk.Tk()
    app = VTMCharacterGenerator(root)
    root.mainloop()