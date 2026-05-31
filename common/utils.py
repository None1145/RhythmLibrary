import msgpack

def save_data_to_file(data: dict, save_path: str) -> None:
    if not save_path.endswith(".msgpack"):
        save_path += ".msgpack"
    with open(save_path, "wb") as f:
        msgpack.dump(data, f)
