# Github Trending Dashboard

## Run MongoDB with Docker

```commandline
docker run -p 27017:27017 -d --name github-mongo mongo
```

## Environment Variables

Go to **Settings** > **Developer settings** > **Personal access token** > **Generate new token**, copy and paste it here:

```commandline
GITHUB_TOKEN=
```
Database uri connection (default: )

```commandline
MONGO_URI=
```

## Run App

```commandline
python app/main.py
```
