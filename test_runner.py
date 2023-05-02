from rich.console import Console
from rich.table import Table
import subprocess
import re
import glob
import os
import ast
from rich.progress import track

console = Console()


def run_single_test(test_symbol):
    cmd = 'python manage.py test ' + test_symbol + '> result 2>&1'
    subprocess.call(cmd, shell=True)


def tear_down():
    cmd = 'rm result'
    subprocess.call(cmd, shell=True)

    cmd = 'mv db.sqlite3.bak db.sqlite3'
    subprocess.call(cmd, shell=True)

    cmd = 'rm db.sqlite3'
    subprocess.call(cmd, shell=True)


def gather_result(test_symbol):
    res = {
        "symbol": test_symbol,
        "status": 'Ready',
        "time": 'N/A'
    }
    with open('result', 'r') as f:
        content = f.read()
        if re.search(r'OK', content):
            res['status'] = 'PASS'
        if re.search(r'Fail', content):
            res['status'] = 'Failed'
        if re.search(r'Error', content):
            res['status'] = 'Error'
        time_consumption = re.findall(r'in\ ([\d\.]+)s', content)[0]
        res['time'] = time_consumption

    return res


def scan_symbol(path):
    res = []
    os.chdir(path)
    prefix = "tests"
    for file in glob.glob("test*.py"):
        scan_symbol_from_file(res, prefix, path + '\\' + file)
    return res


def scan_symbol_from_file(res, prefix, file):
    with open(file, 'r') as f:
        content = f.read()
        tree = ast.parse(content)
        filename = os.path.basename(file)
        filename = os.path.splitext(filename)[0]
        for i in tree.body:
            if isinstance(i, ast.ClassDef):
                scan_func_from_class(res, prefix, filename, i)


def scan_func_from_class(res, prefix, filename, i):
    for j in i.body:
        if isinstance(j, ast.FunctionDef):
            if j.name.startswith("test_"):
                res.append(
                    ".".join([prefix, filename, i.name, j.name]))


def make_summary(meta):
    table = {}
    for _meta in meta:
        status = _meta['status']
        _meta['time']
        symbol = _meta['symbol']

        symbol_token = symbol.split('.')
        class_def = symbol_token[-2]
        func_def = symbol_token[-1]
        v = {
            "name": func_def,
            "status": status,
            "time": str(int(float(_meta['time']) * 1000)) + 'ms'
        }
        if class_def in table.keys():
            table[class_def].append(v)
        else:
            table[class_def] = [v]

    return make_ui(table)


def make_ui(table_data):
    err = []
    passed = 0
    total = 0
    for key in table_data:
        table = Table(show_header=True, header_style="bold magenta",
                      title=key, title_style="b")
        table.add_column("Name")
        table.add_column("Status")
        table.add_column("Time", style='bright_cyan')
        v = table_data[key]
        for item in v:
            total += 1
            status_with_style = item['status']
            if status_with_style == 'PASS':
                status_with_style = '[green]' + status_with_style
                passed += 1
            else:
                status_with_style = '[red]' + status_with_style
                err.append(item)
            table.add_row(
                item['name'],
                status_with_style,
                item['time']
            )
        console.print(table)
    console.print("[cyan]In brief, " + str(total) + "test run, [green]" +
                  str(passed) + "pass, [red]" + str(total-passed) + "failed!")
    return err


def prepare_data():
    cmd = 'mv db.sqlite3 db.sqlite3.bak'
    subprocess.call(cmd, shell=True)

    cmd = 'python manage.py makemigrations core'
    subprocess.call(cmd, shell=True)

    cmd = 'python manage.py migrate'
    subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    prepare_data()
    testset = scan_symbol(os.path.dirname(__file__) + "\\tests")
    res = []
    os.chdir(os.path.dirname(__file__))

    for test in track(testset, description='Testing...'):
        run_single_test(test_symbol=test)
        res.append(gather_result(test_symbol=test))

    err = make_summary(res)
    console.log(err, style='bold red')
    tear_down()
