# Pingtrace

Issue ping and tracert commands on a list of domains from a csv using sync or async methods.

Generally, it's recommended to use the async version, since it's faster, unless the order of the calls is important.

## Usage

Ping async:

```bash
python pingtrace-async.py sites.csv
```

Ping sync:

```bash
python pingtrace-sync.py sites.csv
```
