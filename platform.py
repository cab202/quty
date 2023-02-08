from platformio.public import PlatformBase

class QutyPlatform(PlatformBase):
    def is_embedded(self):
        return True
