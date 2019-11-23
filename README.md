

# media_asset_manager

clone this repository

chmod +x install.sh

./install.sh

## Flow

![Flow Diagram](static/flow.png)

# How to run

## Using docker compose

### Build the project
```
docker-compose up --build
```

## How to run
```
docker-compose up
```

## Using vscode devcointainers
Install the extensions remote-containers to vscode and then just open the folder
containing this project and vscode should prompt you about runnning it in a 
devcontainer.

### Commands
If you're using the devcontainer solution you also have a couple of commands you
can use.

```sh
# Start the server
$ run server

# Start the celery worker
$ run worker

# Start flower
$ run flower
```
