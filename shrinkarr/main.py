import os
import shutil

from dotenv import load_dotenv
from humanfriendly import format_size, parse_size
from qbittorrent import Client

from .config import Config
from .qbit import Torrent

load_dotenv()

config = Config(
    qbit_host=os.getenv("SHRINKARR_QBIT_HOST"),
    qbit_user=os.getenv("SHRINKARR_QBIT_USER"),
    qbit_password=os.getenv("SHRINKARR_QBIT_PASSWORD"),
    monitor_path=os.getenv("SHRINKARR_MONITOR_PATH"),
    free_space=parse_size(os.getenv("SHRINKARR_FREE_SPACE"))
    if os.getenv("SHRINKARR_FREE_SPACE")
    else None,
    free_space_ratio=float(os.getenv("SHRINKARR_FREE_SPACE_RATIO"))
    if os.getenv("SHRINKARR_FREE_SPACE_RATIO")
    else None,
    delete_by_completed_on=True
    if not os.getenv("SHRINKARR_MIN_DELETE_SIZE")
    else False,
    min_delete_size=parse_size(os.getenv("SHRINKARR_MIN_DELETE_SIZE"))
    if os.getenv("SHRINKARR_MIN_DELETE_SIZE")
    else None,
    allowed_categories=os.getenv("SHRINKARR_ALLOWED_CATEGORIES").split(",")
    if os.getenv("SHRINKARR_ALLOWED_CATEGORIES")
    else None,
)

qb = Client(config.qbit_host)

qb.login(config.qbit_user, config.qbit_password)

stat = shutil.disk_usage(config.monitor_path)

min_free_space = (
    stat.total * config.free_space_ratio
    if config.free_space_ratio
    else config.free_space
)


def main():
    if stat.free > min_free_space:
        print(
            f"Free space is {format_size(stat.free)} which is more than the specified {format_size(min_free_space)}, returning..."
        )
        return

    torrents: list[Torrent] = qb.torrents()
    allowed_torrents_to_delete = list(
        filter(
            lambda torrent: torrent["completed"] != 0
            and torrent["category"] in config.allowed_categories
            if config.allowed_categories is not None
            else True,
            torrents,
        )
    )

    new_free_space = stat.free
    torrents_to_delete: list[Torrent] = list()

    if config.delete_by_completed_on:
        torrents_by_completed_on = sorted(
            allowed_torrents_to_delete,
            key=lambda torrent: torrent["completion_on"],
        )
        for torrent in torrents_by_completed_on:
            new_free_space += torrent["size"]
            torrents_to_delete.append(torrent)
            if new_free_space > min_free_space:
                break
    else:
        torrents_by_size = sorted(
            filter(
                lambda torrent: torrent["size"] > config.min_delete_size,
                allowed_torrents_to_delete,
            ),
            key=lambda torrent: torrent["size"],
            reverse=True,
        )
        for torrent in torrents_by_size:
            new_free_space += torrent["size"]
            torrents_to_delete.append(torrent)
            if new_free_space > min_free_space:
                break

    print(
        f"Deleting {len(torrents_to_delete)} to free {format_size(new_free_space-stat.free)}"
    )
    qb.delete(list(map(lambda torrent: torrent["hash"], torrents_to_delete)))


if __name__ == "__main__":
    main()
