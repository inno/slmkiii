import struct
from slmkiii.template.input import Input


class Button(Input):
    def __init__(self, data=None):
        super(Button, self).__init__(data)
        self.behavior = self.data(12)
        self.action = self.data(13)
        self.first_param = self.data(14, 2)
        self.second_param = self.data(16, 2)
        self.step = self.data(18, 2, signed=True)
        self.wrap = self.data(20, boolean=True)
        self.pair = self.data(21, boolean=True)
        self.channel = self._channel_wrapper(22)
        self.third_param = self.data(23)
        self.fourth_param = self.data(24)
        self.lsb_index = self.data(25)

    def from_dict(self, data, extend=False):
        super(Button, self).from_dict(data)
        # Interesting way of signing
        if data['step'] != 0:
            msb = (data['step'] + 8192) >> 7 & 127
            lsb = (data['step'] + 8192) & 127
        else:
            msb = 0
            lsb = 0

        self._data += struct.pack(
            '>BBHHBB??BBBB',
            data['behavior'],
            data['action'],
            data['first_param'],
            data['second_param'],
            msb,
            lsb,
            data['wrap'],
            data['pair'],
            data['channel'],
            data['third_param'],
            data['fourth_param'],
            data['lsb_index'],
        )
        if extend is False:
            self._data = self._data.ljust(self.length, '\0')

    def export_dict(self):
        data = super(Button, self).export_dict()
        data.update({
            'behavior': self.behavior,
            'action': self.action,
            'first_param': self.first_param,
            'first_param_name': self.first_param_name,
            'second_param': self.second_param,
            'second_param_name': self.second_param_name,
            'step': self.step,
            'wrap': self.wrap,
            'pair': self.pair,
            'channel': self.channel,
            'third_param': self.third_param,
            'third_param_name': self.third_param_name,
            'fourth_param': self.fourth_param,
            'fourth_param_name': self.fourth_param_name,
            'lsb_index': self.lsb_index,
        })
        return data

    @property
    def first_param_name(self):
        first_param_names = {
            0: 'Down Value',
            1: 'On Value',
            2: 'From Value',
            3: 'Trigger Value',
        }
        return first_param_names[self.behavior]

    @property
    def second_param_name(self):
        second_param_names = {
            0: 'Up Value',
            1: 'Off Value',
            2: 'To Value',
            3: 'n/a',
        }
        return second_param_names[self.behavior]

    @property
    def third_param_name(self):
        if self.message_type == 2:
            return 'Note'
        return 'n/a'

    @property
    def fourth_param_name(self):
        if self.message_type == 0:
            return 'CC Index'
        if self.message_type == 1:
            return 'MSB Index'
        return 'n/a'
