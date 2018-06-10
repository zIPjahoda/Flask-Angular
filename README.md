# Jednoduchy test Angular s Flaskem
---

Jednoducha Angular 2 app s prihlasenim 


## Usage
---

1.  Install the backend related requirements and run. The following will start a flask-server on `localhost:8080`

    ```bash
    cd backend
    sudo pip install -r requirements.txt
    python run.py
    ```

2.  Extra Note: To create a production build

    ```bash
    cd front
    npm install webpack-dev-server rimraf webpack typescript -g
    npm install
    npm run build:prod

    # Serves on http://localhost:5000
    npm run server:prod
    ```
