# Wishlist web app written in Python/Flask with a Svelte and Tailwind frontend

Build client code with:
```
./node_modules/.bin/gulp
```
Or, for release builds, set the `RELEASE` environment variable to `1` and run:
```
./node_modules/.bin/gulp buildOnly
```

Run Playwright component tests with:
```
npm run test-ct
```

Run Jasmine module unit tests with:
```
npm run test-m
```

https://realpython.com/flask-google-login/

https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https/page/0

Required environment variables
```
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
```

Optional environment variables
```
ENABLE_INTERNAL_AUTH
BASE_PATH
WORKING_DIR
SQLITE_DB
```

SMTP environment variables
```
SMTP_EMAIL
SMTP_SERVER
SMTP_PORT
SMTP_PASSWORD
```

Environment variable for notifications API microservice URL
```
NOTIFICATIONS_API
```
