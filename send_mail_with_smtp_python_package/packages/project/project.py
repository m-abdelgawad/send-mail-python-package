import os


def get_absolute_path():
    return os.path.abspath(__file__ + "/../../..")


if __name__ == "__main__":
    print(get_absolute_path())
