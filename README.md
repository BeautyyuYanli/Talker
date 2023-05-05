# Talker

Virtual talker powered by GPT-3.5

![image](https://user-images.githubusercontent.com/32453863/223974799-603f9673-6ad1-4595-a6ce-b201a83d1cce.png)

## Setup

Modify `docker-compose.yml` to set your OpenAI API key.

```
- OPENAI_API_KEY=<your-openai-kay>
```

Then 
```
docker-compose up -d
```

## Usage

Open http://localhost:5000/?model=default

or HTTP API:
```
curl "http://localhost:5000/gen_msg?model=default&id=default" -X POST -d "你好"
```

The parama `id` can be any string to identify the `talker`, with its own memory.

## Advanced

Define your talker in the folder `models/yourmodel.json` and use it by visit http://localhost:5000/?model=yourmodel

## Other

Distributed using [GPLv3](LICENSE)
