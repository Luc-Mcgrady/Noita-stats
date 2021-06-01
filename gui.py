import xml_python
import xmlfuncs
import os


def main():
    stats_path = os.path.abspath(os.environ.get('APPDATA') + "/../LocalLow/Nolla_Games_Noita/save00/stats/sessions") \
                 + '\\'

    files = os.listdir(stats_path)
    data = {
        file: xmlfuncs.as_attr_dict(
            xml_python.parse(stats_path + file).getroot()
        )
        for file in files
    }


if __name__ == '__main__':
    main()
