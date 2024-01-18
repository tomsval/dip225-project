import calendar_scraper
import calendar_sync


def main():
    calendar_scraper.CalendarScraper("grafiks.ics")
    calendar_sync.CalendarSync()


if __name__ == "__main__":
    main()
