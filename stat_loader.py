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


class EnemyKill:
    def __init__(self, xml: dict):
        self.name = xml["key"]
        self.count = int(xml["value"])


class BiomeVisit(EnemyKill):  # Same format as enemy kills surprisingly
    def __init__(self, xml: dict):
        super().__init__(xml)


class DeathCause:
    def __init__(self, xml: dict):
        cause_type = xml['key'].split(' | ')
        self.cause = cause_type[0]
        self.damage_type = cause_type[1]
        self.hits = int(xml['value'])


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
        self.player_kills = _e_check(self.player_kills, EnemyKill)

        self.death_map = xml['death_map']
        self.death_map = _e_check(self.death_map, DeathCause)


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
        self.biomes_visited = _e_check(self.biomes_visited, BiomeVisit)


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
