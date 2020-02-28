# Script to auto renew/confirm noip.com free hosts

[noip.com](https://www.noip.com/) free hosts expire every month.
This script auto click web pages to renew the hosts,
using Python/Selenium with Chrome headless mode.

- Platform: Debian/Ubuntu Linux, no GUI needed (tested on Debian 9.x/10.x); 3.x
- Author: loblab
- Refactor: SeGarVi

![noip.com hosts](https://raw.githubusercontent.com/loblab/noip-renew/master/screenshot.png)

## Usage

1. Set your noip.com account info and number of hosts in noip-renew.sh,
2. Run setup.sh,
3. Run noip-renew.sh, check result.png (if succeeded) or error.png (if failed)

For docker users, check Dockerfile, docker-compose.yml, crontab-docker-host.

### For local logging

Check confirmed records from multiple log files:

``` bash
grep -h Confirmed *.log | grep -v ": 0" | sort
```

### For Telegram notifications

Since local logging is good but you have to check the result actively, a Telegram Bot notifier is also available. It uses the Telegram Send library.

To configure your own bot and make the script use it, please refer check the [Telegram Send page in Pypi](https://pypi.org/project/telegram-send/).

## Remarks

The script is not designed to renew/update the dynamic DNS records.
Check [noip.com document](https://www.noip.com/integrate) for that purpose.
And most wireless routers support noip.com.
You can also check [DNS-O-Matic](https://dnsomatic.com/) to update multiple noip.com DNS records.

## History

- 0.5  (1/5/2020): Support raspberry pi, try different "chromedriver" packages in setup script.
- 0.4 (1/14/2019): Add num_hosts argument, change for button renaming; support user agent.
- 0.3 (5/19/2018): Support Docker, ignore timeout, support proxy, tested on python3.
- 0.2 (11/12/2017): Deploy the script as normal user only. root user with 'no-sandbox' option is not safe for Chrome.
- 0.1 (11/5/2017): Support Debian with Chrome headless.
