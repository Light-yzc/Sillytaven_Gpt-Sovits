import os
import json
import time
import requests
import winsound
import threading
import shutil
tmp_file = ''
global_msg = ''
def get_file_names(directory):
    file_names = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_names.append(file_path)
    return file_names



def getname(directory_to_list):
    if not os.path.exists(directory_to_list):
        print('路径不存在，请手动指定酒馆路径')
        directory_to_list = input("Enter the directory path: ")
    file_names = get_file_names(directory_to_list)
    print(f"Files in the directory {directory_to_list}:")
    for i in range(len(file_names)):
         print(f'{i}. {file_names[i]}')
    return file_names


def read_json_file(file_path):
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
            return data
    # try:
    #     f = open(file_path, 'r',encoding='utf-8')
    #     for line in f:
    #         data = json.loads(line)
    #     f.close()
    #     return data

    # except FileNotFoundError:
    #     return None

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return None
    except Exception:
        return None

    

def format_str(text):
    form = '[使用简体中文开始创作:]'
    index = text.find(form)
    index2 = text.find("/'/'/'")
    return text[index+len(form):index2]

# def paly_sound():
#     global sound_playing 
#     sound_playing = True
#     winsound.PlaySound('./voice.wav',winsound.SND_FILENAME)
#     sound_playing = False

def play_sound(num):
    winsound.PlaySound('./tmpfile/voice' + str(num) + '.wav',winsound.SND_FILENAME)

i = 0
def gengerate_voice(text):
    global tmp_file,i
    url = f'http://127.0.0.1:9880/?refer_wav_path=F:/yzc/IDM/LLM/SillyTavern/public/sounds/ref.wav&prompt_text=やめない、壊れそうだから、さきが壊れたら&prompt_language=ja&text=' + text + '&text_language=zh&top_k=15&top_p=1&temperature=0.5&speed=1&cut_punc=，。`'
    try:
        if tmp_file == '':
            if os.path.exists('./tmpfile'):
                shutil.rmtree('./tmpfile')
            os.makedirs('tmpfile')
        response = requests.get(url=url)
        
        with open("./tmpfile/voice" + str(i)+ ".wav","wb+") as file:
            file.write(response.content)
        # winsound.PlaySound("./voice.wav",winsound.SND_FILENAME)
        # await paly_sound()
        # with lock:
        #     if not sound_playing:
        #         threading.Thread(target=paly_sound).start
        # play_sound()
        threat = threading.Thread(target=play_sound,kwargs={'num':i})
        threat.start()
    except:
        print("------tts的Api服务器不可用，跳过声音生成------")


def main():
    global global_msg
    path =getname('../data/default-user/chats')
    ids = input('请选择要监听的对话:(数字)\n')
    msg = read_json_file(path[int(ids)])
    while True:
        msg = read_json_file(path[int(ids)])
        if msg['is_user'] == True:
            print("当前为用户对话,请确保最后一条消息不为用户消息")
            time.sleep(10)
        if msg['is_user'] == False and msg['mes'] != global_msg:
            global_msg = msg['mes']
            gengerate_voice(format_str(global_msg))
        time.sleep(5)
    
main()