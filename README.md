# pypltagent-eth

Python pltagent, allowing PLT to control an SBC/PC over Ethernet

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

©2025 Blue Clover Devices - ALL RIGHTS RESERVED

[![CI](https://github.com/bcdevices/pypltagent-eth/actions/workflows/ci.yml/badge.svg)](https://github.com/bcdevices/pypltagent-eth/actions/workflows/ci.yml)

- IPv6 Link-Local , port 8080

## Installation (.deb)

```console
operator@progpc:~$ sudo apt install -y ./pypltagent-0.1.4.noarch.deb
:
Preparing to unpack .../pypltagent-0.1.4.noarch.deb ...
Unpacking pypltagent (1.0) ...
Setting up pypltagent (1.0) ...
Created symlink /etc/systemd/system/multi-user.target.wants/pypltagent.service → /usr/lib/systemd/system/pypltagent.service.
pypltagent service installed and started.
OK
:
operator@progpc:~$
```

## Command Line Usage

```
usage: pypltagent-eth.py [-h] [--host HOST] [--port PORT]
                         [--upload-folder UPLOAD_FOLDER]

pypltagent-eth

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           The host to listen on (default: '::')
  --port PORT           The port to listen on (default: 8080)
  --upload-folder UPLOAD_FOLDER
                        The folder to save uploaded files (default: 'uploads')
```

## POST

Command:

```json
{
   "command": "prog.sh"
}
```

Response:

```json
{
   "command": "prog.sh",
   "retval": 13,
   "stdout": ["line1", "line2"],
   "stderr": [],
   "status": "completed",
   "passFail": "PASS"
}
```

## PUT

- ``uploads`` folder

## Local build

```console
$ docker run --rm -v $(pwd):/app -w /app python:3 bash -c "pip install flake8 && flake8 ."
```

```console
$ docker run --rm -v "$(pwd):/app" python:3 bash -c "pip install autopep8 && autopep8 --in-place --recursive /app"
```
