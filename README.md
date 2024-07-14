# Message cleaner

--- 

Cleans-up redundant messages in chat.

Listens to redis queue (list) named `duck-duck:clean-up`.

Messages are in following structure:
`"{chat_id}:{message_id}"`

For example:
`"123456:789012"`

When message is received, it is split by `:` and first part is used to get chat id and second part is used to get
message id."`.

---

### How to run

1. Set up virtual environment python3.11 using poetry.
2. Install dependencies.
3. Create `config.toml` file in root directory.
4. Fill in the configuration by example.
5. Create `logging_config.json` file in root directory.
6. Fill in the logging configuration by example.
7. Run the `main.py` script.
