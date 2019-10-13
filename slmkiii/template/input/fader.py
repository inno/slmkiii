import struct
from slmkiii.template.input import Input


class Fader(Input):
    def __init__(self, data=None):
        super(Fader, self).__init__(data)
        self.channel = self._channel_wrapper(22)
        self.from_value = self.data(13, 2)
        self.to_value = self.data(15, 2)
        self.first_param = self.data(17)
        self.second_param = self.data(18)
        self.lsb_index = self.data(19)

    def from_dict(self, data):
        super(Fader, self).from_dict(data)
        self._data += struct.pack(
            '>BHHBBB',
            data['channel'],
            data['from_value'],
            data['to_value'],
            data['first_param'],
            data['second_param'],
            data['lsb_index'],
        )
        self._data = self._data.ljust(self.length, '\0')

    def export_dict(self):
        data = super(Fader, self).export_dict()
        data.update({
            'channel': self.channel,
            'from_value': self.from_value,
            'to_value': self.to_value,
            'first_param': self.first_param,
            'first_param_name': self.first_param_name,
            'second_param': self.second_param,
            'second_param_name': self.second_param_name,
            'lsb_index': self.lsb_index,
        })
        return data

    @property
    def first_param_name(self):
        param_names = {
            0: 'Eight Bit',
            1: 'Eight Bit',
        }
        if self.message_type in param_names:
            return param_names[self.message_type]
        return 'n/a'

    @property
    def second_param_name(self):
        param_names = {
            0: 'CC Index',
            1: 'MSB Index',
        }
        if self.message_type in param_names:
            return param_names[self.message_type]
        return 'n/a'
