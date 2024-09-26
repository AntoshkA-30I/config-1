import tarfile
import tkinter as tk
from tkinter import filedialog
import xml.etree.cElementTree as ET
import datetime
import argparse


class Emulator:
    def __init__(self, master):
        self.master = master
        self.path = [] # текущий путь

#------ terminal keys
        parser = argparse.ArgumentParser()
        parser.add_argument("VFS_path", help="Введите путь до архива VFS", type=str)
        parser.add_argument("Log_path", help="Введите путь до Log файла", type=str)
        args = parser.parse_args()

        self.tar = tarfile.open(args.VFS_path, 'a') # архив VFS
        self.log_path = args.Log_path               # путь до xml файла
        open(self.log_path, 'w').close()
        self.log = ET.Element('Logs')               # корневой элемент xml файла

#------ GUI
        self.master.title('Эмулятор')
        self.output_area = tk.Text(master, fg='#E3E3E3', height=20, width=100)
        self.input_area = tk.Text(master, fg='#E3E3E3', height=5, width=100)
        self.enter_button = tk.Button(master, text="Ввод", fg='#E3E3E3', width=20, command = self.Emu)
        self.input_area.insert(tk.END, "$ ")
        self.VFS_button = tk.Button(master, text="Выбрать VFS", fg='#E3E3E3', command=self.ChooseVFS)
        self.log_button = tk.Button(master, text="Выбрать Log", fg='#E3E3E3', command=self.ChooseLog)

        self.VFS_button.pack(side='left', anchor='n', pady=5, padx=5)
        self.log_button.pack(side='left', anchor='n', pady=5)
        self.output_area.pack(pady=5, padx=5)
        self.input_area.pack(pady=5, padx=5)
        self.enter_button.pack(anchor='sw', pady=10, padx=60)

        self.master.configure(background='#121212')
        self.output_area.configure(background='#2B2B2B', relief='flat')
        self.input_area.configure(background='#2B2B2B', relief='flat')
        self.enter_button.configure(background='#2B2B2B', relief='flat')
        self.VFS_button.configure(background='#2B2B2B', relief='flat')
        self.log_button.configure(background='#2B2B2B', relief='flat')


    def ChooseVFS(self):
        vfs_path = filedialog.askopenfilename(title='Выберите архив VFS', filetypes=[('Tar files', '*.tar')])
        if vfs_path:
            self.tar = tarfile.open(vfs_path, 'a')
    

    def ChooseLog(self):
        self.log_path = filedialog.askopenfilename(title='Выберите log файл', filetypes=[('xml files', '*.xml')])
        if self.log_path:
            open(self.log_path, 'w').close()
            self.log = ET.Element('Logs')


    def Log(self, command):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        action_field = ET.SubElement(self.log, 'Action')
        action_field.set('command', command)
        action_field.set('date', date)
        action_field.set('time', time)
        data = ET.tostring(self.log, encoding='unicode')
        xml_file = open(self.log_path, 'w')
        xml_file.write(data)


    def Emu(self):
        command = self.input_area.get('1.0', tk.END)[2:-1]

        if command == 'ls':         
            for member in self.tar.getmembers():
                name = member.name
                np = name.strip('/').split('/')
                last = np.pop()
                if self.path == np:
                    self.output_area.insert(tk.END, last + " ")
            self.output_area.insert(tk.END, "\n")
            self.Log('ls')

        elif command == 'exit':                       
            self.master.quit()
            self.Log('exit')

        elif command.startswith('cd '):                        
            parts = command.split(' ')
            self.path = parts[1].split('/')  
            self.path = [i for i in self.path if i != '']
            self.Log('cd')
        
        elif command == 'tree':
            files_count = 0
            dir_count = 0
            for member in self.tar.getmembers():
                name = member.name
                np = name.strip('/').split('/')
                last = np.pop()
                indent = '│   ' * (name.count('/'))
                    
                if member.isdir():
                    dir_count += 1
                    self.output_area.insert(tk.END, indent + '├───' + last + '\n') 
                elif member.isfile():
                    files_count += 1
                    self.output_area.insert(tk.END, indent + '└───' + last + '\n') 

            self.output_area.insert(tk.END, str(dir_count) + ' directories ' + str(files_count) + ' files' + '\n')
            self.Log('tree')

        '''elif command.startswith('rmdir '):
            #pathToDelete = os.getcwd()
            parts = command.split(' ')
            pathToDelete = ['root']
            pathToDelete.append(parts[1])
            with tarfile.open('myfiles.tar', 'a') as tar:
                for member in tar.getmembers():
                        name = member.name
                        np = name.strip('/').split('/')
                        if pathToDelete == np:
                            tar.remove(member)
                            print("was delete!")

            print('path ', path)
            print(parts)'''

        self.input_area.delete("1.0", tk.END)
        self.input_area.insert(tk.END, "$ ")


if __name__ == "__main__":
    root = tk.Tk()
    app = Emulator(root)
    root.mainloop()