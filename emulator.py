import io
import tarfile
import tkinter as tk

def emu():
    global path 
    command = input_area.get("1.0", tk.END)[2:-1]

    if command == 'ls':         
        with tarfile.open('myfiles.tar', 'a') as tar:
            for member in tar.getmembers():
                name = member.name
                np = name.strip('/').split('/')
                last = np.pop()
                if path == np:
                    output_area.insert(tk.END, last + " ")
        output_area.insert(tk.END, "\n")

    elif command == 'exit':                         
        root.quit()

    elif command.startswith('cd '):                        
        parts = command.split(' ')
        path = parts[1].split('/')  
        path = [i for i in path if i != '']
    
    elif command == 'tree':
        filesCount = 0
        dirCount = 0
        with tarfile.open('myfiles.tar', 'a') as tar:
            for member in tar.getmembers():
                name = member.name
                np = name.strip('/').split('/')
                last = np.pop()
                indent = '│   ' * (name.count('/'))
                
                if member.isdir():
                    dirCount += 1
                    output_area.insert(tk.END, indent + '├───' + last + '\n') 
                elif member.isfile():
                    filesCount += 1
                    output_area.insert(tk.END, indent + '└───' + last + '\n') 
        
            print(dirCount, 'directories,', filesCount, 'files')

    input_area.delete("1.0", tk.END)
    input_area.insert(tk.END, "$ ")

'''
    elif command.startswith('rmdir '):
        parts = command.split(' ')
        path1 = parts[1].split('/')  
        path1 = [i for i in path if i != '']
        with tarfile.open('myfiles.tar', 'r:*') as tar:
            for member in tar.getmembers():
                if member.name == path1:
                    tar.remove(member)
                    break
            else:
                print('File not found') '''




path = []
root = tk.Tk()
root.title("GUI")
output_area = tk.Text(root, height=20, width=100)
output_area.pack(pady=10)
input_area = tk.Text(root, height=5, width=100)
input_area.pack(pady=10)
copy_button = tk.Button(root, text="Enter", command=emu)
copy_button.pack(pady=5)
input_area.insert(tk.END, "$ ")
root.mainloop()