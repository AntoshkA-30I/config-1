import io
import tarfile
import tkinter as tk
from tkinter import filedialog


class Emulator:
    def __init__(self, master):
        self.master = master
        self.path = []
        self.tar = None

        self.master.title("Эмулятор")
        self.output_area = tk.Text(master, fg='#E3E3E3', height=20, width=100)
        self.input_area = tk.Text(master, fg='#E3E3E3', height=5, width=100)
        self.copy_button = tk.Button(master, text="Ввод", fg='#E3E3E3', width=20, command = self.Emu)
        self.input_area.insert(tk.END, "$ ")
        self.start_button = tk.Button(master, text="Выбрать VFS", fg='#E3E3E3', command=self.StartEmu)
#-------
        self.start_button.pack(anchor="nw")
        self.output_area.pack(pady=5)
        self.input_area.pack(pady=5)
        self.copy_button.pack(anchor="sw", pady=10, padx=40)

        self.master.configure(background='#121212')
        self.output_area.configure(background='#2B2B2B', relief='flat')
        self.input_area.configure(background='#2B2B2B', relief='flat')
        self.copy_button.configure(background='#2B2B2B', relief='flat')
        self.start_button.configure(background='#2B2B2B', relief='flat')


    def StartEmu(self):
            vfs_path = filedialog.askopenfilename(title="Выберите архив VFS", filetypes=[("Tar files", "*.tar")])
            if vfs_path:
                self.tar = tarfile.open(vfs_path, 'a')


    def Emu(self):
        command = self.input_area.get("1.0", tk.END)[2:-1]

        if command == 'ls':         
            for member in self.tar.getmembers():
                name = member.name
                np = name.strip('/').split('/')
                last = np.pop()
                if self.path == np:
                    self.output_area.insert(tk.END, last + " ")
            self.output_area.insert(tk.END, "\n")

        elif command == 'exit':    
            self.output_area.insert(tk.END, "Exiting emulator.\n")                     
            self.master.quit()

        elif command.startswith('cd '):                        
            parts = command.split(' ')
            self.path = parts[1].split('/')  
            self.path = [i for i in self.path if i != '']
        
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