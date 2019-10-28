virtualenv -p ~/.brew/bin/python3.7 .venv
source .venv/bin/activate
pip install -r requirements.txt
python setup.py build_ext --inplace
