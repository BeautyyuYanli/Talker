# Talker

Virtual talker powered by GPT-3.5

![image](https://user-images.githubusercontent.com/32453863/223974799-603f9673-6ad1-4595-a6ce-b201a83d1cce.png)

## Setup

```
OPENAI_API_KEY=<your API key> flask -A server:app
```

You can also set your proxy API domain
```
OPENAI_API_BASE=<your API base domain, by default api.openai.com> 
```

## Usage

Open http://localhost:5000/?model=default

or HTTP API:
```
curl "http://localhost:5000/gen_msg?model=default" -X POST -d "你好"
```

## More API

See [server.py](server.py)

## Advanced

Define your talker in the folder `models/yourmodel.json` and use it by visit http://localhost:5000/?model=yourmodel

The name of the model should not contain underscore.

## Other

Distributed using [GPLv3](LICENSE)
