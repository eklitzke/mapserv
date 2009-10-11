import yaml
import os

def cfg_path():
    if 'MAPSERV_ROOT' in os.environ:
        cfgdir = os.environ['MAPSERV_ROOT']
    else:
        cfgdir = os.getcwd()
    return os.path.join(cfgdir, 'config.yaml')

_cfg_cache = None
def load():
    global _cfg_cache
    if _cfg_cache is None:
        _cfg_cache = yaml.load(open(cfg_path()))['mapserv']
    return _cfg_cache
