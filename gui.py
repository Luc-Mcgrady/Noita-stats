import stat_loader
import class_sum

if __name__ == '__main__':
    out_dict = class_sum.sum_classes(stat_loader.load_stats())
    print(out_dict)
