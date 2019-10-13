import struct
from slmkiii.template.input import Input


class Knob(Input):
    def __init__(self, data=None):
        super(Knob, self).__init__(data)
        self.first_param = self.data(12)
        self.lsb_index = self.data(13)
        self.relative = self.data(14)
        self.eight_bit = self.data(15)
        self.pivot = self.data(16, 2)
        self.step = self.data(18)
        self.resolution = self.data(19, 2)
        self.channel = self._channel_wrapper(22)
        self.from_value = self.data(22, 2)
        self.to_value = self.data(24, 2)

    def from_dict(self, data):
        super(Knob, self).from_dict(data)
        self._data += struct.pack(
            '>BBBBHBHBHH',
            data['first_param'],
            data['lsb_index'],
            data['relative'],
            data['eight_bit'],
            data['pivot'],
            data['step'],
            data['resolution'],
            data['channel'],
            data['from_value'],
            data['to_value'],
        )
        self._data = self._data.ljust(self.length, '\0')

    def export_dict(self):
        data = super(Knob, self).export_dict()
        data.update({
            'first_param': self.first_param,
            'first_param_name': self.first_param_name,
            'lsb_index': self.lsb_index,
            'relative': self.relative,
            'eight_bit': self.eight_bit,
            'pivot': self.pivot,
            'step': self.step,
            'resolution': self.resolution,
            'channel': self.channel,
            'from_value': self.from_value,
            'to_value': self.to_value,
        })
        return data

    @property
    def first_param_name(self):
        param_names = {
            0: 'CC Index',
            1: 'MSB Index',
            2: 'Velocity',
        }
        if self.message_type in param_names:
            return param_names[self.message_type]
        return 'n/a'
