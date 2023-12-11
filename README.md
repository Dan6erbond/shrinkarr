# Shrinkarr

Shrink your qBittorrent downloads folder by magnitudes.

Shrinkarr is a support tool for the \*Arr stack, that can automatically delete torrents by size or completion date once a given free space threshold has been reached. Users can limit the categories that Shrinkarr is allowed to remove.

## Motivation

Tools such as [Prunerr](https://github.com/rpatterson/prunerr) already exist to only remove torrents that have been upgraded in the *Arr apps. However, sometimes the *Arr apps and download client don't share the same disk, in which case you might want a simpler approach of deleting items once a certain free space threshold has been reached.

## Running

Shrinkarr can be run with Python, or as a Docker container.

### With Python

Simply run the script once with Python, at least 3.10 is required:

```sh
# Install dependencies, only needed once
$ python3 -m pip install -r requirements.txt
# Run Shrinkarr
$ python3 -m shrinkarr.main
```

A `.env` file must be present at the current location, or mandatory environment variables must be set. For more see [Configuration](#configuration).

### With Docker

The Docker container can manage its own CRON job running every five minutes if you want to. In which case set the `--entrypoint` to `cron`:

```sh
$ docker run shrinkarr:latest --entrypoint 'cron'
```

If you don't want the job to run every five minutes, just run the Docker container. This can be useful for managing your own scheduler e.g. with Kubernetes `CronJob`:

```sh
$ docker run shrinkarr:latest
```

## Configuration

Shrinkarr supports the following environment variables to configure its behavior.

### qBittorrent

General qBittorrent settings to connect with download client.

#### `SHRINKARR_QBIT_HOST` (mandatory, string)

The host of your qBittorrent instance. Must include http(s).

#### `SHRINKARR_QBIT_USER` (mandatory, string)

qBittorrent username.

Default: `admin`

#### `SHRINKARR_QBIT_PASSWORD` (mandatory, string)

qBittorrent password.

Default: `admin`

### Monitoring path

You can configure the path that Shrinkarr should monitor, since usually it will be running in Docker with a mounted volume.

#### `SHRINKARR_MONITOR_PATH` (mandatory, string)

Shrinkarr monitoring path. Should be absolute.

Examples: `/mnt/media`

### Free space

You can either configure the absolute free space or a ratio of the monitored path's size that Shrinkarr will use as the threshold to start deleting downloads.

#### `SHRINKARR_FREE_SPACE` (string, human-readable size)

Free space below which Shrinkarr will delete downloads.

Examples: `20GB`, `2TB`

#### `SHRINKARR_FREE_SPACE_RATIO` (float)

Ratio of the drive's total size below which Shrinkarr will delete downloads.

Examples: `0.2`

### Delete settings

#### `SHRINKARR_MIN_DELETE_SIZE` (string, human-readable size)

Minimum size of files that can be deleted.

Examples: `20GB`, `2TB`

#### `SHRINKARR_DELETE_BY_COMPLETED_ON` (bool)

Delete torrents by completed on (oldest to newest).

Examples: `true`

#### `SHRINKARR_DELETE_BY_SIZE` (bool)

Delete torrents by size (largest to smallest).

Examples: `true`

### Torrent settings

#### `SHRINKARR_ALLOWED_CATEGORIES` (comma-separated list of strings)

Categories for torrents that can be deleted.

Examples: `radarr,tv-sonarr`
