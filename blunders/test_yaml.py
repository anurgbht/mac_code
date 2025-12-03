import logging
## package name pyyaml
import yaml
from munch import Munch


class MapModuleConfig:
    @staticmethod
    def load(cfg_file=None):
        try:
            with open(cfg_file, 'r') as stream:
                cfg_dict = yaml.safe_load(stream)
                print(">>>>> LOADED CONFIGURATION FOR MAP MODULE <<<<<")
                print(yaml.dump(cfg_dict))
                print(">>>>> ----------------------------------- <<<<<")
                
        except IOError:
            raise Exception(f"{cfg_file} not found")

        config = Munch.fromDict(cfg_dict)

        # default value for logging
        if 'loglevel' not in config.MAP.LOG.keys():
            config.MAP.LOG.loglevel = 'info'
        config.MAP.LOG.loglevel = config.MAP.LOG.loglevel.upper()

        # replace with corresponding constant from the logging module
        if config.MAP.LOG.loglevel == 'DEBUG':
            config.MAP.LOG.loglevel = logging.DEBUG
        elif config.MAP.LOG.loglevel == 'INFO':
            config.MAP.LOG.loglevel = logging.INFO
        elif config.MAP.LOG.loglevel == 'WARNING':
            config.MAP.LOG.loglevel = logging.WARNING
        elif config.MAP.LOG.loglevel == 'ERROR':
            config.MAP.LOG.loglevel = logging.ERROR
        elif config.MAP.LOG.loglevel == 'CRITICAL':
            config.MAP.LOG.loglevel = logging.CRITICAL
        else:
            config.MAP.LOG.loglevel = 'INFO'

        return config
    
    
#============================================================================================================
#                                                 DEBUGGING
#============================================================================================================
def main():
    import os
    config_file = os.path.join(os.path.dirname(__file__), r"config.yaml") 
    config = MapModuleConfig().load(config_file)
    print(config)

if __name__ == "__main__":
    main()