if [ ! -d ".venv" ]; then
    virtualenv -p ~/.brew/bin/python3.7 .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
python setup.py build_ext --build-lib=module
