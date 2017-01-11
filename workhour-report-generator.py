#!/usr/bin/env python3
# coding: utf8

"""
    Workhour report generator.
"""

import argparse
from calendar import Calendar
from math import ceil
from time import *
import random
import subprocess
import os


try:
    from yattag import Doc, indent
except ImportError:
    print('The "yattag" package is missing, install with python-pip:')
    print('  $ sudo python3 -m pip install yattag')
    exit(1)

try:
    import holidays
except ImportError:
    print('The "holidays" package is missing, install with python-pip:')
    print('  $ sudo python3 -m pip install holidays')
    exit(1)


UNI_LOGO = ''.join([
    "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2Jl"
    "IElsbHVzdHJhdG9yIDEyLjAuMSwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAg"
    "QnVpbGQgNTE0NDgpICAtLT4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEv"
    "L0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIiBbCgk8"
    "IUVOVElUWSBuc19zdmcgImh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KCTwhRU5USVRZIG5zX3hs"
    "aW5rICJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIj4KXT4KPHN2ZyB2ZXJzaW9uPSIxLjEiIGlk"
    "PSJMYXllcl8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJo"
    "dHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMjMxMS4yNSIgaGVpZ2h0PSI3NjAuMDE4"
    "IiB2aWV3Qm94PSIwIDAgMjMxMS4yNSA3NjAuMDE4IiBvdmVyZmxvdz0idmlzaWJsZSIgZW5hYmxlLWJh"
    "Y2tncm91bmQ9Im5ldyAwIDAgMjMxMS4yNSA3NjAuMDE4IiB4bWw6c3BhY2U9InByZXNlcnZlIj4KPGc+"
    "Cgk8cGF0aCBmaWxsPSJub25lIiBzdHJva2U9IiNBNzFGM0MiIHN0cm9rZS13aWR0aD0iOS40MTciIGQ9"
    "Ik0yODUuNjI2LDc0LjgyOWMtOC45MzksMC0xNi4xNjQtNy4xNzctMTYuMTY0LTE2LjAwOSAgIGMwLTgu"
    "ODI5LDcuMjI1LTE2LjAwNCwxNi4xNjQtMTYuMDA0YzguOTE4LDAsMTYuMTQzLDcuMTc1LDE2LjE0Mywx"
    "Ni4wMDRDMzAxLjc3LDY3LjY1MiwyOTQuNTQ1LDc0LjgyOSwyODUuNjI2LDc0LjgyOXoiLz4KCTxwYXRo"
    "IGZpbGw9Im5vbmUiIHN0cm9rZT0iI0E3MUYzQyIgc3Ryb2tlLXdpZHRoPSIxNC41MDk4IiBkPSJNMTkz"
    "LjkxMSw1MDIuNzk1VjI4MS4xODZsLTE4Ni42NSw5Ny42MnYyMjQuNjQxbDI3Ny43NDQsMTQ1LjQxOSAg"
    "IGwyNzcuNzI5LTE0NS40MTlWMzc4LjgwNmwtMTg2LjctOTcuNjJ2MjIxLjYwOGwtOTEuMDI5LDQ4LjI3"
    "NkwxOTMuOTExLDUwMi43OTVMMTkzLjkxMSw1MDIuNzk1eiBNNy4yMjYsNjIuOTM1djI4Ni40NTcgICBs"
    "MTg2LjczNi05OC4yMTlWNjYuODYxIE0zNzUuMTg4LDY2Ljg0MWgxODguMjg4TDQ1Mi43MzgsNy4yMzhI"
    "MTE1LjgzMUw1LjQ0Myw2Ni44NDFoMTg4LjI4OCBNNTYyLjc3MSw2Mi45MzV2Mjg2LjQ1NyAgIGwtMTg2"
    "LjczNS05Ny42NjlWNjYuODYxIE0xOTMuOTYzLDY3LjYwM3YxODMuMzk1bDQ2LjE1Ny0yMy45NzF2LTg1"
    "LjM1NmMwLTI0LjUyMSwyMC4xMDUtNDQuNDEsNDQuODg2LTQ0LjQxICAgYzI0Ljc2NywwLDQ0Ljg3Miwx"
    "OS44OSw0NC44NzIsNDQuNDFsLTAuMTQxLDg1Ljg4OGw0Ni4yOTgsMjQuMjVsMC4wNzEtMTg0LjA1Mmwt"
    "OTEuMTAxLTQ3LjU4NUwxOTMuOTYzLDY3LjYwM0wxOTMuOTYzLDY3LjYwM3oiLz4KCTxwYXRoIGQ9Ik01"
    "OTkuOTksNjEuNTI0YzIyLjQ1MywyLjczNyw0MC41MjQtNS40NzUsNjAuNzg1LDIuNzM3Yy03LjEyMSw3"
    "LjEyMS0yNC42NDIsNC45MjgtMjEuMzU2LDIwLjgxMWwxLjA5NiwxNjQuODI4ICAgYzMuMjg1LDEzLjE0"
    "NiwxMi41OTQsMjUuNzM5LDI1LjE4OCwzMi44NThjMjEuOTA4LDguNzY0LDQ4LjE5MSwxMS41MDIsNjku"
    "MDAyLTIuMTg4YzE2Ljk3NS0xMC45NTcsMjUuMTkxLTI3LjkzMiwyNC42NDItNDcuMDk0ICAgVjc2Ljg1"
    "NWMwLjU1LTE0Ljc4MS0yNy45MjctMS42NDItMTUuODc5LTE2LjQyOWMxNi40MjksMS4wOTcsMzQuNDk1"
    "LTIuMTg4LDQ5LjI4MiwyLjczOWMtMy44Myw4LjIxNy0yMS45MDEsMi43MzktMjAuODExLDE2Ljk3NSAg"
    "IGwtMS42NDIsMTYyLjA5NWMtMy4yODUsMTcuNTI1LTkuODU1LDM2LjE0My0yNy45MjcsNDUuNDUyYy0z"
    "MC42NjYsMTYuOTc1LTc3LjIxNCwxNy41MjUtMTA1LjE0MS00LjkyOSAgIGMtMTUuODgzLTEzLjE0NC0x"
    "OS43MTQtMzEuMjE1LTIxLjM1NS01MC4zNzlWNzcuOTUzQzYxNi40MTksNjMuNzE3LDU4OS4wNCw3NC42"
    "NjgsNTk5Ljk5LDYxLjUyNEw1OTkuOTksNjEuNTI0eiIvPgoJPHBhdGggZD0iTTgwMy43LDYwLjQyN2Mx"
    "MC45NTUtMi4xODgsMjMuNTQ5LTAuNTQ2LDM1LjA1MS0xLjA5MmM0NS40NDcsNTkuNjg4LDg0Ljg3Niwx"
    "MjEuNTY5LDEyOS43ODIsMTgxLjgwOGwyLjE5My0zLjgzNlY3My4wMjYgICBjLTIuMTkzLTEyLjA0OC0y"
    "MS4zNjItMS42NDQtMTguNjIzLTEzLjY5MWMxNi40My0xLjY0MiwzNS41OTgtMi43MzksNTAuOTMsMS4w"
    "OTJjLTIuNzM4LDguNzYzLTIwLjI2NSwyLjE5My0xOC42MTcsMTYuNDI5ICAgbC0yLjczOSwyMTcuNDA1"
    "Yy0xNi40MjksMTAuNDAxLTkuMzA5LTE0LjI0LTE4LjA3MS0xOS43MTNjLTQxLjA3LTU3LjUtNzkuOTUz"
    "LTExNi42NDItMTIyLjY2Ni0xNzEuOTUzICAgYy0zLjgzNSw1OC41OTctMy44MzUsMTIwLjQ3OCwwLDE4"
    "MC4xNjVjMy44MzEsOS4zMSwxNi45NzYsMi4xODksMTcuNTI1LDExLjUwMmMtMTYuNDI5LDEuNjQ0LTM0"
    "LjUsMS42NDQtNTAuOTMsMCAgIGMxLjY0My04Ljc2MywxOC42MTctMi43MzcsMTkuNzE0LTE0Ljc4NVY4"
    "MS43ODljLTUuNDc4LTguNzYzLTE0LjIzNi0xNC43ODctMjMuNTQ5LTE3LjUyNlY2MC40MjdMODAzLjcs"
    "NjAuNDI3eiIvPgoJPHBhdGggZD0iTTEwNDIuNDYxLDI4MC41NzFsMS4wOTctMjAzLjcxNmMxLjY0My0x"
    "NS4zMzEtMzUuNTk4LTYuMDIzLTEzLjY5LTE3LjUyMWMzOS40MjksMC41NDYsNzUuMDIxLTEuMDk2LDEx"
    "My45MDMsMS4wOTIgICBjLTAuNTUxLDguMjE3LTEzLjY5LDMuODM2LTE1Ljg4MywxMi42YzE1Ljg4Myw2"
    "My41MjIsNDAuNTI0LDEyNC4zMDgsNjIuOTc3LDE4NS4wOTNsNC45MjgtNC45MjhsNjAuMjM5LTE3Ni4z"
    "MzUgICBjLTAuNTUxLTMuODI5LTIuNzM5LTcuNjY2LTYuMDI0LTEwLjQwNGMtNC45MzMsMS4wOTYtOC43"
    "NjMtMC41NDYtMTIuMDQ3LTMuMjg1bDEuMDkyLTMuODMxaDE3OS4wNzMgICBjMi43MzQsMTAuNDA2LDEy"
    "LjU5MywyMC44MDYsNy42NjYsMzAuNjY2Yy0xNi45NzktMzEuMjE3LTU2Ljk1NC0yMS45MDgtODguMTY5"
    "LTIxLjkwOGwtNy4xMTYsOC43NjNsLTEuMDk3LDczLjkyOSAgIGMxMy4xNDUsMTAuOTUyLDMzLjQwNC0w"
    "LjU0Niw1MC4zOCw0LjkyOWMyLjE5MywxLjA5NiwzLjgzNSw0LjM4MSwxLjA5Niw2LjAyM2MtMTUuMzMx"
    "LDcuMTItMzkuNDI3LTQuMzgyLTUwLjM3OSw5Ljg2ICAgbC0xLjA5NywxMDQuMDQyYzAuNTQ2LDUuNDc5"
    "LDcuMTIxLDkuMzA5LDEyLjA0OSw5Ljg1OWMzMS4yMTUtNC4zODEsNzUuMDIsMTMuMTQ1LDg5LjI2LTI0"
    "LjY0Mmg2LjAyNSAgIGMtMi43NCwxMi4wNDgtNi4wMjUsMjMuNTQ2LTEzLjY5LDMzLjQwNGMtNDUuNDUy"
    "LTAuNTUxLTkxLjQ1LDEuMDkyLTEzNS44MTItMS4wOTZjMC41NTItMTIuNTk0LDIwLjgxMi0wLjU0Niwx"
    "OS43MTUtMTYuNDMgICBsLTEuMDkyLTIwNi40NDljLTcuNjcxLTQuOTI4LTE4LjA3MS02LjAyNC0yNy4z"
    "ODUtMy44MzZsLTEwLjk1MSwxMi41OTlsLTc1LjU3MiwyMTUuMjEyYy0yLjE4OCwyLjczNC00LjkyNyw0"
    "LjM4Mi04Ljc1OCwzLjgzMSAgIGwtNi4wMjMtOC43NjNsLTczLjkyOS0yMTIuNDc0Yy02LjU3LTEwLjQw"
    "NC0yMC44MTEtMTEuNDk2LTMyLjMwOC04Ljc2M2wtNC45MzIsNi4wMjR2MjA2LjQ1NCAgIGMxLjY0Miw4"
    "LjIxMiwxMi4wNDYsNy4xMTUsMTguNjIxLDguNzU4djQuOTMyYy0yMC4yNjUsMS4wOTItNDUuNDUyLDMu"
    "ODMxLTYyLjk3Ny0yLjczOCAgIEMxMDI3LjEyOSwyODQuNDAyLDEwMzkuNzIyLDI5MS41MjMsMTA0Mi40"
    "NjEsMjgwLjU3MUwxMDQyLjQ2MSwyODAuNTcxeiIvPgoJPHBhdGggZD0iTTE0NjAuMjkyLDI3OS40NzVs"
    "MS4wOTctMTg5LjQ3NWMwLjU0Ni0xMC40MDYtMTQuNzg3LTMuMjg1LTEzLjY5LTEzLjE0NmMzNy43ODYt"
    "MjIuNDUyLDg5LjI2MS0yOS41NjgsMTI4LjY4OS02LjU2OCAgIGMxNy41MjEsMTUuMzMxLDIzLjU0NCwz"
    "Ny4yMzQsMTguNjE3LDYwLjc4NGMtMy44MywxNS4zMzItMTUuMzMyLDMyLjMwNy0zMS4yMTEsMzguMzMx"
    "bC0yOS41NzMsOC43NjNsNzEuNzM1LDEwMS4zMTEgICBjNS40NzgsOS44NTQsMTguNjIzLDQuOTI3LDIz"
    "LjU1LDEzLjY4OWMtMTIuMDQ4LDMuODMxLTI3LjkyNywyLjE4OC00MC41MjQsMS4wOTdjLTI4LjQ3OC00"
    "MS4wNzEtNjEuMzMxLTc5LjQwNy04NC4zMy0xMjIuNjY1ICAgYzI1LjE4Ny0yLjE5NCw1Mi4wMjEtNy4x"
    "MjEsNjQuNjE1LTMxLjc2M2M2LjAyNC0xNi45NzUsNC45MjctMzkuNDI5LTMuODMxLTU0Ljc2MmMtMTIu"
    "MDQ4LTE0LjI0LTI3LjM4LTIxLjM1Ni00Ni4wMDItMTkuNzEzICAgYy05Ljg1NCwxLjA5Mi0yMC4yNjEs"
    "Mi4xODgtMjguNDczLDguNzU4bC02LjAyMywxMC45NTVsLTIuMTkzLDE5MC41NjdjMC41NTEsNi4wMjMs"
    "NC45MjcsMTAuOTU3LDEwLjk1MSwxMi4wNDggICBjNC4zODItMC41NDYsNy4xMiwxLjY0MywxMC45NTYs"
    "Mi43Mzh2My44MzZjLTIwLjgxMSwxLjA5MS00NC4zNTksMi43MzQtNjQuMDc0LTEuMDk3ICAgQzE0NDMu"
    "MzE1LDI4NC40MDIsMTQ1OC42NDgsMjkwLjQyNiwxNDYwLjI5MiwyNzkuNDc1TDE0NjAuMjkyLDI3OS40"
    "NzV6Ii8+Cgk8cGF0aCBkPSJNMTYyOS41MDIsMjQ4LjI1OWMxMi41OTQsMTYuNDMsMjguNDc4LDMzLjk1"
    "NSw0OS4yODMsMzguMzM4YzE4LjA3MSwzLjgyOSwzNi4xNDQsMCw0OS44MzMtMTAuOTU3ICAgYzExLjUw"
    "Mi0xMi4wNDgsMTYuNDMtMjYuODMsMTQuNzg3LTQ0LjM1NWMtMTYuOTc2LTUyLjAyMi03OC44NTctNTku"
    "MTQyLTEwNS4xNDEtMTA0LjA0OGMtNi41NzQtMTcuNTIxLTQuMzgxLTM5Ljk3NSw3LjExNi01NC4yMSAg"
    "IGMyMi40NTItMjYuMjg5LDYxLjMzNS0xNy41MjYsOTAuMzU4LTEyLjZjNC45MjcsMCw4LjIxMi03LjY2"
    "NiwxMi41OTQtNC45MjdjMi4xOTIsMTQuNzg3LDExLjUwMiwyOS41NzMsNi4wMjMsNDQuMzU1ICAgYy0x"
    "Mi41OTQtMTMuMTQtMjQuNjQyLTMwLjExNC00My4yNTktMzQuNDk1Yy0xNS4zMzMtMi4xOTQtMzMuNDA0"
    "LTIuNzQtNDQuMzU1LDkuODU0Yy0xMi4wNDgsOS4zMDktMTIuNTk5LDI0LjY0Mi05Ljg2LDM4LjMzMSAg"
    "IGMzMC4xMiw0OC43NDIsMTI3LjA0OCw2My41MjQsMTA2LjIzNywxMzguNTVjLTYuMDIzLDIyLjQ1My0y"
    "Ny45MjYsNDAuNTI0LTUwLjkzLDQ0LjM1NWMtMjIuOTk5LDUuNDc4LTQzLjI2LTMuODMxLTY1LjE2MS02"
    "LjAyNCAgIGMtNC45MzMsMS42NDQtNC45MzMsMTEuNTAyLTExLjUwMiw2LjAyNGMtMy4yODQtMTUuMzMz"
    "LTguMjEzLTI5LjU2OC05Ljg1OS00NS40NTJMMTYyOS41MDIsMjQ4LjI1OUwxNjI5LjUwMiwyNDguMjU5"
    "eiIvPgoJPHBhdGggZD0iTTE3OTIuNjk2LDI3Ni43MzVWNzAuMjg2Yy0yLjczOS05LjMwOS0yNi4yODkt"
    "MC41NDYtMTQuNzg3LTEyLjA0OGMxOS4xNjMtMS4wOTYsNDQuMzU1LTMuODM2LDU5LjE0MiwyLjE4OCAg"
    "IGMtNC45MjcsNi41NzUtMTkuMTY3LDEuNjQ4LTIwLjgxMSwxMy42OTFjLTEuNjQyLDY1LjE2NS0xLjY0"
    "MiwxNDQuMDIyLDAsMjA3LjU0NWM0LjM4Miw2LjAyNCwxMi41OTQsNC4zODIsMTguNjE4LDYuMDI0ICAg"
    "YzEuMDk3LDcuNjY1LTcuNjY2LDYuMDIzLTEyLjU5NCw2LjU3NGMtMTYuNDI5LTEuMDk3LTM0LjUwMSwy"
    "LjE4OC00OS4yODItMi43MzggICBDMTc3NS43MTYsMjgyLjc1OSwxNzkxLjU5OSwyODkuMzI5LDE3OTIu"
    "Njk2LDI3Ni43MzVMMTc5Mi42OTYsMjc2LjczNXoiLz4KCTxwYXRoIGQ9Ik0xODU1LjY2Myw1Ni41OTVs"
    "MTU3LjE2NywyLjczOWMzLjI4NSwxMi4wNDgsMTEuNDk3LDIzLjU0NSw5Ljg1NCwzNS41OTNjLTkuMzA5"
    "LTEuNjQzLTkuODU0LTEzLjEzOS0xOC42MTctMTguMDcyICAgYy0xMi4wNDgtMTQuNzgxLTMyLjg1OC04"
    "Ljc2My01MC45My0xMC40MDRsLTkuODU1LDEwLjQwNGMwLDY3LjkwNi00LjM4MSwxMzcuOTk5LTEuMDk2"
    "LDIwNC44MDggICBjNC4zODEsNy42NjYsMjIuOTk4LDAsMTcuNTI1LDExLjUwMmMtMjEuMzU2LTAuNTQ2"
    "LTQyLjcxMywwLjU0Ni02Mi45NzgtMS42NDNjMi4xOTItMTAuOTUxLDI0LjY0Mi0yLjE5MywyMS45MDYt"
    "MTkuNzE0ICAgbDEuNjQ0LTE5Ny42OTFjLTEwLjk1Ni0xMS40OTgtMzIuMzEyLTkuODU1LTQ3LjA5NS02"
    "LjAyNGMtMTMuNjksMS42NDctMjAuMjY1LDE2LjQyOS0yOC40NzgsMjUuNzM3bC00LjkyNy0yLjE4OCAg"
    "IEMxODQzLjA3LDc5LjA0OSwxODQ2LjkwMSw2NS45MDUsMTg1NS42NjMsNTYuNTk1TDE4NTUuNjYzLDU2"
    "LjU5NXoiLz4KCTxwYXRoIGQ9Ik0yMDM2LjM3OCwyMi4wOTVjNi41NzQsMC41NSwxNS44ODMsMS42NDIs"
    "MTYuOTc1LDkuODU5YzEuNjQ3LDguNzU3LTEuMDkyLDE3LjUyMS05Ljg1NCwxOS43MTQgICBjLTguMjEy"
    "LDEuNjQzLTE3LjUyNi0xLjA5Ny0xOS43MTQtOS44NTlDMjAyMS41OTUsMzIuNTAxLDIwMjcuNjE1LDIz"
    "LjczNywyMDM2LjM3OCwyMi4wOTVMMjAzNi4zNzgsMjIuMDk1eiIvPgoJPHBhdGggZD0iTTIxNDEuNTI0"
    "LDI4MC41NzFsLTYzLjUyMy0yMTAuMjg1Yy0zLjI4NS00LjM4MS0yLjc0LTE0LjIzNi0xMC45NTctMTMu"
    "NjljLTI0LjY0Miw3My4zNzgtNDkuMjgzLDE0Ni4yMTEtNzMuOTI0LDIxOS4wNDMgICBsLTExLjUwMywx"
    "MC45NTdjLTIuNzM3LDIuMTg4LTEwLjQwNCwwLjU0Ni04LjIxMSw2LjU2OGwzOC4zMzEsMi4xODhsNC45"
    "MjgtMy44M2MtMS42NDMtNS40NzktMTEuNDk4LTMuMjg1LTEzLjY4OS05Ljg2ICAgYzYuNTczLTI0LjY0"
    "MSw5Ljg1OC01MC45MjUsMjUuNzM3LTcxLjczNWMyMC4yNjUsMCwzOC44ODMsMCw2MC43ODQsMGw3LjEy"
    "MSw0LjkyOGM3LjY2NSwyMS45MDYsMTcuNTI1LDQyLjcxMiwxOC42MTcsNjYuODA4ICAgYy0yLjc0LDgu"
    "MjE3LTEyLjA0OCw0LjkzNC0xOC42MTcsNy42Njd2NC45MzJjMjAuMjU5LDEuNjQ0LDQ0LjM1NCwxLjY0"
    "NCw2Mi45NzgsMCAgIEMyMTU4LjQ5OSwyODYuMDQ0LDIxNDUuMzU0LDI5MC40MjUsMjE0MS41MjQsMjgw"
    "LjU3MUwyMTQxLjUyNCwyODAuNTcxeiBNMjA4Ny44NTQsMjAwLjA3MmwtNTguMDQ1LTEuMDk3bDMxLjIx"
    "Ni05Ni4zODEgICBjMTIuMDQzLDI5LjU3MywyMC4yNjEsNjMuNTIyLDMwLjY2NSw5NS4yODVMMjA4Ny44"
    "NTQsMjAwLjA3MkwyMDg3Ljg1NCwyMDAuMDcyeiIvPgoJPHBhdGggZD0iTTIwOTMuMzI5LDIyLjA5NWM5"
    "LjMwOC0yLjE4OCwxOC4wNyw0LjM4MSwxOS43MTQsMTIuNTk0Yy0wLjU1Miw2LjU3NC0zLjI4NSwxNC4y"
    "NDEtOS44NiwxNi45NzkgICBjLTguMjEyLDEuMDkxLTE2LjQyOS0wLjU1MS0yMC4yNi04LjIxN0MyMDc5"
    "LjA4NywzNC42ODksMjA4NC41NjUsMjQuODM1LDIwOTMuMzI5LDIyLjA5NUwyMDkzLjMyOSwyMi4wOTV6"
    "Ii8+Cgk8cGF0aCBkPSJNMjEzNC45NTEsNTguMjM5bDE1Ni4wNywxLjA5NmM2LjAyMywxMS40OTcsMTEu"
    "NTAyLDI0LjY0MiwxMC45NSwzNy4yMzVjLTEwLjk1LTQuOTI4LTE0Ljc4MS0yMi40NTMtMjguNDcxLTI2"
    "LjI4MyAgIGMtMTUuMzMzLTEuMDk4LTQyLjE2OC05Ljg2LTUwLjM4Niw3LjY2NmwtMi43MzMsMjAxLjUy"
    "MmMyLjE4OCwxMC45NSwyNy4zOCwzLjgzMSwxNy41MjEsMTQuNzg2aC01OS42ODlsLTMuODM1LTMuODM2"
    "ICAgYzUuNDc5LTcuNjY2LDE5LjcxNCwwLDIyLjQ1My0xMi41OTRsMy44MzYtMTk4Ljc4MmMtMC41NTEt"
    "Ny4xMi04LjIxNy0xMi4wNDgtMTQuNzg3LTEyLjU5OSAgIGMtMTYuOTc2LTAuNTQ1LTMyLjg1OCwwLjU1"
    "MS00NS45OTgsOC43NjRjLTcuNjcxLDYuMDIyLTkuODU4LDIwLjgxMS0xOS43MTQsMTguNjE2ICAgQzIx"
    "MjEuMjYxLDgwLjY5MiwyMTI2LjE4OCw2Ny41NDgsMjEzNC45NTEsNTguMjM5TDIxMzQuOTUxLDU4LjIz"
    "OXoiLz4KCTxwYXRoIGQ9Ik04MjIuMDM4LDU0NS42MTJjMTAuNDA0LDMuODM2LDE2Ljk3NSwxNy41MjYs"
    "MjYuMjg4LDI0LjY0N2MxNi45NzUsMTMuNjg5LDQzLjI1OSwxOS43MTMsNjQuMDY5LDkuODU0ICAgYzE0"
    "Ljc4Ni04Ljc2MywyNC4xMS0yMy41NDYsMjUuNzM4LTM5Ljk3NWMtMi43MzktNjIuNDI3LTc3Ljc2LTY3"
    "LjM1OC0xMDMuNDk3LTExNi4wOTZjLTUuNDc4LTEzLjY5LTUuNDc4LTMwLjEyLDAtNDQuMzU1ICAgYzEw"
    "Ljk1MS0yMS4zNTYsMzQuNDk1LTI5LjU3Myw1OC4wNDUtMjguNDc4YzE2LjQzLTEuMDk2LDMxLjc2Mywx"
    "My42OSw0Ny4xMDksMS4wOTdoMy4yNzFjMy44MzUsMTQuMjM2LDguMjEyLDI5LjU2OSw3LjY2Niw0My4y"
    "NTkgICBjLTEwLjkzNy0zLjI4NS0xMy4xNDUtMTYuNDI0LTIzLjU0NS0yMi45OTljLTE2Ljk4LTEyLjU5"
    "NC00MS42MjEtMTUuODc4LTYwLjc5LTUuNDczYy0xMC4zOTksOC4yMTItMTQuMjM1LDE4LjYxOC0xNS44"
    "NzcsMzAuMTE5ICAgYzEyLjU5Myw1My42NjQsNzguMzEsNTUuODUzLDEwMi40MDUsMTA1LjE0MWMxMS41"
    "MTYsMTkuNzE0LDYuNTY5LDQ4LjE5MS00LjkxMyw2Ni4yNjJjLTE5LjE4MywyNi4yODUtNTEuNDk1LDI3"
    "LjkyNy03OS45NjgsMjMuNTQ2ICAgYy0xMC45NTYsMS4wOTYtMjUuMTkxLTE0Ljc4Ny0zMi4zMTIsMS42"
    "NDJoLTQuOTI3QzgyNS4zNDIsNTc4LjQ3MSw4MjIuNTg5LDU2MC45NDUsODIyLjAzOCw1NDUuNjEyTDgy"
    "Mi4wMzgsNTQ1LjYxMnoiLz4KCTxwYXRoIGQ9Ik0xMDAyLjc1MSwzNTMuOTQ5YzQ2LjAwMiw1OC4wNDYs"
    "ODMuMjM3LDEyMy4yMTIsMTI5Ljc4NSwxODEuMjYyYzMuODM2LTU0Ljc2NSwyLjczOS0xMTUsMS4xMTEt"
    "MTY5LjIxNCAgIGMtMi43NTMtOS4zMDktMjUuMjA3LTEuMDk4LTE0LjgwMS0xMi4wNDhjMTUuODc5LDAs"
    "MzIuODU4LTEuMDk3LDQ4LjE5MSwxLjA5N2MtMi43MzksOC43NTgtMTguNjIzLDIuMTg4LTE5LjcxNSwx"
    "NC43ODIgICBsLTIuNzI0LDIyMS4yMzVjLTEyLjYwOCw2LjU3NC05LjMyNC04Ljc1Ny0xMy43MDUtMTQu"
    "NzgxYy00MS42MjEtNTkuNjkzLTgyLjE0Mi0xMjEuNTc1LTEyNS45NTEtMTc5LjA3ICAgYy0zLjgzNiw1"
    "NS44NTQtMi43MTgsMTIzLjIxMi0xLjA5NiwxODEuMjU5YzQuMzgxLDcuMTIsMTUuODgzLDEuMDk3LDE3"
    "LjUyNCwxMC40MDVjLTE1LjMzMSwzLjI4NS0zNi42OTMsMy4yODUtNTAuOTI5LDAgICBjMS42NDItOC43"
    "NjMsMTguNjE2LTIuNzM5LDE5LjcxNC0xNS4zMzNsMS4wOTctMTk3LjY5MmMtNi41NzUtOC4yMTItMTIu"
    "NTk0LTE1Ljg3OS0yMy0xNi45NzV2LTMuODMxTDEwMDIuNzUxLDM1My45NDkgICBMMTAwMi43NTEsMzUz"
    "Ljk0OXoiLz4KCTxwYXRoIGQ9Ik03NTEuOTQ0LDM1OC44NzdjLTM3LjIzOS0xMi4wNDgtODMuNzg0LTcu"
    "NjY3LTExMi44MDcsMTguNjIyYy00Mi43MTcsMzguMzMxLTQ1LjQ1MiwxMDUuNjg2LTI4LjQ3NywxNTYu"
    "NjE2ICAgYzE0Ljc4NywzMy45NSw0OS44MzQsNTkuNjg4LDg2LjUzNyw2MC43ODVjNDEuMDc2LDMuMjg0"
    "LDc3Ljc0NS0xMC40MDYsMTAxLjI5NS00My4yNjVjMjMuNTQ1LTM0LjQ5NSwyNS43MzctODUuNDI2LDE0"
    "Ljc4Mi0xMjUuOTUxICAgQzgwNS4wNjMsMzk3LjIxMyw3ODAuOTg3LDM2Ny42MzksNzUxLjk0NCwzNTgu"
    "ODc3TDc1MS45NDQsMzU4Ljg3N3ogTTc2NC4wMDcsNTYyLjU5MmMtMTkuMTgzLDIxLjM1Ni00OC43NTIs"
    "MjYuMjg0LTc2LjY4MywxOS43MTUgICBjLTI3LjM4MS03LjEyMS00NC4zNTUtMzUuMDUyLTU0LjIxLTU5"
    "LjE0NGMtMTMuMTI0LTUzLjExOC03LjY2Ni0xMTUuNTUsMzguMzMxLTE0OS41YzE2LjQzLTEyLjA0OCw0"
    "MC41MjUtMTMuMTQ2LDYwLjIzOS04Ljc2NCAgIGMzNi42ODksOC4yMTgsNTYuNDAzLDQ3LjY0Niw2MC43"
    "OTksODEuNTk2Qzc5Ny45NDIsNDg5Ljc1OSw3OTEuMzcyLDUzMS4zNzUsNzY0LjAwNyw1NjIuNTkyTDc2"
    "NC4wMDcsNTYyLjU5MnoiLz4KCTxwYXRoIGQ9Ik0xMzI2LjM5MSw1ODAuMTE0bC02Ny45MDYtMjE5LjA0"
    "NGwtNi4wMjMtNy4xMmwtMy44MzEsMi4xODhsLTcxLjc0LDIxNi4zMDlsLTguNzY0LDEwLjk1MiAgIGMt"
    "Mi43MzQsNS40NzgtMTMuNjg5LTEuNjQ0LTEwLjk1MSw3LjY2NWw0NS40NzIsMS4wOThjMy44MTUtMTEu"
    "NTAyLTEzLjcxLTIuNzM5LTE1Ljg5Ny0xMi4wNDggICBjNi41NjktMjQuNjQyLDkuODU0LTUyLjAyMiwy"
    "NS43MzctNzEuNzM2YzIyLjQ1MywwLDUwLjkyNS03LjEyLDY5LjU0OCw2LjAyNGM3LjY2NiwyMS4zNTYs"
    "MTUuMzMzLDQyLjE2NywxNi45NzUsNjUuNzEyICAgYy0yLjczOSw5LjMwOS0xNy41MDUsMS42NDItMTku"
    "NzE0LDEwLjk1YzE4LjYxOCw0LjM4Myw0MC41MjEsMS42NDQsNjAuNzg1LDIuNzM5ICAgQzEzNTEuMDMx"
    "LDU4My4zOTgsMTMyOS42NzQsNTg4LjMzLDEzMjYuMzkxLDU4MC4xMTRMMTMyNi4zOTEsNTgwLjExNHog"
    "TTEyMTIuNDg3LDQ5NS43ODQgICBjMTAuNDA0LTMyLjMxMiwyMC44MDYtNjUuNzE3LDMyLjMwOC05Ni4z"
    "ODJjMTEuNTAyLDMxLjc2MywyMS45MDIsNjQuNjIsMjkuNTczLDk3LjQ3NUwxMjEyLjQ4Nyw0OTUuNzg0"
    "TDEyMTIuNDg3LDQ5NS43ODR6Ii8+Cgk8cGF0aCBkPSJNMTUwOS4yOTUsNDg4LjY2NGMtMTAuMzk5LTE3"
    "LjUyNi0yOS4wMjItMjQuMDk2LTQ3LjA5NC0yOC40NzdjMy44MzYtMy4yODUsOC4yMTgtNC4zODIsMTIu"
    "NTk5LTYuNTcgICBjMjAuODI2LTkuODU5LDMwLjY2NC0zMS4yMTcsMjkuNTY4LTU0LjIxNWMtMy4yODUt"
    "MTcuNTI1LTEzLjY4OS0zOC44ODMtMzMuNDA0LTQzLjI2NWMtMzguMzMyLTkuODU0LTg1LjQyNi01LjQ3"
    "My0xMTMuOTAzLDE5LjcxNSAgIGwxMi41OTQsNy42NjZsMy44MzYsMTc5LjA3NWMtMS4wOTcsOC4yMTIt"
    "MTEuNTAzLDguNzU4LTE0Ljc4NywxMy42ODljNC4zODIsNi4wMjQsMTIuMDQ4LDEwLjk1MSwxOS43MTQs"
    "MTIuNTk0ICAgYzQyLjE2OCw5Ljg1NCw5OC4wMjQsMTIuMDQ4LDEyNy4wNDgtMjYuMjgzQzE1MTkuMTU1"
    "LDU0Mi44NzksMTUyMS4zNDMsNTA5LjQ3NCwxNTA5LjI5NSw0ODguNjY0TDE1MDkuMjk1LDQ4OC42NjR6"
    "ICAgIE0xNDc1Ljg5Miw1NjguNjE2Yy0xNi45NzYsMTcuNTIxLTQ3LjY0MiwxOC4wNjYtNjguOTk4LDku"
    "ODU1bC05LjgzOC0xMC45NTFjLTEuMTEyLTYxLjg4Mi0zLjg1Mi0xMjUuOTUxLTIuNzU1LTE5MC4wMjEg"
    "ICBjNy4xMTYtMTMuMTQ2LDIyLjQ0Ny0xNi40MywzNy4yMzQtMTYuNDNjMTIuNTk0LDAuNTQ2LDI0LjY0"
    "MiwyLjczMywzNC41MDIsOS44NTRjMTkuNzEzLDE1Ljg4MywxNS4zMzIsNDIuNzEyLDguNzYzLDYyLjk3"
    "OCAgIGMtMTMuMTQ1LDIxLjM1Ny0zOC4zMzgsMjIuOTk5LTYxLjg2NywyNS4xODhjLTYuMDM5LDMuMjg0"
    "LDAuNTMxLDguMjE4LDMuODE1LDkuODU5YzI1LjczOS0xLjY0Miw1My4xMTgtMS4wOTYsNjYuODEsMjEu"
    "OTAyICAgQzE0OTUuNjI2LDUxMy44NSwxNDkzLjQxNyw1NDguOTAxLDE0NzUuODkyLDU2OC42MTZMMTQ3"
    "NS44OTIsNTY4LjYxNnoiLz4KCTxwYXRoIGQ9Ik0xNTUxLjQ1Niw1NzUuMTg2bDIuMTkzLTE4OS40NzVj"
    "MC04Ljc2NC0xMC45NTYtNC4zODMtMTMuMTQ1LTEwLjk1MmMyMC4yNjEtMjEuMzU1LDU0LjIxNS0yNC42"
    "NDYsODQuODgtMjIuNDUzICAgYzIxLjkwMy0wLjU0Niw0MS4wNyw4LjIxMiw1NC43NjIsMjYuMjg0Yzgu"
    "NzYzLDE0LjI0LDEyLjU5MywzMy40MDQsNy4xMTksNTAuMzhjLTQuOTI3LDI0LjY0Ni0zMS43NDcsMzku"
    "OTc5LTU0LjIxNSw0My4yNjQgICBjLTIuNzM4LDAuNTQ2LTYuMDIyLTAuNTQ2LTcuNjY2LDIuNzM4bDc2"
    "LjY2OCwxMDYuMjM3YzUuNDc0LDYuMDI0LDE3LjUyMSwwLDE4LjYxOCw5Ljg1NGMtMTMuNjksMC0yOS41"
    "NzQsNS40NzktNDAuNTI0LDAgICBsLTg0LjMzNS0xMTkuOTI4YzMuODM1LTEyLjA0OCwyNC4wOTYtMi4x"
    "ODgsMzMuNDA4LTguNzYzYzEyLjA0NC00LjM3NiwyNS43MzMtMTMuMTM5LDMwLjY2Ni0yNS43MzIgICBj"
    "OC43NjMtMTkuMTY5LDcuNjY3LTQ2LjU0OS04LjIxNy02MS44ODJjLTE0LjIzNi0xNS44ODMtMzguODc4"
    "LTE1LjMzMy01OC4wNDYtMTAuOTU2Yy01LjQ1OCwyLjczOS0xMi4wNDgsNi4wMjQtMTQuNzg3LDEyLjA0"
    "OCAgIGMtMi43MzksNjUuMTY2LTUuNDczLDEzNS4yNjUtMi43MzksMjAyLjYyYzMuMjksOS44NTgsMjYu"
    "ODM1LDEuMDk2LDE3LjUyNywxMi41OTJjLTIwLjgxMS0wLjU0NS00Mi43MTQsMi4xOTQtNjEuODgyLTIu"
    "MTg4ICAgQzE1MzMuOTM1LDU3OC40NzEsMTU1MC45MSw1ODguODc2LDE1NTEuNDU2LDU3NS4xODZMMTU1"
    "MS40NTYsNTc1LjE4NnoiLz4KCTxwYXRoIGQ9Ik0xNzA4LjA3NiwzNTUuMDQ2bDU5LjY4OCwxLjA5MmMt"
    "NC4zODEsNy42NjYtMjAuMjYsNC4zODEtMjEuMzQxLDE3LjUyNmwxLjYyNywxNzUuMjM4ICAgYzMuMjg1"
    "LDE0LjIzNiwxNS44OTgsMjUuMTg3LDI4LjQ3NywzMi4zMDhjMjAuMjgsOS4zMDksNDYuNTQ0LDMuODMx"
    "LDY1LjE2Ni00LjkyN2MxMy4xNC05LjMxMywyMi40NDgtMjEuOTA3LDIzLjU0Ni0zNy4yNCAgIGMwLTU4"
    "LjU5Niw1LjQ5Mi0xMTMuOTAzLDAtMTcxLjk0OWMtMi43Mi03LjY2Ni0xNi45NzYtMi4xOTMtMTYuOTc2"
    "LTEwLjk1NmMxNi45NzYsMCwzNS4wNDctNS40NzMsNTEuNDc2LDAgICBjLTEuMDk2LDEwLjQwNi0xNy41"
    "MjUsMC41NTItMTkuNzE0LDEzLjY5bC0zLjgzNiwxNzMuMDUxYy0xLjY0MiwxNy41MjEtMTQuMjM1LDMy"
    "LjMwOC0yOS41NjgsNDIuMTYxICAgYy0zMS43NjEsMTQuMjQyLTc4Ljg1NSwxNi45OC0xMDYuMjM3LTku"
    "ODU0Yy0xMy4xNDQtMTAuOTUyLTE1LjMzMi0yNi44MzUtMTYuOTc1LTQyLjE2OFYzNjcuMDk0ICAgQzE3"
    "MjAuNjcsMzU3Ljc4NSwxNjk3LjEyLDM2Ni41NDMsMTcwOC4wNzYsMzU1LjA0NkwxNzA4LjA3NiwzNTUu"
    "MDQ2eiIvPgoJPHBhdGggZD0iTTE3NzEuNjAyLDMxMy45NzRjNi41NzUsMS4wOTIsMTUuMzM3LDEuNjQ0"
    "LDE2Ljk3OSwxMC40MDFjMi4xODgsNy42NzEtMi4xOTIsMTguMDcxLTEwLjk1NywyMC44MTEgICBjLTcu"
    "NjY1LTAuNTQ2LTE2LjQyMy0yLjczOS0xOC42MTYtMTAuOTUxQzE3NTYuODE4LDMyNC45MjcsMTc2Mi44"
    "NDMsMzE1LjYxOCwxNzcxLjYwMiwzMTMuOTc0eiIvPgoJPHBhdGggZD0iTTE4MjkuNjY4LDMxMy45NzRj"
    "OC4yMTctMi4xOTIsMTUuODYzLDMuMjg1LDE4LjYwMywxMC40MDFjMC41NDYsOC4yMTctMS4wOTgsMTUu"
    "ODg0LTguNzY0LDE5LjcxMyAgIGMtNy4xMTksMC41NTItMTkuMTYyLDAtMjEuMzU2LTkuODU0QzE4MTUu"
    "NDEyLDMyNC45MjcsMTgyMS45ODYsMzE3LjI2LDE4MjkuNjY4LDMxMy45NzRMMTgyOS42NjgsMzEzLjk3"
    "NHoiLz4KCTxwYXRoIGQ9Ik0xOTcwLjM4MywzNTYuMTM3YzIzLjAwNC03LjExNSw1MC45MzEtOC4yMTIs"
    "NzIuODM3LDEuMDk4YzYuMDE5LDIuMTkyLDkuMzA5LTMuODMxLDEzLjY5MS02LjAyNCAgIGM5LjMwOSwx"
    "MC40MDUsMTIuNTk0LDI3LjM4LDE1Ljg3OCw0Mi4xNjZjLTEyLjA0OCw4Ljc2NS0xMi41OTQtMTIuMDQ4"
    "LTIxLjkwMi0xNC43ODZjLTE3LjUyNS0xNy41MjEtNDUuNDUyLTI0LjA5Ni02Ny45MDUtMTMuNjkgICBj"
    "LTQ1LjQ1MiwyMi45OTktNTAuOTMsNzIuODMzLTUzLjExNywxMTguODM3YzMuMjgzLDM0LjQ5NSwxMC45"
    "NSw2OC45OTYsNDEuNjE2LDg5LjgwN2MxNi40MjksNy42NjYsMzcuMjM5LDExLjQ5Nyw1NS44NTYsNi41"
    "NjkgICBjMTcuNTI2LTQuMzgxLDMwLjY2Ni0yMC44MTEsNDQuMzU1LTMyLjMwOGM4Ljc2Myw0LjM4Mi0w"
    "LjU0NSw5Ljg1NC0xLjA5MiwxNC43ODdjLTI1LjE5MSwyOS4wMjMtNjUuMTY2LDM3Ljc4MS0xMDEuMjk0"
    "LDI2LjI4MyAgIGMtNDUuNDY3LTE2LjQyOS02MS44OTYtNjMuNTIyLTY1LjcxMi0xMDYuNzg2QzE5MDMu"
    "NTk1LDQzMS4xNjUsMTkyMC4wMDQsMzc4LjA0NiwxOTcwLjM4MywzNTYuMTM3TDE5NzAuMzgzLDM1Ni4x"
    "Mzd6Ii8+Cgk8cGF0aCBkPSJNMjEwNC4wMDYsNTc1LjE4NmMyLjE4OC02OC40NTEsMC41NDYtMTQxLjgz"
    "NCwxLjA5MS0yMDguMDkyYy00LjkyNy01LjQ3OC0xMi4wNDctNi4wMjMtMTguNjE2LTcuMTIxdi00Ljky"
    "NyAgIGMxOS43MTMtMS42NDMsNDIuMTY3LTEuNjQzLDYxLjg4MSwwYy0wLjU1MiwxMi4wNDgtMTcuNTI2"
    "LDEuMDkyLTE5LjcxNCwxNC43ODJjLTEuNjQzLDI5LjU3My0xLjY0Myw2MS44ODIsMCw5MS40NTVsODMu"
    "NzgzLTkwLjM1OCAgIGMzLjgzNi0xMi41OTQtMTMuMTQ1LTcuNjY3LTEzLjE0NS0xNS44NzljMTYuOTc5"
    "LTEuNjQzLDM2LjY5NC0xLjY0Myw1NC4yMTUsMGMtMS42NDMsOS44NTQtMTUuMzMyLDUuNDczLTIxLjM1"
    "NiwxMi4wNDggICBsLTc5Ljk1Miw4NC4zM3YzLjgzNmwxMDAuMjEzLDEyMS4wMjJjNC45MzIsOC43NTgs"
    "MTYuOTc5LDYuMDI0LDIwLjgxMSwxMy42ODljLTEwLjk1MiwzLjgzMS0yNS43MzgsMi43MzUtMzcuMjM1"
    "LDEuMDkyICAgYy0zOC44ODItNDIuNzEzLTcwLjA5OC04Ny4wNjgtMTA3LjMzMy0xMjkuNzhjLTQuMzY1"
    "LDM3Ljc4NS0yLjczOSw3OC44NTUtMS4wOTYsMTE3LjE4OGMzLjgzNiw5LjMwOSwxOC42MTctMC41NDcs"
    "MTguMDcxLDExLjUwMSAgIGgtNjIuOTczQzIwODMuNzQyLDU3Ny4zNzUsMjEwMS44MTMsNTg5LjQyMywy"
    "MTA0LjAwNiw1NzUuMTg2TDIxMDQuMDA2LDU3NS4xODZ6Ii8+CjwvZz4KPC9zdmc+"
])


