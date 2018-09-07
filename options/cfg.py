from configparser import ConfigParser, NoOptionError
from .args import args

cfgfile = '{}/api.conf'.format(args.conf_dir)

config = ConfigParser()
try:
    config.read_file(open(cfgfile))
except FileNotFoundError:
    print('Error: {} not found'.format(cfgfile), file=sys.stderr)
    sys.exit(1)
