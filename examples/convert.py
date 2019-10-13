import argparse
import slmkiii


# Supported filetypes are currently json|js and syx|sysex

parser = argparse.ArgumentParser(
    description='Takes a given MkIII file and creates a new one',
)
parser.add_argument('input_filename')
parser.add_argument('output_filename')
args = parser.parse_args()

print "Opening {}...".format(args.input_filename)
# This is really all there is \/\/
template = slmkiii.Template(args.input_filename)
template.save(args.output_filename)
# /\/\
print "Created {}".format(args.output_filename)
