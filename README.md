# pypltagent-eth

Python pltagent, allowing PLT to control an SBC/PC over Ethernet

- IPv6 Link-Local , port 8080

## POST

```json
{
   "command": "prog.sh"
}

```json
{
   "command: "prog.sh",
   "retval": 13,
   "stdout": ["line1", "line2"],
   "stderr": [].
   "status": "completed",
   "passFail": "PASS"
}
```

## PUT

- ``uploads`` folder

## Local build

```
$ docker run --rm -v $(pwd):/app -w /app python:3 bash -c "pip install flake8 && flake8 ."
```

