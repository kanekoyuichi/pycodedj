# PyCodeDJ demo — run each block independently:
#   pycodedj eval examples/demo.py::bass
#   pycodedj eval examples/demo.py::melody
#   pycodedj eval examples/demo.py::pad

# @loop bass interval=2.0
def bass():
    for i in range(8):
        if i % 2 == 0:
            pass

# @loop melody interval=0.5
def melody():
    x = 1
    y = 2
    return x + y

# @loop pad interval=4.0
# ここに余白を置く
# もう少し置く
# 静寂も音楽
def pad():
    pass
