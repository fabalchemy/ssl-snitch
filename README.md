# ssl-snitch

A [bpftrace](https://github.com/iovisor/bpftrace) script to detect processes
communicating over TLS with [OpenSSL](https://www.openssl.org/).

`ssl-snitch` can detect incoming and outgoing SSL traffic. It records every
successful TCP connection (`accept` or `connect`) and then _snitches_ when a
connection holder calls `SSL_write` or `SSL_read`.

The script relies on the assumption that your `libssl.so` copy lives in
`/usr/lib/x86_64-linux-gnu/`. However, this can be updated and extended to
detect more cryptography libraries. For example, Firefox uses its own `libnspr`
(probes for this library are provided in the script).

## ⚡️ Quickstart

1. [Install `bpftrace`](https://github.com/iovisor/bpftrace/blob/master/INSTALL.md)
   and grab a copy of `ssl-snitch`:

```console
sudo apt install bpftrace
git clone https://github.com/FabAlchemy/ssl-snitch.git
```

2. Run the script!

```console
$ cd ssl-snitch
$ sudo bpftrace ssl-snitch.bt # <port> to filter 

Attaching 8 probes...
Tracing TLS connections... Press Ctrl-C to exit

TIME      COMMAND  PID    DADDR           DPORT 
21:05:13  python   35457  1.1.1.1         443   
21:05:24  curl     35474  142.250.72.164  443   
```

## 👀 Tests

You need `make` and a working `python3` installation with
[`venv`](https://docs.python.org/3/tutorial/venv.html), as well as `curl` and
`openssl`. The test suite tries to connect to several servers with different
tools and checks the script output.

```console
$ make test
OK

$ make clean # optional
```
