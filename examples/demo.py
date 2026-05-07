# PyCodeDJ demo — run each block independently:
#   pycodedj eval examples/demo.py::bass
#   pycodedj eval examples/demo.py::melody
#   pycodedj eval examples/demo.py::pad

from pycodedj import loop


@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(8):
        if i % 2 == 0:
            pass


@loop("melody", interval=0.5)
def melody(volume=0.3):
    x = 1
    y = 2
    return x + y


@loop("pad", interval=4.0)
def pad(volume=0.15):
    # ここに余白を置く
    # もう少し置く
    # 静寂も音楽
    pass
