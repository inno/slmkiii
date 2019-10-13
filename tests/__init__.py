import tempfile
import slmkiii
import unittest
import slmkiii.template.sections as sections


class TestTemplate(unittest.TestCase):
    def assert_equal_templates(self, template1, template2):
        json1 = template1.export_json()
        json2 = template2.export_json()
        self.assertEqual(json1['name'], json2['name'])
        self.assertEqual(json1['version'], json2['version'])
        for sdata in sections:
            section = sdata['name']
            self.assertListEqual(json1[section], json2[section])
        json1 = template1.export_json(minify=True)
        json2 = template2.export_json(minify=True)
        self.assertEqual(json1['name'], json2['name'])
        self.assertEqual(json1['version'], json2['version'])
        for sdata in sections:
            section = sdata['name']
            self.assertListEqual(json1[section], json2[section])

    def test_parse_sysex_and_json_export(self):
        template1 = slmkiii.Template('tests/data/expected_1.json')
        template2 = slmkiii.Template('tests/data/test1.syx')
        self.assertDictEqual(template1.export_json(), template2.export_json())

    def test_parse_seven_bit_raw_and_json_export(self):
        with open('tests/data/test1.syx', 'rb') as r:
            raw = r.read()
        template1 = slmkiii.Template('tests/data/expected_1.json')
        template2 = slmkiii.Template(raw)
        self.assertDictEqual(template1.export_json(), template2.export_json())

    def test_parse_eight_bit_raw(self):
        with open('tests/data/test1.syx', 'rb') as r:
            raw = r.read()
        template1 = slmkiii.Template(raw)
        template2 = slmkiii.Template(template1._data)
        self.assertDictEqual(template1.export_json(), template2.export_json())

    def test_parse_invalid_sysex(self):
        with open('tests/data/test1.syx', 'rb') as r:
            raw = r.read()
        raw += 'uh oh'
        with self.assertRaises(slmkiii.errors.ErrorUnknownData):
            slmkiii.Template(raw)
        with self.assertRaises(slmkiii.errors.ErrorUnknownData):
            slmkiii.Template('wut')

    def test_sysex_export_sysex(self):
        template1 = slmkiii.Template('tests/data/expected_1.json')
        with open('tests/data/expected_1.syx', 'rb') as f:
            sysex = f.read()
        self.assertEqual(sysex, template1.export_sysex())

    def test_save_export_json(self):
        tf = tempfile.NamedTemporaryFile(suffix='.syx')
        template1 = slmkiii.Template('tests/data/expected_1.json')
        template1.save(tf.name, overwrite=True)
        template2 = slmkiii.Template(tf.name)
        with open('tests/data/expected_1.syx', 'rb') as f:
            sysex2 = f.read()
        self.assertEqual(template2.export_sysex(), sysex2)

    def test_save_json(self):
        tf = tempfile.NamedTemporaryFile(suffix='.json')
        template1 = slmkiii.Template('tests/data/test1.syx')
        template1.save(tf.name, overwrite=True)
        template2 = slmkiii.Template(tf.name)
        self.assertDictEqual(template1.export_json(), template2.export_json())

    def test_save_export_sysex(self):
        tf = tempfile.NamedTemporaryFile(suffix='.syx')
        template1 = slmkiii.Template('tests/data/expected_1.json')
        template1.save(tf.name, overwrite=True)
        with open(tf.name, 'rb') as f:
            sysex1 = f.read()
        with open('tests/data/expected_1.syx', 'rb') as f:
            sysex2 = f.read()
        self.assertEqual(sysex1, sysex2)

    def test_default_json(self):
        template1 = slmkiii.Template('tests/data/minimal_1.json')
        template2 = slmkiii.Template('tests/data/expected_2.json')
        self.assertDictEqual(template1.export_json(), template2.export_json())
        self.assertEqual(template1.knobs[0].message_type_name, 'CC')
        self.assertEqual(template1.knobs[0].short_message_type_name, 'CC')

    def test_invalid_extension(self):
        tf = tempfile.NamedTemporaryFile(suffix='.fail')
        with self.assertRaises(slmkiii.errors.ErrorUnknownExtension):
            slmkiii.Template(tf.name)

    def test_bad_import(self):
        with self.assertRaises(slmkiii.errors.ErrorTooManyItemsInSection):
            slmkiii.Template('tests/data/expected_bad_1.json')

    def test_minify_json(self):
        template1 = slmkiii.Template('tests/data/minimal_2.json')
        template2 = slmkiii.Template('tests/data/test2.syx')
        self.assert_equal_templates(template1, template2)

    def test_bad_json_version(self):
        with self.assertRaises(slmkiii.errors.ErrorUnknownVersion):
            slmkiii.Template('tests/data/bad_version.json')

    def test_bad_checksum(self):
        with self.assertRaises(slmkiii.errors.ErrorInvalidChecksum):
            slmkiii.Template('tests/data/bad_checksum.syx')

    def test_do_not_replace(self):
        tf = tempfile.NamedTemporaryFile(suffix='.syx')
        template = slmkiii.Template('tests/data/minimal_2.json')
        with self.assertRaises(slmkiii.errors.ErrorFileExists):
            template.save(tf.name, overwrite=True)
            template.save(tf.name)

    def test_create_new(self):
        tf = tempfile.NamedTemporaryFile(suffix='.syx')
        template1 = slmkiii.Template()
        template1.save(tf.name, overwrite=True)
        template2 = slmkiii.Template(tf.name)
        self.assert_equal_templates(template1, template2)
