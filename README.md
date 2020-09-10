# ✔ Who am I ?

### A convenient library to get our ip (real public ip or private ip).

## Tutorial

```bash
pip3 install ipaddress
```

```python
from ipaddress import get_my_ip

get_my_ip(IPType.WAN)

get_my_ip(IPType.LAN)

# the return type will be a list storing your ip.
```