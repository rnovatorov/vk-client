# `vk-client`

`vk-client` is a Python 2/3 high level VK API.


## Install

From PyPI:
```bash
pip install vk-client
```

From Github:
```bash
pip install git+https://github.com/Suenweek/vk-client#egg=vk-client
```

## Usage

```python
import vk_client

vk = vk_client.VkClient('YOUR_ACCESS_TOKEN')

for post in vk.Group(-1).get_posts():
    # Everyone likes cats, right?
    if 'cat' in post.text:
        post.like()
```
