import argparse
import os
import random


class SlowClass(object):

    def __init__(self, first_names_file):
        """ Initialize a `SlowClass`

        Args:
            first_names_file (:obj:`str`): the name of a file in the `data` subdir
                of the directory storing this program
        """
        filename = os.path.join(os.path.dirname(__file__), 'data', first_names_file)
        with open(filename, 'r') as fh:
            self.first_names = [l.strip() for l in fh.readlines()]

    def known_name(self, name):
        """ Determine whether a name exists in the list of first names

        Args:
            name (:obj:`str`): a name to search for

        Returns:
            :obj:`bool`: `True` if `name` is found, false otherwise
        """
        for first_name in self.first_names:
            if name == first_name:
                return True
        return False

    def num_known_names(self, name_list):
        """ Count the number of names in `name_list` that appear in `self.first_names`

        Args:
            name_list (:obj:`list` of :obj:`str`): a list of names

        Returns:
            :obj:`int`: the number of names in `name_list` that appear in `self.first_names`
        """
        count = 0
        for name in name_list:
            if self.known_name(name):
                count += 1
        return count


def parse_args():
    """ Parse command line argument(s)

    Returns:
        :obj:`argparse.Namespace`: parsed command line arguements
    """
    parser = argparse.ArgumentParser(description="Performance measurement and tuning")
    parser.add_argument('sample_fraction', type=float, help="Fraction of list to sample, in (0, 1]")
    args = parser.parse_args()
    if args.sample_fraction <= 0 or 1 < args.sample_fraction:
        parser.error(f"sample_fraction ({args.sample_fraction}) must be in (0, 1]")
    return args

def use_slow_class():
    """ Try running  SlowClass.num_known_names() """
    slow_class = SlowClass('first-names.txt')
    args = parse_args()
    size_names_list = len(slow_class.first_names)
    sample_names = random.sample(slow_class.first_names, int(args.sample_fraction * size_names_list))
    print(slow_class.num_known_names(sample_names), 'names found')


if __name__ == '__main__':
    use_slow_class()