# mfa
Time based tokens directly on your terminal


# Getting started
- Copy the `.env_sample` file to a `.env`
- Erase the dumb keys in there and insert yours
- Create a python venv and install the dependencies (`poetry install`)
- run a `python main.py get_code <key>` with your key to get one code


# Using it everywhere
- run `python main.py gen_scripts` to generate one executable for each token
- copy all those scripts to ~/.local/bin/
- just use `mfa_key` in any terminal to get your code both on the screen and on the clipboard
