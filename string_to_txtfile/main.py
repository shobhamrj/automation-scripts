from datetime import datetime
from os import getcwd, path, makedirs


def main():
    curr_date, curr_time = datetime.now().__str__().split()
    curr_dir = getcwd()
    file_dir = path.join(curr_dir, curr_date)
    makedirs(file_dir, exist_ok=True)
    file_name = f'{curr_date}-{curr_time}.txt'
    full_path = path.join(file_dir, file_name)
    with open(full_path, "w") as f:
        content = input("PLease enter file contents? \n")
        f.write(content)

if __name__ == '__main__':
    main()
