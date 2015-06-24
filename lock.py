"""
未验证：使用Python快速实现显示器关闭和锁住桌面

from: http://blog.csdn.net/caimouse/article/details/45840363
"""

# python 3.4 win7
from ctypes import *
from ctypes.wintypes import *

HWND_BROADCAST = 0xffff
WM_SYSCOMMAND = 0x0112
SC_MONITORPOWER = 0xF170
MonitorPowerOff = 2
SW_SHOW = 5


def main():
    windll.user32.PostMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MonitorPowerOff)
    shell32 = windll.LoadLibrary("shell32.dll")
    shell32.ShellExecuteW(None, 'open', 'rundll32.exe', 'USER32,LockWorkStation', '', SW_SHOW)


if __name__ == "__main__":
    print "Win32 Application in python"
    main()

