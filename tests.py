from emulator import Emulator


outputs = []
emu = Emulator(None, 'C:/Users/anton/Desktop/config-1/VFS.tar', 'C:/Users/anton/Desktop/config-1/log.xml', ' C:/Users/anton/Desktop/config-1/Start.txt')
emu.Output = lambda message: outputs.append(message)
emu.UpdateInput = lambda: None

# TREE
emu.path = []
emu.command = 'tree'
emu.Emu()

assert outputs == ['├───root\n', '│   ├───dir_1\n', '│   │   └───1.txt\n', '│   │   └───2.txt\n',  '│   ├───dir_2\n', '│   │   └───11.txt\n', '│   ├───dir_3\n', '│   └───text.txt\n', '4 directories 4 files\n']

# LS
outputs = []
emu.path = ['root']
emu.command = 'ls'
emu.Emu()

emu.path = ['root', 'dir_2']
emu.command = 'ls'
emu.Emu()

emu.path = ['root', 'dir_3']
emu.command = 'ls'
emu.Emu()

assert outputs == ['dir_1 ', 'dir_2 ', 'dir_3 ', 'text.txt ', '\n', '11.txt ', '\n', '\n']

# CD
outputs = []
emu.path = []
emu.command = 'cd root'
emu.Emu()

assert emu.path == ['root']

outputs = []
emu.path = []
emu.command = 'cd /'
emu.Emu()

assert emu.path == []

outputs = []
emu.path = []
emu.command = 'cd root/dir_3'
emu.Emu()

assert emu.path == ['root', 'dir_3']

# RMDIR
outputs = []
emu.path = ['root']
emu.command = 'rmdir dir_3'
emu.Emu()

assert outputs == ['rmdir: removing directory, "dir_3"\n']

outputs = []
emu.path = ['root']
emu.command = 'rmdir dir_3'
emu.Emu()

assert outputs == ['rmdir: failed to remove "dir_3": Directory is not exist\n']

outputs = []
emu.path = ['root']
emu.command = 'rmdir dir_2'
emu.Emu()

assert outputs == ['rmdir: failed to remove "dir_2": Directory is not empty\n']

print('OK')