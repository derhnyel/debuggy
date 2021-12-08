run:
    python setup.py install

setup: requirements.txt
    pip install -r requirements.txt

clean:
    rm -rf __pycache__
