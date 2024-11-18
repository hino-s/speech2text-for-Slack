# speech2text-for-Slack
## Introduction
- Article about this app in Japanese
-- https://qiita.com/hinosi/items/974d343f18e1ff81d2c3

  1. Create .env file in the same directory as docker-compose.yml
  2. Follow the tutorial of the Slack application to get the Slack API key, and get the OpenAI API key from the OpenAI site.
  - https://tools.slack.dev/bolt-python/ja-jp/getting-started
  - https://openai.com/index/openai-api/
  3. Writing to .env files
~~~
SLACK_SIGNING_SECRET=XXXXXXXXXXXXXX
SLACK_BOT_TOKEN=xoxb-XXXXXXXXXXXXXX
SLACK_APP_TOKEN=xapp-XXXXXXXXXXXXXX
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXX
~~~
4. Enter **docker compose up -d**
