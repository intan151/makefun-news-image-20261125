# The World in One Day — Tuesday, 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/intan151/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/intan151/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261125-blue)](https://make.fun)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](main.py)

One newspaper-style picture of the world's news on Wednesday,
25 November 2026, built from six stories that were each verified
against reputable reporting dated 25 November 2026:

1. Two oil tankers struck naval mines, exploded and caught fire in
   the Strait of Hormuz, Iran's Revolutionary Guards said. (Reuters)
2. Yemen's Houthis said they attacked Saudi Arabia's Ras Tanura oil
   refinery, the kingdom's largest, and Riyadh's financial district.
   (Reuters)
3. Drone strikes by Sudan's paramilitary Rapid Support Forces killed
   19 civilians and wounded 20 others in two cities. (Just Security)
4. Australia and Solomon Islands signed a security treaty making
   Canberra the islands' defence partner of choice, with a pledge of
   no foreign military base on their soil. (Reuters)
5. Colombian security forces stormed an Exito supermarket in
   Cartagena, freeing all remaining hostages after a day-long siege;
   one captor was killed. (Reuters)
6. China's Shenzhou-24 launched and docked with the Tiangong space
   station, carrying Muhammad Zeeshan Ali — the first Pakistani in
   orbit and the first foreigner aboard Tiangong. (Reuters)

`draw_news.py` renders the picture with Pillow on the build machine;
`main.py` (standard library only) copies the finished `entry.png`
into the grader's output directory. No photographs, no network calls.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png` — 1024×1024 PNG, byte-identical on
every run.
