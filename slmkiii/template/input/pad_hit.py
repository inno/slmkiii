import struct
from slmkiii.template.input.button import Button


class PadHit(Button):
    def __init__(self, data=None):
        super(PadHit, self).__init__(data)
        self.max_velocity = self.data(28)
        self.min_velocity = self.data(29)
        self.range_method = self.data(30)

    def from_dict(self, data):
        super(PadHit, self).from_dict(data, extend=True)
        self._data += struct.pack(
            '>HBBB',
            0,
            data['max_velocity'],
            data['min_velocity'],
            data['range_method'],
        )
        self._data = self._data.ljust(self.length, '\0')

    def export_dict(self):
        data = super(PadHit, self).export_dict()
        data.update({
            'max_velocity': self.max_velocity,
            'min_velocity': self.min_velocity,
            'range_method': self.range_method,
            'range_method_name': self.range_method_name,
        })
        return data

    @property
    def range_method_name(self):
        method_names = {
            0: 'None',
            1: 'Clip',
            2: 'Scale',
        }
        return method_names[self.data(30)]
