import os
import argparse

# Set defaults for config and output
conf_dir = '{}/rofi-mopidy-spotify'.format(os.environ.get('XDG_CONFIG_HOME') or
                                           os.path.expanduser('~/.config'))
cache_dir = '{}/rofi-mopidy-spotify'.format(os.environ.get('XDG_CACHE_HOME') or
                                            os.path.expanduser('~/.cache'))

# Parse command line overrides if given
parser = argparse.ArgumentParser(description='Rofi music adding script')
parser.add_argument('-c', dest='conf_dir', default=conf_dir,
                    help='config dir')
parser.add_argument('-C', dest='cache_dir', default=cache_dir,
                    help='cache dir')
args = parser.parse_args()
