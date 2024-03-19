# Custom Truth and Dare Bot

This is a somewhat easy to customize Truth and Dare bot. The truth and dares can also be integrated into other bots by
including `TruthDareCog` from `truthdare.py`.

The configuration for the included bot is simple: create a `config.json` file with the following:

```json
{
  "botToken": "tokenHere",
  "prefix": "if wanted, prefix here, else empty string"
}
```

Two files are used to add truths and dares, simply called `truths.txt` and `dares.txt`. Each line is a truth or a dare.
