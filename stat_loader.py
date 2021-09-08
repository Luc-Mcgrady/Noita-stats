import xml_python
import xml_funcs
import traceback
import os


def _check_list(to_check):
    """If a value is not a list, pack it into one and return it, else just returns the value"""
    if type(to_check) != list:
        return [to_check]
    else:
        return to_check


def _e_check(to_check, conv_class=None):
    """
    :param to_check: the dictionary to check
    :param conv_class: Unused, used to convert the elements of the return to a class
    :return: to_check['E'] Or an empty list if that value isn't there
    """
    if "E" in to_check:
        to_check = _check_list(to_check['E'])
    else:
        return []

    if conv_class is not None:
        return [conv_class(a) for a in to_check]
    else:
        return to_check


def _xml_key_val_to_dict(xml: list[dict]):
    return {a["key"]: int(a["value"]) for a in xml}


class RunStats:
    """Holds a representation of both the 2 files that are saved"""

    def __init__(self, kills_xml: dict, stats_xml: dict):
        self.kills = XmlKills(kills_xml)
        self.stats = XmlStats(stats_xml)


class XmlKills:

    def __init__(self, xml: dict):
        self.kills = int(xml['kills'])
        self.player_projectile_count = int(xml['player_projectile_count'])
        self.player_kill_count = int(xml['player_kills'])

        self.player_kills = xml['kill_map']
        self.player_kills = _xml_key_val_to_dict(_e_check(self.player_kills))
        self.player_kills = {" ".join(key.split('_')[::-1]): val for key, val in self.player_kills.items()}
        # Reverse order for adjectives

        self.death_map = xml['death_map']
        self.death_map = _xml_key_val_to_dict(_e_check(self.death_map))


class XmlStats:
    def __init__(self, xml: dict):
        stats = xml["stats"]

        self.biomes_visited_with_wands = int(stats["biomes_visited_with_wands"])  # Not a clue
        self.damage_taken = float(stats["damage_taken"])
        self.dead = bool(stats["dead"])
        self.death_pos_x = float(stats["death_pos.x"])
        self.death_pos_y = float(stats["death_pos.y"])  # Same as depth
        self.enemies_killed = int(stats["enemies_killed"])  # Same as player kill count I assume (maybe w/o friendly's)
        self.gold = int(stats["gold"])
        self.gold_all = int(stats["gold_all"])
        self.items = int(stats["items"])
        self.kicks = int(stats["kicks"])
        self.visited_count = int(stats["places_visited"])
        self.playtime = float(stats["playtime"])
        self.playtime_formatted = stats["playtime_str"]
        self.shots_fired = int(stats["projectiles_shot"])
        self.teleports = int(stats["teleports"])
        self.wands_edited = int(stats["wands_edited"])

        self.biomes_visited = xml["biomes_visited"]
        self.biomes_visited = _xml_key_val_to_dict(_e_check(self.biomes_visited))


STATS_PATH = os.path.abspath(os.environ.get('APPDATA') + "/../LocalLow/Nolla_Games_Noita/save00/stats/sessions") \
             + '\\'


def load_stats() -> dict[str, dict]:
    """:return: The players stats in the form dict[Filename: loaded stats]"""
    global STATS_PATH

    if not os.path.isdir(STATS_PATH):
        STATS_PATH = input(f"Stats not found at regular directory of {STATS_PATH}, provide a replacement directory?: ")

    files = os.listdir(STATS_PATH)

    data = {}
    for file in files:
        try:
            data[file] = xml_funcs.as_attr_dict(
                xml_python.parse(STATS_PATH + file).getroot()
            )
        except Exception as e:
            print(f"Failed to parse file: \"{file}\" with exception: {e!r}")

    data = {key: RunStats(kills, stats) for  # Stats are stored in 2 files per run by the game,
            kills, (key, stats) in
            zip(
                list([val for key, val in data.items() if key.endswith("kills.xml")]),
                list([(key, val) for key, val in data.items() if key.endswith("stats.xml")])
            )
            }

    return data
