
# Media Asset Manager

### Dependencies

* make sure that `pipenv` and `docker` are installed on your machine
* all application specific dependencies are specified in `Pipfile`

### Configuration
follow the structure of `.env.example` and add your own environment variables.
by default the app will Read environment variables from `.env`
```
ENV="DEV" # if you are running it locally choose "DEV", if not check `config.py` for env specific config
SECRET_KEY="your-super-secret-key" # add your secret key here
WATCH_DIR="/path/to/dir" # add path to the directory you need to watch (make sure that the app has access to that dir)
```

### Install dependencies (locally)

```
pipenv install --dev
```

### How to run
```
chmod +x run.sh
./run.sh
```

#### API documentation
    api/swagger - Open-API 3.0 (Swagger) documentation
    api/redoc - Redoc documentation


### Running tests
```
chmod +x test.sh
./run.sh
```

### known bugs
* Application does not sync with files in the directory, if at anytime the background watcher is not working and files and being add/deleted, the app will lose track of these files.

* search GUI, I did configure pagination to display only 6 results at a time which works great if we need all media, however it breaks my search functionality.

* Search functionality, works fine for a demo app, but it is not scalable, I wanted to use Elastic search from the start but I was worried about my limited time, I wanted to create this app in a day max.

* Works only with text files for simplicity reasons.

### Future Improvements

* Using media files and converting to a web displayable format, probably it is better use celery for this.
* Using Elastic search for search functionality instead of the ugly ORM filter.
* Using React/MaterialUI instead of the ugly bootstrap django template (becoming fully restful).
* Implementing caching using Redis
* Adding tests, atm there are some tests written for API endpoints but the coverage is quite low.(just lack of time)
* Image fields can be added as meta fields and linked to an external CDN for storage and retrieval e.g Cloudinary.
* Find a way for docker to watch directories of Host machine and get correct events.
* Use ELK and APM for application monitoring.
* API versioning is probably good to implement right away.
