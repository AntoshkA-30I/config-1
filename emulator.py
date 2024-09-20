import io
import tarfile

path = []
while True:
    command = input("$ ")

    if command == "ls":
        with tarfile.open('myfiles.tar', 'a') as tar:
            for member in tar.getmembers():
                name = member.name
                np = name.strip('/').split('/')
                last = np.pop()
                if path == np:
                    print(last, end=" " * 2)
        print()

    elif command == "exit":
        break

    elif command.startswith("cd "):
        parts = command.split(" ")
        path = parts[1].split("/")  
        path = [i for i in path if i != ""]
    

