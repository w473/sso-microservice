# SSO-PY
SIMPLE SSO server generating JWT

## virtual env setup
python3 -m venv venv
. venv/bin/activate

## run app
run.sh

### CLI COMMANDS
flask init db
flask key generate

### test run
. venv/bin/activate
pytest