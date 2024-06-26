import os
import errno
import pickle
import json
import subprocess
import shutil


# ! Screen

def get_screen_list(identifier='\t'):
    """Return all screens on this screen"""
    all_screens = subprocess.run(['screen', '-ls'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
    return [_.strip('(Detached)').strip('\t') for _ in all_screens if identifier in _]


def quit_screens(*screens_to_kill):
    for screen_name in screens_to_kill:
        # killSCREEN
        os.system(f'screen -S {screen_name} -X quit\n')


def json_save(data, file_name, log=print):
    with open(file_name, 'w', encoding='utf-8') as f:
        try:
            json.dumps(data)
        except:
            log(f"{data['Static logs']} failed to save in json format.")
        json.dump(data, f, ensure_ascii=False, indent=4)
        log(f'Successfully saved to {file_name}')


def json_load(file_name, log=print):
    try:
        with open(file_name) as data_file:
            return json.load(data_file)
    except:
        remove_file(file_name)
        log(f'Failed to load {file_name}, file removed.')
        return None


def init_path(file_or_path):
    path = get_dir_of_file(file_or_path)
    if not os.path.exists(path):
        os.makedirs(path)
    return file_or_path


def list_dir(dir_name, error_msg=None):
    try:
        f_list = os.listdir(dir_name)
        return f_list
    except FileNotFoundError:
        if error_msg is not None:
            print(f'{error_msg}')
        return []


def silent_remove(file_or_path):
    # Modified from 'https://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist'
    try:
        if file_or_path[-1] == '/':
            shutil.rmtree(file_or_path)
        else:
            os.remove(file_or_path)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


def remove_file(f_list):
    'Remove file or file list'
    f_list = f_list if isinstance(f_list, list) else [f_list]
    for f_name in f_list:
        silent_remove(f_name)


def get_dir_of_file(f_name):
    return os.path.dirname(f_name) + '/'


def get_grand_parent_dir(f_name):
    from pathlib import Path
    if '.' in f_name.split('/')[-1]:  # File
        return get_grand_parent_dir(get_dir_of_file(f_name))
    else:  # Path
        return f'{Path(f_name).parent}/'


def get_abs_path(f_name, style='command_line'):
    # python 中的文件目录对空格的处理为空格，命令行对空格的处理为'\ '所以命令行相关需 replace(' ','\ ')
    if style == 'python':
        cur_path = os.path.abspath(os.path.dirname(__file__))
    elif style == 'command_line':
        cur_path = os.path.abspath(os.path.dirname(__file__)).replace(' ', '\ ')

    root_path = cur_path.split('src')[0]
    return os.path.join(root_path, f_name)


def mkdir_p(path, log=True):
    """Create a directory for the specified path.
    Parameters
    ----------
    path : str
        Path name
    log : bool
        Whether to print result for directory creation
    """
    import errno
    if os.path.exists(path): return
    # print(path)
    # path = path.replace('\ ',' ')
    # print(path)
    try:

        os.makedirs(path)
        if log:
            print('Created directory {}'.format(path))
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path) and log:
            print('Directory {} already exists.'.format(path))
        else:
            raise


def mkdir_list(p_list, use_relative_path=True, log=True):
    """Create directories for the specified path lists.
        Parameters
        ----------
        p_list :Path lists or a single path

    """
    # ! Note that the paths MUST END WITH '/' !!!
    root_path = os.path.abspath(os.path.dirname(__file__)).split('src')[0]
    p_list = p_list if isinstance(p_list, list) else [p_list]
    for p in p_list:
        p = os.path.join(root_path, p) if use_relative_path else p
        p = os.path.dirname(p)
        mkdir_p(p, log)


def save_pickle(var, f_name):
    mkdir_list([f_name])
    pickle.dump(var, open(f_name, 'wb'))
    print(f'File {f_name} successfully saved!')


def load_pickle(f_name):
    return pickle.load(open(f_name, 'rb'))


def get_root_dir():
    return os.path.abspath(os.path.dirname(__file__)).split('src')[0]


def get_src_dir():
    return get_root_dir() + 'src/'
