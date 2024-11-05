import tarfile
import tkinter as tk
from tkinter import filedialog
import xml.etree.cElementTree as ET
import datetime
import argparse

import os


class Emulator:
    def __init__(self, master):
        self.master = master
        self.path = [] # текущий путь

#------ terminal keys
        parser = argparse.ArgumentParser()
        parser.add_argument("VFS_path", help="Введите путь до архива VFS", type=str)
        parser.add_argument("Log_path", help="Введите путь до Log файла", type=str)
        parser.add_argument("Start_path", help="Введите путь до стартового файла", type=str)
        args = parser.parse_args()

        self.path_to_tar = args.VFS_path                # архив VFS
        self.tar = tarfile.open(self.path_to_tar, 'a')  
        self.log_path = args.Log_path                   # путь до xml файла
        open(self.log_path, 'w').close()
        self.log = ET.Element('Logs')                   # корневой элемент xml файла

#------ GUI
        self.master.title('Эмулятор')
        self.output_area = tk.Text(master, fg='#E3E3E3', height=20, width=100)
        self.input_area = tk.Text(master, fg='#E3E3E3', height=5, width=100)
        self.enter_button = tk.Button(master, text="Ввод", fg='#E3E3E3', width=20, command = self.InputButton)
        self.input_area.insert(tk.END, "$ ")

        self.output_area.pack(pady=5, padx=5)
        self.input_area.pack(pady=5, padx=5)
        self.enter_button.pack(anchor='sw', pady=10, padx=60)

        self.master.configure(background='#121212')
        self.output_area.configure(background='#2B2B2B', relief='flat')
        self.input_area.configure(background='#2B2B2B', relief='flat')
        self.enter_button.configure(background='#2B2B2B', relief='flat')

        self.path_to_start = args.Start_path            # стартовый файл
        self.Start()                                    


    def Start(self):
        with open(self.path_to_start, 'r') as start_file:
            for line in start_file:
                self.command = line.strip()
                self.Emu()


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


    def InputButton(self):
        self.command = self.input_area.get('1.0', tk.END)[2:-1]
        self.Emu()


    def IsDirectoryEmpthy(self, folder_name):
        cnt = 0
        for member in self.tar.getmembers():
            if member.name.find(folder_name) != -1: 
                cnt +=1
        return cnt


    def Emu(self):
        if self.command == 'ls':         
            for member in self.tar.getmembers():
                name = member.name
                np = name.strip('/').split('/')
                last = np.pop()
                if self.path == np:
                    self.output_area.insert(tk.END, last + " ")
            self.output_area.insert(tk.END, "\n")
            self.Log('ls')

        elif self.command == 'exit':                       
            self.master.quit()
            self.Log('exit')

        elif self.command.startswith('cd '):                        
            parts = self.command.split(' ')
            self.path = parts[1].split('/')  
            self.path = [i for i in self.path if i != '']
            self.Log('cd')
        
        elif self.command == 'tree':
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

        elif self.command.startswith('rmdir '): 
            directory_name = self.command.split(' ')[1]
            path_to_directory = self.path[:]
            path_to_directory.append(directory_name)
            path_to_directory = "/".join(path_to_directory)

            if self.IsDirectoryEmpthy(directory_name) == 1:
                print('rmdir: removing directory, "' + directory_name + '"')
                with tarfile.open(self.path_to_tar, 'r') as tin:
                    with tarfile.open(self.path_to_tar + '.tmp', 'w') as tout:
                        for item in tin.getmembers():
                            buffer = tin.extractfile(item.name)
                            print(item.name)
                            if path_to_directory != item.name:
                                tout.addfile(item, buffer)
                self.tar.close()
                os.system('del VFS.tar')                                        #работает только на windows :)
                os.system('move VFS.tar.tmp VFS.tar')
                self.tar = tarfile.open(self.path_to_tar, 'a')
                
            elif self.IsDirectoryEmpthy(directory_name) > 1:
                print('rmdir: failed to remove "' + directory_name + '": Directory is not empty')
            else:
                print('rmdir: failed to remove "' + directory_name + '": Directory is not exist')

            self.Log('rmdir')

        self.input_area.delete("1.0", tk.END)
        self.input_area.insert(tk.END, "$ ")


if __name__ == "__main__":
    root = tk.Tk()
    app = Emulator(root)
    root.mainloop()