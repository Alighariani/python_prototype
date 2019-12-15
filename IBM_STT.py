import subprocess

def IBM_STT(file):
    commandstr = ['java','-jar','IBM_STT.jar','.','.','5']
    commandstr.append(file)
    subprocess.call(commandstr)

IBM_STT("sample.wav")