def days_of_month(year, month):
    calendar = Calendar()
    dates = calendar.itermonthdates(year, month)

    def is_in_correct_month(date):
        return date.month == month

    return list(filter(is_in_correct_month, dates))


def is_workday(date):
    return date.weekday() < 5 and date not in holidays.DE(state='NI', years=date.year)


def random_distribution(days, hours, **kwargs):
    """
    Args:
        days (list):    List of dates.
        hours (int):    Number of hours to distribute.

    Kwargs:
        min_hours_per_day (int):    Minimum number of hours per day.
    """
    min_h_per_day = kwargs.get('min_hours_per_day', 4)
    num_days_required = ceil(hours / min_h_per_day)
    selected_days = sorted(random.sample(days, num_days_required))

    day_to_hours = {}
    for day in selected_days:
        assigned_hours = min(min_h_per_day, hours)
        day_to_hours[day] = assigned_hours
        hours -= assigned_hours

    return [(day, day_to_hours.get(day, 0)) for day in days]

def getDay(day, month, year):
    timestamp = mktime((year, month, day, 0, 0, 0, 0, 0, 0))
    lt = localtime(timestamp)
    monat = strftime('%a',lt)
    if monat == 'Mon':
        monat = 'Mo'
    elif monat == 'Tue':
        monat = 'Di'
    elif monat == 'Wed':
        monat = 'Mi'
    elif monat == 'Thu':
        monat = 'Do'
    elif monat == 'Fri':
        monat = 'Fr'
    elif monat == 'Sat':
        monat = 'Sa'
    elif monat == 'Sun':
        monat = 'So'

    datum = strftime('., %d.%m.%Y', localtime(timestamp))
    return monat + datum


