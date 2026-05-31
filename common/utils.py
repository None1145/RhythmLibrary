import pathlib
import msgpack

def save_data_to_file(data: dict, save_path: str | pathlib.Path) -> None:
    if isinstance(save_path, pathlib.Path):
        save_path = str(save_path)
    
    if not save_path.endswith(".msgpack"):
        save_path += ".msgpack"
    with open(save_path, "wb") as f:
        msgpack.dump(data, f)
