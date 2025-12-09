# checksums.py

import os
import hashlib

# files to hash for integrity
FILES_TO_HASH = [
    "data/processed/games_with_weather.csv",
    "data/processed/games_with_coords.csv",
    "data/raw/venues_all.csv",
]


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs("results", exist_ok=True)

    lines = []
    for path in FILES_TO_HASH:
        if os.path.exists(path):
            digest = sha256_of_file(path)
            lines.append(f"{digest}  {path}")
        else:
            lines.append(f"[missing] {path}")

    out_path = "results/data_checksums.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"wrote checksums to {out_path}")


if __name__ == "__main__":
    main()