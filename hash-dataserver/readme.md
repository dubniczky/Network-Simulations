# Hash Dataserver

A dataserver returning data based on it's hash. A user can add a new piece of data to the server storage, then request it later using it's hash. If the hash has no corresponding data in the storage an error is returned instead.

## Usage

Start data server

> IP address 0.0.0.0 means any ip address

```bash
python dataserver.py 0.0.0.0 8080
```

Connect to the server with the client

> IP address 127.0.0.1 is a loopback address

```bash
python client.py 127.0.0.1 8080
```
