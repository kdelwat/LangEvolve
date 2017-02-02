# Onset

Onset is a language evolution simulator, which evolves a list of words
in [IPA form](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet)
according to realistic phonological rules.

The frontend is built with [Vue](https://vuejs.org/) and the CSS
framework [Bulma](http://bulma.io/). It communicates with the backend using
simple REST endpoints.

The backend is built with Python and [Flask](http://flask.pocoo.org/).

## Directory Structure

+ `src` is the source code for the Vue frontend
+ `app` is the source code for the Python API, written in Flask.
+ `engine` is the source code for the evolution engine which is called by Flask.
+ `app/templates/` contains the Webpack-generated index file, served with Flask.
+ `app/static/` contains static assets generated by Webpack.
+ `config` contains Webpack configuration files, generated using [vue-cli](https://github.com/vuejs/vue-cli)

## Build Setup

``` bash
# install Python dependencies
pip install -r requirements.txt

# install Javascript dependencies
npm install

# build frontend
npm run build

# run using Flask's development server
python run.py
```

To validate the YAML data:

``` bash
pip install -r requirements-dev.txt

pykwalify -d engine/data/rules.yaml -s engine/data/rules.schema.yaml
pykwalify -d engine/data/diacritics.yaml -s engine/data/diacritics.schema.yaml
```

To run the tests:

```bash
pip install -r requirements-dev.txt

py.test
```

## Sources

Information on the phonological processes that underpin the app is from
Wikipedia
and
[Trask's Historical Linguistics](https://www.amazon.com/Trasks-Historical-Linguistics-Larry-Trask/dp/0340927658).
