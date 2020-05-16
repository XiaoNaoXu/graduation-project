import os

count = 0

def write_to_zsh(themes_list, zshrc_path):
    global count
    fp = open(zshrc_path, 'r+')
    config = fp.readlines()
    for index in range(len(config)):
        if 'ZSH_THEME' in config[index] and config[index][0] != '#':
            config[index] = config[index][0:config[index].find('=')] + '="' + themes_list[count][0:themes_list[count].find('.')] + '"\n'
            count = count + 1
            print(config[index])
            fp.seek(0, 0)
            fp.truncate()
            fp.writelines(config)
            fp.close()
            return

def read_from_zsh(zsh_path):
    if os.path.isdir(zsh_path):
        return os.listdir(zsh_path)

if "__main__" == __name__:
    zsh_path = '/home/kasim/.oh-my-zsh/themes'
    zshrc_path = '/home/kasim/.zshrc'
    themes_list = read_from_zsh(zsh_path)
    while True:
        input()
        write_to_zsh(themes_list, zshrc_path)
#sonicradish


