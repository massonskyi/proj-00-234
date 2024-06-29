import os
import shutil


def check_configuration():
    config_file_path = "./configuration_config_mdt.json"

    if os.path.exists(config_file_path):
        yield [True]

    try:
        from utils.configuration_config_mdt import ConfigurationMDTH
        config = ConfigurationMDTH.create_configuration_config_mdt()
        config.save_as_json()
    except Exception as e:
        yield [f"Failed to create configuration file: {str(e)}"]
    else:
        yield ["Configuration file created successfully."]


def remove_pycache_dirs(start_path='.'):
    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                shutil.rmtree(pycache_path)
                yield f"Removed: {pycache_path}"
