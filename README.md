# rofi-gister

Rofi userscript to manage local copies of your gists created by [gister](https://github.com/weakish/gister).

I like using [Dash](https://kapeli.com/dash) to manage code snippets on OSX.  [Lepton](https://github.com/hackjutsu/Lepton) does a good job with managing the snippets, but accessing them leaves something to be desired when compared with Dash's expansion functionality.  I also like using Rofi for a variety of quick tasks, so I wrote this userscript.

![usage](assets/demo.gif)

## Dependencies

- [rofi](https://github.com/davatorium/rofi)
- [xclip](https://github.com/astrand/xclip)
- [gister](https://github.com/weakish/gister)
- [gist.rb](https://github.com/defunkt/gist)
- [jq](https://stedolan.github.io/jq/)
- [Python 3](https://www.python.org/)

## Usage

Prior to your first use, use gister to create a local copy of your repository in `~/.gists`.

Launch the userscript somehow (bind a key to it, launch it from rofi, etc.)

You can search the gist names and descriptions from the rofi window itself, or press `Alt`+`S` to execute a search of the snippet contents.

You can also refresh your local gists with `Alt`+`R`.
