# libslmkiii

libslmkiii is a Python library to alter Novation SL MkIII files programatically.

## Installation

Nothing yet, PyPI package Coming Soon™

## Why?

The Novation Components interface is a great tool for quick updates, but the point-and-click interface is tedious.  I have more gear that I care to admit and creating templates via the UI got unruly very quick. This allows much faster editing of SL MkIII templates either programmatically or via any text editor that can handle JSON.

I probably could have point-and-clicked all of the templates I needed in the time I wrote this, but I love a good data deep-dive. Hopefully someone else can benefit as well.

## Usage

### From Scratch
Create a blank file:
```python
import slmkiii

template = slmkiii.Template()
template.save('my_new_template.json')
```

Edit `my_new_template.json` to your hearts content, then convert to sysex template file:
```python
import slmkiii

template = slmkiii.Template('my_new_template.json')
template.save('my_new_template.syx')
```

Import into the Novation Components utility and send to your SL MkIII!

### Examples
See `examples/`

### Testing

Simple unittest
`python -m unittest test`

Code coverage
`coverage run -m unittest tests && coverage report -m`

### Future

* PyPi release
* Remove manual utility step with push/pull via MIDI

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate. This has 100% coverage, barring lookup table hackery and the like. As the spec can change at any moment, please keep the coverage as high as possible!

## License

Tl;dr: Do whatever you want with it and I'd appreciate a shoutout. Don't blame me if your gear bursts into flames, though.

MIT License

Copyright (c) 2019 inno

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
