# Netcopy Checksum

The clients sends a message to the server, which forwards it to the checksum server for verification. The client can create and delete verified message blocks.

## Usage

Start checksum server

```bash
python checksum_server.py 127.0.0.1 8891
```

Start netcopy server

```bash
python netcopy_server.py 127.0.0.1 8890 127.0.0.1 8891 1852 ./receieved.txt
```

Send message with client

```bash
python netcopy_client.py 127.0.0.1 8890 127.0.0.1 8891 1852 ./message.txt
```
