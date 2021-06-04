import xml_python
import xmlfuncs
import os


def _check_list(to_check):
    if type(to_check) != list:
        return [to_check]
    else:
        return to_check


def _e_check(to_check, conv_class=None):
    if "E" in to_check:
        to_check = _check_list(to_check['E'])

    if conv_class is not None:
        return [conv_class(a) for a in to_check]
    else:
        return to_check


def _xml_key_val_to_dict(xml: list[dict]):
    return {a["key"]: int(a["value"]) for a in xml}


class RunStats:
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
        self.player_kills = {" ".join(key.split('_')[::-1]): val for key,val in self.player_kills.items()}
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


def load_stats():
    stats_path = os.path.abspath(os.environ.get('APPDATA') + "/../LocalLow/Nolla_Games_Noita/save00/stats/sessions") \
                 + '\\'
    #  ^ This is what you need to change if doesnt work correctly ^

    files = os.listdir(stats_path)
    data = {
        file: xmlfuncs.as_attr_dict(
            xml_python.parse(stats_path + file).getroot()
        )
        for file in files
    }

    data = {key: RunStats(kills, stats) for
            kills, (key, stats) in
            zip(list(data.values())[::2], list(data.items())[1::2])}

    return data
