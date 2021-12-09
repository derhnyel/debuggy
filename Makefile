setup: requirements.txt
    pip install -r requirements.txt

run:
    python setup.py install

clean:
    rm -rf __pycache__

