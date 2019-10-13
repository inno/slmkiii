import argparse
import slmkiii

# value storage is not
#
# data is scattered around the various parameters 


parser = argparse.ArgumentParser(description='ALL CCs ARE BECOME BACON')
parser.add_argument('input_filename')
parser.add_argument('output_filename')
args = parser.parse_args()

print "Opening {}...".format(args.input_filename)
template = slmkiii.Template(args.input_filename)

# ALL CCs ARE BECOME BACON
for knob in syx.knobs:
    if knob.message_type_name == 'CC':
        knob.name = 'Bacon {}'.format(knob.first_param)
for button in syx.buttons:
    if button.message_type_name == 'CC':
        button.name = 'Bacon {}'.format(button.fourth_param)
for fader in syx.faders:
    if fader.message_type_name == 'CC':
        fader.name = 'Bacon {}'.format(fader.second_param)
for pad_hit in syx.pad_hits:
    if pad_hit.message_type_name == 'CC':
        pad_hit.name = 'Bacon {}'.format(pad_hit.fourth_param)

template.save(args.output_filename)
print "Created {}".format(args.output_filename)
