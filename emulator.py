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

        self.path_to_start = args.Start_path            # стартовый файл
        self.Start()                                    


    def Start(self):
        with open(self.path_to_start, 'r') as start_file:
            for line in start_file:
                self.command = line.strip()
                self.Emu()


    def ChooseVFS(self):
        self.path_to_tar = filedialog.askopenfilename(title='Выберите архив VFS', filetypes=[('Tar files', '*.tar')])
        if self.path_to_tar:
            self.tar = tarfile.open(self.path_to_tar, 'a')
    

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


    def InputButton(self):
        self.command = self.input_area.get('1.0', tk.END)[2:-1]
        self.Emu()


    def IsDirectoryEmpthy(self, folder_name):
        cnt = 0
        print(folder_name)
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
            path_to_directory = self.command.split(' ')
            path_to_directory = str(path_to_directory[1])
            #directory_info = self.tar.getmember(path_to_directory)

            if self.IsDirectoryEmpthy(str(path_to_directory.split('/')[-1])) == 1:
                print('rmdir: removing directory, "' + str(path_to_directory.split('/')[-1]) + '"')
            else:
                print('rmdir: failed to remove "' + str(path_to_directory.split('/')[-1]) + '": Directory is not empty')
#-------------
            '''
            tar_file = "VFS.tar"
            folder_to_delete = "dir_3"
            # Открываем архив для чтения и извлекаем все его члены
            with tarfile.open(tar_file, "a") as tar:
                members = tar.getmembers()

            # Открываем архив для записи и добавляем все его члены, кроме удаляемой папки
            with tarfile.open(tar_file, "a") as tar:
                for member in members:
                    if member.name.startswith(folder_to_delete) and member.isdir():
                        continue
                    tar.addfile(member, tar.extract(member))

            # Удаляем пустую папку из архива
            os.system(f"tar --delete --file={tar_file} {folder_to_delete}")
            '''
            '''
            members = self.tar.getmembers()
            # Find the folder you want to delete
            folder_to_delete = 'dir_3'
            # Filter out the members that are not in the folder to delete
            members_to_keep = [member for member in members if not member.name.startswith(folder_to_delete)]
            # Open the tar archive in write mode
            self.tar = tarfile.open('VFS1.tar', 'a')
            for member in members_to_keep:
                self.tar.add(member.name)'''




        self.input_area.delete("1.0", tk.END)
        self.input_area.insert(tk.END, "$ ")


if __name__ == "__main__":
    root = tk.Tk()
    app = Emulator(root)
    root.mainloop()