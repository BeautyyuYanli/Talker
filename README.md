# Talker

Virtual talker powered by GPT-3.5

![image](https://user-images.githubusercontent.com/32453863/223974799-603f9673-6ad1-4595-a6ce-b201a83d1cce.png)

## Setup

```
env OPENAI_API_KEY=<your API key> flask -A server:app
```

## Usage

Open http://localhost:5000/?model=default

## Advanced

Define your talker in the folder `save/your_model` and use it by visit http://localhost:5000/?model=your_model

## Other

Distributed using [GPLv3](LICENSE)
