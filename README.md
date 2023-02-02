# Leek Modding Tools<br>[![GitHub Actions][actions-img]][actions-url] [![Patreon][patreon-img]][patreon-url] [![PayPal][paypal-img]][paypal-url] [![Discord][discord-img]][discord-url]

> WARNING: Please note that Leek is an experimental work in progress project, and as such, the API might change unexpectedly at any time.

This is a simple extension for Leek that adds a bunch of modding related tools for modding communities.

Right now, it comes with the following cogs:

- `leek_modding:Rage`: Tools Grand Theft Auto V, FiveM and Red Dead Redemption 2 like Native Lookup
- `leek_modding:Diagnoser`: A simple(ish) Cog that helps with the diagnostic of game problems from SHVDN log files

## Download

* [GitHub Releases](https://github.com/LeekByLemon/LeekModding/releases)
* [GitHub Actions](https://github.com/LeekByLemon/LeekModding/actions) (experimental versions)

## Installation

Run the following command to install the latest version of Tags Extension from master.

```
pip install https://github.com/LeekByLemon/LeekModding/archive/master.zip
```

If you want to install from git for developent purposes, run the following commands:

```
git clone https://github.com/LeekByLemon/LeekModding.git leek
cd leek
pip install -e .
```

## Usage

To add the cog to Leek, add any of the Cogs provided by the mod to your `DISCORD_COGS` environment variable in your `.env` file.

[actions-img]: https://img.shields.io/github/actions/workflow/status/LeekByLemon/LeekModding/main.yml?branch=master&label=actions
[actions-url]: https://github.com/LeekByLemon/LeekModding/actions
[patreon-img]: https://img.shields.io/badge/support-patreon-FF424D.svg
[patreon-url]: https://www.patreon.com/lemonchan
[paypal-img]: https://img.shields.io/badge/support-paypal-0079C1.svg
[paypal-url]: https://paypal.me/justalemon
[discord-img]: https://img.shields.io/badge/discord-join-7289DA.svg
[discord-url]: https://discord.gg/Cf6sspj
