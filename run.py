import subprocess
import sys
import os

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    example_py = os.path.join(script_dir, 'example.py')
    if not os.path.exists(example_py):
        print('未找到 example.py 文件！')
        sys.exit(1)
    print('正在启动 LLMAssistant...')
    # 指定 Anaconda 的 Python 解释器路径
    anaconda_python = r'C:\Users\H.Seldon\anaconda3\python.exe'  # 如有不同请修改为实际路径
    try:
        subprocess.run([anaconda_python, example_py], check=True)
    except subprocess.CalledProcessError as e:
        print(f'运行 example.py 失败，错误信息：{e}')
    input('\n按回车键退出...')

if __name__ == '__main__':
    main()
