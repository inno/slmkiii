import struct


class Input:
    def __init__(self, data: dict[str, ...] | bytes | None = None) -> None:
        self.length = 44
        if isinstance(data, bytes):
            self._data = data[: self.length]
        elif isinstance(data, dict):
            self.from_dict(data)

        self.enabled = self.data(0, boolean=True)
        self.name = self.data(1, 9).rstrip(b"\0").rstrip()
        self.message_type = self.data(10)

    def _channel_wrapper(self, offset: int) -> str | int:
        if self.data(offset) == 127:
            return "default"
        return self.data(offset) + 1

    def data(
        self,
        offset: int,
        length: int = 1,
        boolean: bool = False,
        signed: bool = False,
    ) -> int | bytes | bool:
        value = self._data[offset : offset + length]
        if length > 2:
            return value
        elif length == 2:
            if signed:
                return struct.unpack(">h", value)[0]
            else:
                return struct.unpack(">H", value)[0]
        if boolean:
            return bool(ord(value))
        return ord(value)

    def from_dict(self, data: dict[str, ...]) -> None:
        if "channel" in data:
            if data["channel"] == "default":
                data["channel"] = 127
            else:
                data["channel"] -= 1
        self._data = struct.pack(
            ">?9sBB",
            data["enabled"],
            data["name"].encode("utf-8"),
            data["message_type"],
            0,
        )

    def export_dict(self) -> dict[str, ...]:
        return {
            "enabled": self.enabled,
            "name": self.name,
            "message_type": self.message_type,
        }

    @property
    def message_type_name(self) -> str:
        message_type_names = (
            "CC",
            "NRPN",
            "Note",
            "Program Change",
            "Song Position",
            "Channel Pressure",
            "Poly Aftertouch",
        )
        return message_type_names[self.message_type]

    @property
    def short_message_type_name(self) -> str:
        short_names = ("CC", "NRPN", "Not", "PCh", "SP", "ChP", "PA")
        return short_names[self.message_type]
