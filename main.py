import argparse
import os
from rich.console import Console
from rich.markdown import Markdown
from models import Problem

console = Console()

def parse_args():
    try:
        parser = argparse.ArgumentParser(description="Luogu CLI 工具")
        subparsers = parser.add_subparsers(dest="command", required=True)

        # lgcli parse PID
        parse_parser = subparsers.add_parser("parse", help="下载指定题目的题面、样例和题解")
        parse_parser.add_argument("pid", help="题目编号，例如 P1145")

        # lgcli view PID
        view_parser = subparsers.add_parser("view", help="查看题目描述")
        view_parser.add_argument("pid", help="题目编号，例如 P1145")

        # lgcli solution PID
        solution_parser = subparsers.add_parser("solution", help="查看题解列表或具体题解内容")
        solution_parser.add_argument("pid", help="题目编号，例如 P1145")
        solution_parser.add_argument("--id", help="指定题解文件名（不带.md）", default=None)

        return parser.parse_args()
    except argparse.ArgumentError as e:
        console.print(f"[red]参数解析错误：{e}[/red]")
        exit(1)
    except Exception as e:
        console.print(f"[red]未知错误：{e}[/red]")
        exit(1)


def cmd_view(pid):
    filename = f"{pid}/{pid}.md"
    if not os.path.exists(filename):
        console.print(f"[red]错误：{pid} 尚未解析，请先运行 lgcli parse {pid}[/red]")
        return

    try:
        console.clear()
        with open(filename, "r", encoding="utf8") as f:
            content = f.read()
        console.print(Markdown(content))
    except IOError as e:
        console.print(f"[red]读取文件失败：{e}[/red]")
    except Exception as e:
        console.print(f"[red]渲染Markdown失败：{e}[/red]")


def cmd_solution(pid):
    folder = f"{pid}/solutions"
    if not os.path.exists(folder):
        console.print(f"[red]错误：{pid} 题解尚未下载，请先运行 lgcli parse {pid}[/red]")
        return

    try:
        files = [f for f in os.listdir(folder) if f.endswith(".md")]
        if not files:
            console.print("[yellow]暂无题解。[/yellow]")
            return

        if args.id is None:
            console.clear()
            console.print("[bold blue]可用题解：[/bold blue]")
            for i, fname in enumerate(files):
                console.print(f"{i+1}. {fname[:-3]}")
            return

        selected_file = f"{args.id}.md"
        full_path = os.path.join(folder, selected_file)
        if not os.path.exists(full_path):
            console.print(f"[red]错误：题解 {selected_file} 不存在。请检查名称。[/red]")
            return

        console.clear()
        with open(full_path, "r", encoding="utf8") as f:
            content = f.read()
        console.print(Markdown(content))
    except IOError as e:
        console.print(f"[red]读取题解文件失败：{e}[/red]")
    except Exception as e:
        console.print(f"[red]渲染Markdown失败：{e}[/red]")


def cmd_parse(pid):
    try:
        p = Problem(pid)
        p.gen_all()
        console.print(f"[green]✅ 题目 {pid} 已成功下载到目录 '{pid}'[/green]")
    except ConnectionError as e:
        console.print(f"[red]网络连接错误：{e}[/red]")
    except RuntimeError as e:
        console.print(f"[red]数据解析错误：{e}[/red]")
    except Exception as e:
        console.print(f"[red]未知错误：{e}[/red]")


if __name__ == "__main__":
    try:
        args = parse_args()

        if args.command == "parse":
            cmd_parse(args.pid)
        elif args.command == "view":
            cmd_view(args.pid)
        elif args.command == "solution":
            cmd_solution(args.pid)
    except KeyboardInterrupt:
        console.print("\n[yellow]用户中断操作。[/yellow]")
    except Exception as e:
        console.print(f"[red]发生致命错误：{e}[/red]")