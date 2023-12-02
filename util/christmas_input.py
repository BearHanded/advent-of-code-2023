from itertools import groupby


def get_file_and_print(filename):
    fp = open(filename, 'r')
    print(BColors.OKGREEN + "--------")
    print("IMPORTING ", filename)
    print("--------" + BColors.ENDC)
    return fp


def file_to_array(filename):
    fp = get_file_and_print(filename)
    input_iterable = map(lambda x: x.replace("\n", ""), fp.readlines())
    input_array = list(input_iterable)
    return input_array


def file_as_string(filename):
    fp = get_file_and_print(filename)
    input_iterable = map(lambda x: x.replace("\n", ""), fp.readlines())
    input = list(input_iterable)[0]
    return input


def file_to_subarray(filename):
    """Chunks a file into subarrays by empty line, with each line as a string"""
    initial_array = file_to_array(filename)
    return [list(sub) for ele, sub in groupby(initial_array, key=bool) if ele]


def file_to_subarray_ints(filename):
    """Chunks a file into subarrays by empty line, with each line already converted to an int"""
    initial_array = file_to_array(filename)
    return [list(int(i) for i in sub) for ele, sub in groupby(initial_array, key=bool) if ele]



class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
