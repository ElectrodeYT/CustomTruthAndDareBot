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

Truths and dares are seperated into categories; each category is a file in a folder called `truths` or `dares`. A
category may be present in either one of both of the types; that is to say you may have the same category in truths and
dares, or may have a category where you only have truths or dares.