def default_tabulation(days_and_hours, monat, jahr):
    args = read_args
    table = []

    for day, hours in days_and_hours:

        if hours == 0:
            row = {'day': getDay(day.day,monat,jahr), 'begin': None, 'end': None, 'pause': None,
                   'duration': None, 'noted': None}
        else:
            pause = 1 if hours > 4 else 0
            row = {
                'day': getDay(day.day,monat,jahr),
                'begin': 8,
                'end': 8 + hours + pause,
                'pause': pause,
                'duration': hours,
                'noted': day
            }

        table.append(row)

    return table


def read_args():
    opts = argparse.ArgumentParser(description='Create workhour reports.')
    opts.add_argument('firstname', metavar='FIRSTNAME', type=str,
                      help='First name')
    opts.add_argument('lastname', metavar='LASTNAME', type=str,
                      help='First name')
    opts.add_argument('hours', metavar='HOURS', type=int,
                      help='Number of hours')
    opts.add_argument('year', metavar='YEAR', type=int,
                      help='Year')
    opts.add_argument('month', metavar='MONTH', type=int,
                      help='Month')

    opts.add_argument('--institution', dest='institution', type=str,
                      default='FB Mathematik/Informatik, Institut für Informatik')

    opts.add_argument('--signature', dest='signature', type=str,
                      default='')

    args = opts.parse_args()
    return args


