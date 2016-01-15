# Cream

Cream is a creamy language.

## Requirements

* Python 2.7.x

## How to run

### 1. Get this repository:
```bash
cd $WORK_DIR
git clone https://github.com/tattn/cream
cd cream
```

### 2. Install libraries
```bash
pip install -r requirements.txt
```

### 3. Run on Python
```bash
./cream.py examples/hello.crm
```

## How to compile

### 1. Get the pypy
```bash
cd $WORK_DIR
hg clone https://bitbucket.org/pypy/pypy
```

### 2. Compile
```bash
cd cream
python ../pypy/rpython target.py
```

### 3. Run as a native code
```bash
./cream examples/hello.crm
```

