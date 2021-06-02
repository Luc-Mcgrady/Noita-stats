import stat_loader
import class_sum

if __name__ == '__main__':
    out_dict = class_sum.json_dump_load(stat_loader.load_stats(), default=lambda o: o.__dict__, indent=4)
    out_dict = class_sum.sum_dicts(list(out_dict.values()))
    print(out_dict)
