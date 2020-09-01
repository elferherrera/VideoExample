import os
from configparser import ConfigParser, ExtendedInterpolation

# Config file to set server
Config = ConfigParser(interpolation=ExtendedInterpolation())

Config.optionxform = str

# Reading config file in order to setup values
file_folder = os.path.dirname(__file__)
config_file = os.path.join(file_folder, "config.ini")

Config.read(config_file)

# In case there are ENV VARS, then
# the default values from the utils_config module are 
# changed for the ENV VARS before the modules from this
# project are loaded 
for section in Config.sections():
    for option in Config[section]:
        env_variable = os.environ.get(option, None)

        if env_variable:
            Config.set(section, option, env_variable)

# Log format for loggin module
LOG_FORMAT = '%(asctime)s %(name)s %(levelname)s - %(message)s'