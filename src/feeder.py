import bot
import api




def main() -> None:
    proc = api.start_server(bot.queue)
    bot.start_bot()
    proc.terminate()

if __name__ == "__main__":
    main()