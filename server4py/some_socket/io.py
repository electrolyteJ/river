import io
f = io.StringIO("some initial text data")
f = io.BytesIO(b"some initial binary data: \x00\x01")
f = open("socket_client.py", "rb", buffering=0)  # raw io
print(type(f))
import os
