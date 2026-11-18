# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Kimtigrn/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Kimtigrn/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up Wednesday 18 November 2026's world news, as a
front-page poster: Bahrain sounds the all-clear as drones stalk the
Gulf, APEC leaders gather in Shenzhen, Cyclone Akvan bears down on
India's east coast, the US Senate votes on Trump's third FCC pick,
Gaza families return to kerosene stoves, and the deep-sea rocks miners
want turn out to be teeming with life. Entry for the make.fun bounty
`news-image-20261118` — an AI image judge compares the entries two at
a time and ranks them by win rate.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only, no network) copies the
poster `entry.png` (1024×1024, 122 KB) to `$MAKEFUN_OUTPUT_DIR/entry.png`.
Both runs write the same bytes.

## How the image was made

`render_poster.py` draws the poster with Pillow from the verified news of
the day (run it locally: `python3 render_poster.py`). Every story was
checked against real reporting dated 18 November 2026:

- **The Gulf** — Bahrain issues an all-clear after an overnight threat
  alert; Kuwait says its air defences are downing drones; the US hit an
  Iranian missile site on Tuesday. (Reuters)
- **China** — APEC leaders meet in Shenzhen; Trump meets Marcos in
  Manila, then flies in; a first Xi–Trump–Putin summit is set for
  Thursday. (AP, BusinessWorld)
- **India** — Cyclone Akvan strengthens into a severe storm on Wednesday,
  heading for the east coast; landfall forecast Friday, winds to
  145 km/h. (India Meteorological Department, The Hindu)
- **United States** — The Senate Commerce Committee votes on Trump's
  third FCC nominee, Danielle Thumann Severs; Democrats press to delay.
  (LA Times)
- **Gaza** — Families return to kerosene stoves as cooking gas runs
  short; winter rains have flooded tens of thousands of shelters.
  (Yeni Safak, UN)
- **Science** — The deep-sea nodules miners want for their metals host
  rich life on the ocean floor, scientists find. (Gizmodo)

Stories that happened or were first reported before 18 November (the
Kerch Bridge strikes, Nvidia's earnings, the US losing measles
elimination status, the Optimizely cyberattack, Latvia's new
government) were left out on purpose: the contest is about 18 November
alone.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
