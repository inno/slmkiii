import binascii
import json
import os
import struct
import slmkiii.errors
import slmkiii.utils as utils
from slmkiii.template.defaults import defaults
from slmkiii.template.sections import sections

version = 1.0


class Template:
    def __init__(self, data: str | bytes | None = None) -> None:
        self.name = ""
        for sdata in sections:
            setattr(self, sdata["name"], [])

        if data is None:
            self._new()
        elif len(data) == 3408:
            self._open_raw(data)
        elif len(data) == 4214:
            self._open_sysex(None, raw=data)
        elif (
            isinstance(data, str)
            and data.find("\0") != -1
            or isinstance(data, bytes)
            and data.find(b"\0") != -1
        ):
            raise slmkiii.errors.ErrorUnknownData()
        elif os.path.isfile(data):
            self._open_file(data)
        else:
            raise slmkiii.errors.ErrorUnknownData()

    def _open_file(self, filename: str) -> None:
        ftype = utils.file_type(filename)
        if ftype == "json":
            self._open_json(filename)
        elif ftype == "sysex":
            self._open_sysex(filename)

    def _new(self) -> None:
        data = self.patch_defaults({})
        data["version"] = version
        self._data_to_raw(data)

    def _open_json(self, filename: str) -> None:
        with open(filename, "rb") as jsonfile:
            data = self.patch_defaults(json.load(jsonfile))
        self._data_to_raw(data)

    def _data_to_raw(self, data: dict[str, ...]) -> None:
        # If we add more versions, fail hard instead of breaking old versions
        if data["version"] != version:
            raise slmkiii.errors.ErrorUnknownVersion(data["version"])

        # Header
        raw = struct.pack(
            ">4s16s", b"\x50\x0d\x00\x00", data["name"].encode("utf-8")
        )

        for sdata in sections:
            for item in data[sdata["name"]]:
                raw += sdata["class"](item)._data

        self._open_raw(raw)

    def _open_sysex(
        self,
        filename: str | None,
        raw: bytes | None = None,
    ) -> None:
        if raw is None:
            with open(filename, "rb") as sysexfile:
                raw = sysexfile.read()

        checksum = 0
        data = b""
        for chunk in raw[1:-1].split(b"\xf7\xf0"):
            block_type = chunk[6]
            if block_type == 1:
                data = b""
            elif block_type == 2:
                raw_chunk = utils.seven_to_eight(chunk[17:])
                data += raw_chunk
                checksum = binascii.crc32(raw_chunk, checksum) & 0xFFFFFFFF
            elif block_type == 3:
                if checksum != utils.nibbles_to_bytes(chunk[17:]):
                    raise slmkiii.errors.ErrorInvalidChecksum()
        self._open_raw(data)

    def _open_raw(self, data: bytes) -> None:
        ofst = 20  # header length
        block_length = 44
        self._data = data
        self._header = self._data[:ofst]
        self.name = self._header[4:17].rstrip(b"\0").rstrip().decode("utf-8")
        self._body = self._data[ofst:]

        for sdata in sections:
            items = []
            for _ in range(sdata["items"]):
                items.append(sdata["class"](data[ofst : ofst + block_length]))
                ofst += block_length
            setattr(self, sdata["name"], items)

    def patch_defaults(self, data: dict[str, ...]) -> dict[str, ...]:
        for sdata in sections:
            section = sdata["name"]
            if section not in data:
                data[section] = []
            if len(data[section]) > sdata["items"]:
                raise slmkiii.errors.ErrorTooManyItemsInSection(
                    section,
                    len(data[section]),
                    sdata["items"],
                )
            elif len(data[section]) < sdata["items"]:
                needed = sdata["items"] - len(data[section])
                data[section] += [defaults[section] for _ in range(needed)]
            new_structure = []
            for item in data[section]:
                new_item = defaults[section].copy()
                new_item.update(item)
                new_structure.append(new_item)
            data[section] = new_structure
        for k in ("name", "version"):
            if k not in data:
                data[k] = defaults[k]
        return data

    def save(
        self,
        filename: str,
        minify: bool = False,
        overwrite: bool = False,
    ) -> None:
        ftype = utils.file_type(filename)
        if overwrite is False:
            if os.path.exists(filename):
                raise slmkiii.errors.ErrorFileExists(filename)
        if ftype == "json":
            self.export_json(filename, minify)
        elif ftype == "sysex":
            self.export_sysex(filename)

    def export_sysex(self, filename: str | None = None) -> bytes:
        header = struct.pack(">7B", 240, 0, 32, 41, 2, 10, 3)
        data = header + struct.pack(">B2L4B", 1, 0, 0, 2, 0, 1, 247)

        # Data
        block = 0
        checksum = 0
        while (block * 256) <= len(self._data):
            chunk = self._data[block * 256 : (block + 1) * 256]
            checksum = binascii.crc32(chunk, checksum) & 0xFFFFFFFF
            encoded_data = utils.eight_to_seven(chunk)
            data += header
            data += struct.pack(
                f">B2L2B{len(encoded_data)}sB",
                2,
                0,
                block + 1,
                2,
                0,
                encoded_data,
                247,
            )
            block += 1

        # Footer/crc
        data += header
        encoded_checksum = utils.bytes_to_nibbles(checksum)
        data += struct.pack(">B2L2B8sB", 3, 0, 15, 2, 0, encoded_checksum, 247)

        if filename is not None:
            with open(filename, "wb") as sysexfile:
                sysexfile.write(data)

        return data

    def export_json(
        self,
        filename: str | None = None,
        minify: bool = False,
    ) -> dict[str, ...]:
        data = {x["name"]: [] for x in sections}

        for sdata in sections:
            items = getattr(self, sdata["name"])
            for item in items:
                data[sdata["name"]].append(item.export_dict())

        data["name"] = self.name
        data["version"] = version
        data["-NOTES-"] = (
            "*_param_name fields are for reference and are not editable",
            "Many fields are used/unused based on behavior or message_type",
        )

        if minify:
            for sdata in sections:
                new_structure = []
                for item in data[sdata["name"]]:
                    for key, value in defaults[sdata["name"]].items():
                        if item[key] == value:
                            item.pop(key)
                    for key in list(item.keys()):
                        if key[-11:] in ("_param_name", "method_name"):
                            item.pop(key)
                    new_structure.append(item)
                data[sdata["name"]] = new_structure

        if filename is not None:
            with open(filename, "w") as jsonfile:
                json.dump(
                    data,
                    jsonfile,
                    indent=4,
                    sort_keys=True,
                    default=lambda x: x.decode("utf-8"),
                    separators=(",", ": "),
                )

        return data
