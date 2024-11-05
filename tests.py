import unittest
import tarfile
import shutil
import os

#Функции для тестов
def ls(tar, path):  
    result = []   
    for member in tar.getmembers():
        name = member.name
        np = name.strip('/').split('/')
        last = np.pop()
        if path == np:
            result.append(last)
    return result


def cd(command):
    result = []  
    parts = command.split(' ')
    result = parts[1].split('/')  
    result = [i for i in result if i != '']
    return result


def tree(tar):
    result = []
    files_count = 0
    dir_count = 0
    for member in tar.getmembers():
        name = member.name
        np = name.strip('/').split('/')
        last = np.pop()
        indent = '│   ' * (name.count('/'))
                    
        if member.isdir():
            dir_count += 1
            result.append(indent + '├───' + last) 
        elif member.isfile():
            files_count += 1
            result.append(indent + '└───' + last) 

    result.append(str(dir_count) + ' directories ' + str(files_count) + ' files')
    return result


def IsDirectoryEmpthy(tar, folder_name):
    cnt = 0
    for member in tar.getmembers():
        if member.name.find(folder_name) != -1: 
            cnt +=1
    return cnt
    

def rmdir(tar, command, path):
    result = []
    directory_name = command.split(' ')[1]
    path_to_directory = path[:]
    path_to_directory.append(directory_name)
    path_to_directory = "/".join(path_to_directory)

    if IsDirectoryEmpthy(tar, directory_name) == 1:
        result.append('rmdir: removing directory, "' + directory_name + '"')
        with tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar', 'r') as tin:
            with tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar' + '.tmp', 'w') as tout:
                for item in tin.getmembers():
                    buffer = tin.extractfile(item.name)
                    print(item.name)
                    if path_to_directory != item.name:
                        tout.addfile(item, buffer)
        tar.close()
        os.system('del VFS.tar')                                #работает только на windows :)
        os.system('move VFS.tar.tmp VFS.tar')
        tar = tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar', 'a')
                
    elif IsDirectoryEmpthy(tar, directory_name) > 1:
        result.append('rmdir: failed to remove "' + directory_name + '": Directory is not empty')
    else:
        result.append('rmdir: failed to remove "' + directory_name + '": Directory is not exist')
    return result




#Тесты
class TestStringMethods(unittest.TestCase):

#---ls
    def test_ls_1(self):
        expected_result = ['dir_1', 'dir_2', 'dir_3', 'text.txt']
        input = ls(tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar', 'a'), ['root'])
        self.assertEqual(input, expected_result)
    
    def test_ls_2(self):
        expected_result = ['11.txt']
        input = ls(tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar', 'a'), ['root', 'dir_2'])
        self.assertEqual(input, expected_result)
    
    def test_ls_3(self):
        expected_result = []
        input = ls(tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar', 'a'), ['root', 'dir_3'])
        self.assertEqual(input, expected_result)

#---cd
    def test_cd_1(self):
        expected_result = ['root']
        input = cd('cd root')
        self.assertEqual(input, expected_result)
    
    def test_cd_2(self):
        expected_result = ['root', 'dir_1']
        input = cd('cd root/dir_1')
        self.assertEqual(input, expected_result)
    
    def test_cd_3(self):
        expected_result = []
        input = cd('cd /')
        self.assertEqual(input, expected_result)

#---tree
    def test_tree_1(self):
        expected_result = ['├───root', '│   ├───dir_1', '│   │   └───1.txt', '│   │   └───2.txt', '│   ├───dir_2', '│   │   └───11.txt', '│   ├───dir_3', '│   └───text.txt', '4 directories 4 files']
        input = tree(tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar', 'a'))
        self.assertEqual(input, expected_result)

#---rmdir
    def test_rmdir_1(self):
        expected_result = ['rmdir: failed to remove "dir_4": Directory is not exist']
        input = rmdir(tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar', 'a'), 'rmdir dir_4', ['root'])
        self.assertEqual(input, expected_result)

    def test_rmdir_2(self):
        expected_result = ['rmdir: failed to remove "dir_2": Directory is not empty']
        input = rmdir(tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar', 'a'), 'rmdir dir_2', ['root'])
        self.assertEqual(input, expected_result)

    def test_rmdir_3(self):
        expected_result = ['rmdir: removing directory, "dir_3"']
        input = rmdir(tarfile.open('C:/Users/anton/Desktop/config-1/VFS_test.tar', 'a'), 'rmdir dir_3', ['root'])
        self.assertEqual(input, expected_result)


#Запуск тестов
def copy_tar_archive(source_path, destination_path):
    shutil.copy2(source_path, destination_path)


if __name__ == '__main__':
    copy_tar_archive('C:/Users/anton/Desktop/config-1/VFS.tar', 'C:/Users/anton/Desktop/config-1/VFS_test.tar')
    unittest.main()