from slmkiii.template.input.button import Button
from slmkiii.template.input.fader import Fader
from slmkiii.template.input.knob import Knob
from slmkiii.template.input.pad_hit import PadHit


sections = [
    {
        'class': Button,
        'items': 16,
        'name': 'buttons',
    },
    {
        'class': Knob,
        'items': 16,
        'name': 'knobs',
    },
    {
        'class': Fader,
        'items': 8,
        'name': 'faders',
    },
    {
        'class': Fader,
        'items': 2,
        'name': 'wheels',
    },
    {
        'class': Fader,
        'items': 2,
        'name': 'pedals',
    },
    {
        'class': Button,
        'items': 1,
        'name': 'footswitches',
    },
    {
        'class': PadHit,
        'items': 16,
        'name': 'pad_hits',
    },
    {
        'class': Fader,
        'items': 16,
        'name': 'pad_pressures',
    },
]
