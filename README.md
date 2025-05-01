![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Fly.io](https://img.shields.io/badge/deployed-Fly.io-orange.svg)

# HUR Support Bot
A Telegram bot built with Python and the `aiogram` library, deployed on Fly.io. The bot provides support functionality (e.g., handling user queries, providing directions) and uses a modular structure for maintainability.

## Features
- 📩 Responds to user commands and messages via Telegram.
- 🗂️ Organized into modules (`bot/`, `config/`, `texts/`) for clean code structure.
- ☁️ Deployed on Fly.io for scalable hosting.
- 📜 Logs application events for debugging (written to stdout for Fly.io logs).

## Prerequisites
- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **Telegram Bot Token**: Obtain from [BotFather](https://t.me/BotFather) on Telegram.
- **Fly.io Account and CLI**: Sign up at [Fly.io](https://fly.io/) and install `flyctl` ([Installation Guide](https://fly.io/docs/getting-started/installing-flyctl/)).
- **Git**: Required to clone the repository ([Install Git](https://git-scm.com/downloads)).

## Getting Started
1. **Clone the Repository**:
```
git clone https://github.com/<your-username>/hur-support-bot.git
cd hur-support-bot
```


2. **Install Dependencies:** Create a virtual environment and install the required packages:
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```


3. **Set Environment Variables:** Create a `.env` file in the root directory with your Telegram bot token:
```
BOT_TOKEN=your-telegram-bot-token
```
> _**Note:** Ensure `.env` is listed in `.gitignore` to avoid committing sensitive data._

4. **Test Locally:** Run the bot locally to ensure it works:
```
python main.py
```
Interact with your bot on Telegram to verify functionality.


## Deployment on Fly.io
1. **Set Up Fly.io**
   - Log in to Fly.io:
   ```
   flyctl auth login
   ```
   - The app is already configured in `fly.toml`. Verify the app name (`hur-support-bot`) matches your Fly.io app.


2. **Set Fly.io Secrets**
    
    Set your `BOT_TOKEN` and other environmental variables as Fly.io secrets:
    ```
    flyctl secrets set BOT_TOKEN=your-telegram-bot-token -a hur-support-bot
   ```

3. **Scale to One Machine**

    Ensure only one machine runs to avoid Telegram API conflicts:
    ```
   flyctl scale count 1 -a hur-support-bot
   ```

4. **Deploy the Application**
   
    Deploy the bot to Fly.io: 
     ```
     flyctl deploy -a hur-support-bot
     ```

5. **Monitor Logs**

   Check the logs to ensure the bot is running:
    ```
    flyctl logs -a hur-support-bot
      ```


## Project Structure

| File/Directory     | Description                                                                                       |
|--------------------|---------------------------------------------------------------------------------------------------|
| `bot/`             | Core bot logic, including handlers (`start.py`, `direction.py`) and database utilities (`db.py`). |
| `config/`          | Configuration files (e.g., `config.py` to load `BOT_TOKEN`).                                      |
| `texts/`           | Static text or message templates for the bot.                                                     |
| `main.py`          | Entry point of the application, initializes the bot and starts polling.                           |
| `requirements.txt` | List of Python dependencies (e.g., `aiogram`).                                                    |
| `fly.toml`         | Fly.io configuration file.                                                                        |
| `Procfile`         | Defines the worker process for Fly.io (`worker: python main.py`).                                 |
| `.dockerignore`    | Excludes files from Docker builds (if used).                                                      |
| `.gitignore`       | Excludes sensitive or generated files (e.g., `.env`, `bot.log`).                                  |


## Troubleshooting

- **Bot Exits Immediately:**
  - Check logs with `flyctl logs -a hur-support-bot`.
  - Ensure `BOT_TOKEN` is set correctly with `flyctl secrets list`.
  - Verify only one machine is running with `flyctl machines list`.


- **TelegramConflictError:**
  - Ensure only one bot instance is running (locally or on Fly.io).
  - Scale to one machine if needed with `flyctl scale count 1`.


- **Database Issues:**
  - Ensure connection details are set in Fly.io secrets.


## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and test locally.
4. Commit your changes: `git commit -m "Add your feature"`
5. Push to your fork: `git push origin feature/your-feature`
6. Open a pull request on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for details.