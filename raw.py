# Returns just the json if you want to see it,
import stat_loader
import class_sum

import json

if __name__ == '__main__':
    out_dict = class_sum.sum_dict_classes(stat_loader.load_stats())
    print("Totals: ")
    print(json.dumps(out_dict, indent=4))
    input("Press enter to close: ")
