import requests
import json
import random
import click

class Environment:
	def __init__(self):
		self.frames = []
		self.weapons = []
		self.systems = []

pass_environment = click.make_pass_decorator(Environment, ensure=True)

def getCompanyColor(company:str):
	company_colors = {
		"GMS": "bright_red",
		"HA": "bright_magenta",
		"SSC": "bright_yellow",
		"IPS-N": "bright_cyan",
		"HORUS": "green",
		"IC": "bright_green"
	}
	return company_colors[company] or "white"

# Function that joins the list of frame types
def getFrameTypes(frame_data: list):
	return '/'.join(frame_data)

# Function which gets a random mech not already chosen
def get_random_frame(frame_data: list, chosen_frames: list):
	narrowed_list = list(filter(lambda x: x not in chosen_frames, frame_data))
	potential_choice = random.choice(narrowed_list)
	return potential_choice

# Function that randomizes frames, 1 for each type
def randomize_frames(frame_data: list, total_frames: int, frame_types=["striker", "controller", "defender", "support", "artillery"]):
	chosen_frames = []
	for type in frame_types:
		frames_by_type = [x for x in frame_data if type in (string.lower() for string in x['mechtype'])]
		chosen_frames.append(get_random_frame(frames_by_type,chosen_frames))
	for i in range(total_frames - len(frame_types)):
		chosen_frames.append(get_random_frame(frame_data,chosen_frames))
	chosen_frames.sort(key=lambda x: (x["source"], x['name']))
	return chosen_frames

def randomize_weapons(weapon_data: list, max_license_level: int, number_to_pick: int):
	no_frame_integrated = [x for x in weapon_data if "_integrated" not in x['id']]
	not_from_a_talent = [x for x in no_frame_integrated if "talent_item" not in x or not x["talent_item"]]
	valid_license_level = [x for x in not_from_a_talent if "license_level" in x and x['license_level'] <= max_license_level]
	weapons = random.sample(valid_license_level, number_to_pick)
	weapons.sort(key=lambda x: (x["source"], x["license"], x['license_level'], x['name']))
	return weapons

def randomize_systems(system_data: list, max_license_level: int, number_to_pick: int):
	no_frame_integrated = [x for x in system_data if "_integrated" not in x['id']]
	not_from_a_talent = [x for x in no_frame_integrated if "talent_item" not in x or not x["talent_item"]]
	not_a_weaponsmith_system = [x for x in not_from_a_talent if "_weaponsmith" not in x['id']]
	valid_license_level = [x for x in not_a_weaponsmith_system if "license_level" in x and x['license_level'] <= max_license_level]
	systems = random.sample(valid_license_level, number_to_pick)
	systems.sort(key=lambda x: (x["source"], x["license"], x['license_level'], x['name']))
	return systems

# Function that prints the lists of randomly generated gear
def print_overview(frames: list, weapons: list, systems: list):
	# Frames: frame name | frame types
	click.echo(click.style(f"""Frames({len(frames)})
------""", fg='white', bold=True))
	for frame in frames:
		click.echo(click.style(f'{frame["source"]} {frame["name"]} | {getFrameTypes(frame["mechtype"])}', fg=getCompanyColor(frame["source"])))
	click.echo(click.style(f"""
Weapons({len(weapons)})
------""",fg='white', bold=True))
	# Weapons: weapon name | weapon source
	for weapon in weapons:
		if 'license' in weapon:
			weapon_to_print = f'{weapon["name"]} | {weapon["source"]} {weapon["license"]} {str(weapon["license_level"])}'
		else:
			weapon_to_print = f'{weapon["name"]} | {weapon["source"]}'
		click.echo(click.style(weapon_to_print, fg=getCompanyColor(weapon["source"])))
	# Systems: system name | system source
	click.echo(click.style(f"""
Systems({len(systems)})
------""",fg='white', bold=True))
	for system in systems:
		if 'license' in system:
			system_to_print = f'{system["name"]} | {system["source"]} {system["license"]} {str(system["license_level"])}'
		else: 
			system_to_print = f'{system["name"]} | {system["source"]}'
		click.echo(click.style(system_to_print, fg=getCompanyColor(system["source"])))

