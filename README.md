# Cream

Cream is a creamy language.

## Requirements

* Python 2.7.x

## How to run or compile

1 Get this repository:
```bash
git clone https://github.com/tattn/cream
```

2 Change directory:
```bash
cd cream
```

3 Install libraries
```bash
pip install -r requirements.txt
```

4-1 Run on Python
```bash
./cream.py examples/hello.crm
```

4-2-1 Compile
```bash
python rpython --output cream target.py
```

4-2-2 Run as a native code
```bash
./cream examples/hello.crm
```

