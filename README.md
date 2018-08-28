# `vk-client`

`vk-client` is a Python 2/3 high level VK API.


## Install

```bash
pip install vk-client
```

## Usage

```python
import vk_client

vk = vk_client.VkClient('YOUR_ACCESS_TOKEN')

for post in vk.Group(-1).get_posts():
    if 'cat' in post.text:
        post.like()
```
