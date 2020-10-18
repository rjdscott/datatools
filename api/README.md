# protobuf-example

This repository showcases how to implement a protocol buffer using python.

You will need to install the protoc compiler. On macOS this can be done via 
```
brew install protoc
```

You will also need to the following python library

```
pip install protobuf
```

In order to begin, you will need to define the schema in the `.poto` file.

Then you need to compile via the following command:

```
protoc -I=. --python_out=. ./todolist.proto
```

Once the file has been converted into the python-native metafile, 
you can simply use it as outlines in the `asset.py` file.