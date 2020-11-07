<h1>Blisscribe</h1>

Blisscribe is a translator designed for visual reading, allowing you to input text and receive a PDF with selected words replaced with Blissymbols.


<h2>Setup</h2>

Check out the repo, and get started using Pipenv.

```bash
pipenv install .
pipenv run makemigrations
pipenv run migrate
pipenv run server
```

Then open up `http://localhost:8000/translate/` and translate to Bliss!


<h2>Translation</h2>

After setting up Blisscribe, you can translate either from command line, Python, or online.

<h3>Command Line</h3>

Open blisscribe-master in command line and enter the prompt:

> cd bliss_online/bliss_webapp/translation

Then run blisscript.py with your version of Python:

> python blisscript.py

This will run a prompt asking which language and text you wish to translate.  To change the script simply modify blisscript.py.

<h3>Python</h3>

To translate in Python, head to the [translation folder](https://github.com/coraharmonica/blisscribe/tree/master/bliss_online/bliss_webapp/translation), located under bliss_online/bliss_webapp.  From here you can edit the demo.py file to translate demo text or some of your own.  Any text you translate will appear as a PDF in the out folder.

<h2>Features</h2>

Blisscribe currently supports the following languages:
- English
- Spanish
- German
- French
- Italian
- Dutch
- Polish
- Swedish
- Portuguese
- Danish


![alice en sample](https://github.com/coraharmonica/blisscribe/blob/master/bliss_online/bliss_webapp/translation/sample%20translations/alice%20en%20sample.png?raw=true)

***

![alice pl sample](https://github.com/coraharmonica/blisscribe/blob/master/bliss_online/bliss_webapp/translation/sample%20translations/alice%20pl%20sample.png?raw=true)


Blisscribe also provides options for users to select which parts of speech to translate, including nouns, verbs, adjectives/adverbs, and/or all parts of speech.

![nouns](https://github.com/coraharmonica/blisscribe/blob/master/bliss_online/bliss_webapp/translation/sample%20translations/quickbrownfox_nouns.png?raw=true)

***

![verbs](https://github.com/coraharmonica/blisscribe/blob/master/bliss_online/bliss_webapp/translation/sample%20translations/quickbrownfox_verbs.png?raw=true)

***

![adjs/advs](https://github.com/coraharmonica/blisscribe/blob/master/bliss_online/bliss_webapp/translation/sample%20translations/quickbrownfox_adjs.png?raw=true)

***

![other](https://github.com/coraharmonica/blisscribe/blob/master/bliss_online/bliss_webapp/translation/sample%20translations/quickbrownfox_other.png?raw=true)


Blisscribe is currently maintained in Python 3.6 (as of 06/22/2018).
To learn more about Blisscribe, visit the website:  blisscribe.tumblr.com.  You can also contact me through Blisscribe at blisscribe [at] gmail [dot] com.