# Function that prints out individual frame deatils for better reading comprehension
def print_frame_details(frames: list):
	for frame in frames:
		stats = frame["stats"]
		click.echo(f'''{frame["source"]} {frame["name"]} | {getFrameTypes(frame["mechtype"])}
------
Stats:
    SP: {stats["sp"]}
    Size: {stats["size"]}
    Structure: {stats["structure"]}
    Stress: {stats["stress"]}
    Armor: {stats["armor"]}
    HP: {stats["hp"]}
    Speed: {stats["speed"]}
    Evasion: {stats["evasion"]}
    E-Def: {stats["edef"]}
    Maximum Heat: {stats["heatcap"]}
    Repairs: {stats["repcap"]}
    Sensor Range: {stats["sensor_range"]}
    Tech Attack Bonus: {stats["tech_attack"]}
    Save: {stats["save"]}

''')
		click.echo("Traits:")
		for trait in frame['traits']:
			print(
f'''  {trait["name"]}:
  {trait["description"]}
''')
		click.echo(f'''Core System:
{frame["core_system"]["name"]}:
  Active name: {frame["core_system"]["active_name"]}
  Active effect: {frame["core_system"]["active_effect"]}
  Passive name: {frame["core_system"]["passive_name"] if "passive_name" in frame["core_system"] else ""}
  Passive effect: {frame["core_system"]["passive_effect"] if "passive_effect" in frame["core_system"] else ""}
 ''')

# Function to generate a totally random group of frames, weapons, and systems 
def generate_all_random(frames: list, weapons: list, systems: list, save):
	random_frames = randomize_frames(frames, total_frames=7)
	random_weapons = randomize_weapons(
		weapon_data=weapons,
		max_license_level=3,
		number_to_pick=20
	)
	random_systems = randomize_systems(
		system_data=systems,
		max_license_level=3,
		number_to_pick=50
	)
	print_overview(
		frames = random_frames,
		weapons = random_weapons,
		systems = random_systems
	)

	return {"frames":random_frames,"weapons":random_weapons,"systems":random_systems}
	
@click.group()
def cli():
	pass

@click.command()
@click.version_option(version="0.1")
@click.option(
	"--save",
	"-s",
	help="stores your full json output at this location"
)
@click.option(
	"--no-save",
	help="Does not save a copy of any data generated to local storage",
	is_flag = True
)
@click.option(
	"--lcp-data", 
	"-d",
	help="additional data from other LCPs"
)
@pass_environment
def randomize(ctx, save, no_save, lcp_data):
	"""A sample cli tool to generate groups of random frames, weapons, and systems for lancer TTPG"""
	# Load core data
	core_frames_url = "https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/frames.json"
	core_weapopns_url = "https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/weapons.json"
	core_systems_url = "https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/systems.json"

	core_frames_json = requests.get(core_frames_url)
	core_frames_data = json.loads(core_frames_json.text)	
	core_weapons_json = requests.get(core_weapopns_url)
	core_weapons_data = json.loads(core_weapons_json.text)	
	core_systems_json = requests.get(core_systems_url)
	core_systems_data = json.loads(core_systems_json.text)	

	# merge core content
	for i in core_frames_data:
	 	if i["name"] != "ERR: DATA NOT FOUND":
	 		ctx.frames.append(i)
	for i in core_weapons_data:
	 	if i["name"] != "ERR: DATA NOT FOUND":
	 		ctx.weapons.append(i)
	for i in core_systems_data:
	 	if i["name"] != "ERR: DATA NOT FOUND":
	 		ctx.systems.append(i)

	# load extra content if provided
	if lcp_data is not None:
		extra_content_file = open(lcp_data)
		extra_content_data = json.load(extra_content_file)

		for entry in extra_content_data:
			entry_frames = entry["data"]["frames"]
			for extra_frame in entry_frames:
				ctx.frames.append(extra_frame)
			entry_weapons = entry["data"]["weapons"]
			for extra_weapon in entry_weapons:
				ctx.weapons.append(extra_weapon)
			entry_systems = entry["data"]["systems"]
			for extra_system in entry_systems:
				ctx.systems.append(extra_system)

	data = generate_all_random(ctx.frames, ctx.weapons, ctx.systems,save)

	if save is not None:
		with open(save, 'w') as outfile:
			json.dump(data, outfile)
	elif no_save is None:
		with open('lancer-random-data.json', 'w') as outfile:
			json.dump(data, outfile)

@click.command()
@click.argument(
	"json-file", type=click.Path(), nargs=1
)
@click.option(
	"--lcp-data",
	help="additional data from other LCPs"
)
@click.option(
	"-fd", 
	"--frame-details", 
	is_flag= True,
	help="print additional frame details"
)
@click.option(
	"-wd", 
	"--weapon-details", 
	is_flag= True,
	help="print additional weapon details"
)
@click.option(
	"-sd", 
	"--system-details", 
	is_flag= True,
	help="print additional frame details"
)
def details(json_file, lcp_data, frame_details):
	json_to_load = open(json_file)
	data = json.load(json_to_load)
	if frame_details:
		print_frame_details(data["frames"])
	else:
		print_overview(data["frames"], data["weapons"], data["systems"])

cli.add_command(details)
cli.add_command(randomize)