def main():
    lt = localtime()
    jahr, monat, tag = lt[0:3]

    datum = '%02i.%02i.%04i' % (tag, monat, jahr)
    args = read_args()
    days = days_of_month(args.year, args.month)
    workdays = list(filter(is_workday, days))

    # Distribute hours onto the days
    used_days = random_distribution(workdays, args.hours)

    # Merge assigned days and non-workdays
    day_to_hours = {day: hours for day, hours in used_days}
    days_and_hours = [(day, day_to_hours.get(day, 0)) for day in days]

    # Make output table
    table = default_tabulation(days_and_hours, args.month, args.year)

    # Generate html output

    def val2str(val):
        return "" if val is None else val

    def hours2string(hours):
        return "" if hours is None else '{:02d}:00'.format(hours)

    column_heads = [
        'Kalendartag',
        'Beginn (Uhrzeit)',
        'Pause (Dauer)',
        'Ende (Uhrzeit)',
        'Dauer (Summe)',
        'aufgezeichnet am',
        'Bemerkung'
    ]

    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('head'):
            doc.asis('<meta charset="utf-8">')
            with tag('style'):
                doc.asis("""
                    body { font-size:9pt; }
                    table { width:100%; }
                    .dates { border-collapse:collapse; }
                    .dates td { border:1pt solid black; padding:3pt; }
                    .formhead { width:40%; padding-right:10pt; }
                    .formval { border-bottom:1pt solid black; }
                    .sig { border-top:1pt solid black; width:45%; vertical-align:top; }
                    td { font-size:9pt; }
                """)
        with tag('body'):
            doc.stag('br')
            doc.stag('br')
            doc.stag('br')
            doc.stag('img', src='data:image/svg+xml;base64,{}'.format(UNI_LOGO),
                     style='width:150pt;')

            with tag('h2'):
                text('Erfassung der geleisteten Arbeitszeiten')
            with tag('table'):
                with tag('tr'):
                    with tag('td', klass='formhead'):
                        text('Name, Vorname der Hilfskraft')
                    with tag('td', klass='formval'):
                        text(args.lastname, ', ', args.firstname)
                with tag('tr'):
                    with tag('td', klass='formhead'):
                        text('Fachbereich / Organisationseinheit')
                    with tag('td', klass='formval'):
                        text(args.institution)
                with tag('tr'):
                    with tag('td', klass='formhead'):
                        text('Monat / Jahr')
                    with tag('td', klass='formval'):
                        text(args.month, ' / ', args.year)
                with tag('tr'):
                    with tag('td', klass='formhead'):
                        text('Monatsarbeitszeit laut Arbeitsvertrag')
                    with tag('td', klass='formval'):
                        text(args.hours, 'h')

            for _ in range(3): doc.stag('br')

            with tag('table', klass='dates'):
                with tag('tr'):
                    for column_head in column_heads[:-1]:
                        with tag('td'):
                            text(column_head)
                    with tag('td', style='width:30%;'):
                        text(column_heads[-1])

                for row in table:
                    with tag('tr'):
                        with tag('td'):
                            text(val2str(row['day']))
                        with tag('td'):
                            text(hours2string(row['begin']))
                        with tag('td'):
                            text(hours2string(row['pause']))
                        with tag('td'):
                            text(hours2string(row['end']))
                        with tag('td'):
                            text(hours2string(row['duration']))
                        with tag('td'):
                            text(str(row['noted'] or ""))
                        with tag('td'):
                            pass

                # Sum row
                with tag('tr'):
                    with tag('td'):
                        with tag('strong'):
                            text('Summe')
                    for _ in range(3):
                        with tag('td'):
                            pass
                    with tag('td'):
                        text(hours2string(args.hours))
                    for _ in range(2):
                        with tag('td'):
                            pass

            for _ in range(5): doc.stag('br')

            with tag('table'):
                with tag('tr'):
                    with tag('td'):
                        text(datum)
                        if args.signature != '':
                            sig = ''
                            if args.signature[0] == '/':
                                sig = args.signature
                            else:
                                sig = os.path.dirname(os.path.abspath(__file__)) + '/' + args.signature
                            print(sig)
                            doc.stag('img', src='{}'.format(sig), style='width:150pt;')
                    with tag('td'):
                        pass
                with tag('tr'):
                    with tag('td', klass='sig'):
                        text('Datum, Unterschrift der Hilfskraft')
                    with tag('td'):
                        pass
                    with tag('td', klass='sig'):
                        text('Datum, Unterschrift der Leiterin / des Leiters der OE')
                        doc.stag('br')
                        text('alternativ: Vorgesetzte / Vorgesetzter')

    # Generate report..

    report_filename = '{}-{:04d}-{:02d}.pdf'.format(
        args.lastname.lower(),
        args.year,
        args.month
    )

    proc = subprocess.Popen(['wkhtmltopdf', '-', report_filename], stdin=subprocess.PIPE)
    proc.communicate(input=bytes(doc.getvalue(), encoding='utf-8'))

    if proc.returncode != 0:
        print('Some error occurred during report generation :(')
        exit(1)
    else:
        print('Report written to "{}"'.format(report_filename))


if __name__ == '__main__':
    main()
