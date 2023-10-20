import os
import re
import shutil

SERVER_PROPERTIES_PATH = "server.properties"

def reset_server(level_type="flat", regen_world=False):
    trg_level_type = level_type
    # Read contents of server.properties
    with open(SERVER_PROPERTIES_PATH, "r") as f:
        content = f.read()
    # User regular expression to check if level-type=default
    if not re.search(f"level-type={trg_level_type}", content) or regen_world:
        try:
            content = re.sub(r'level-type=\w+', f'level-type={trg_level_type}', content)
            # Write contents of server.properties
            with open(SERVER_PROPERTIES_PATH, "w") as f:
                f.writelines(content)
            # Remove server/world folder.
            try:
                shutil.rmtree("world")
            except FileNotFoundError:
                pass
            shutil.rmtree(".mixin.out")
            shutil.rmtree("logs")
            if os.path.exists("crash-reports"):
                shutil.rmtree("crash-reports")
            os.remove("ops.json")
            shutil.rmtree("config")
            os.remove("banned-ips.json")
            os.remove("banned-players.json")
            os.remove("whitelist.json")
        except FileNotFoundError:
            print("Failed to clean old world, loading it up again.")

    # Launch the server.
    os.system("java -jar spongevanilla-1.12.2-7.3.0.jar")


if __name__ == "__main__":
    reset_server(level_type="flat", regen_world=True)