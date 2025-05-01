import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.exceptions import RequestException

# 加载 .env 文件
load_dotenv()

# 请求头与 Cookie
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) '
        'Gecko/20100101 Firefox/115.0'
    )
}

cookies = {
    "__client_id": os.getenv("CLIENT_ID"),
    "_uid": os.getenv("UID"),
    "cf_clearance": os.getenv("CF_CLEARANCE"),
    "C3VK": os.getenv("C3VK")
}

BASE_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36'
    ),
    'Origin': 'https://www.luogu.com.cn',
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
}


class Problem:
    def __init__(self, problem_id):
        self.problem_id = problem_id
        self.problem_url = f"https://luogu.com.cn/problem/{problem_id}"
        self.html = None
        self.json = None
        self.title = ""
        self.background = ""
        self.description = ""
        self.formatI = ""
        self.formatO = ""
        self.hint = ""
        self.samples = []

        try:
            resp = requests.get(self.problem_url, headers=headers, cookies=cookies, timeout=10)
            resp.raise_for_status()
            self.html = resp.text
        except RequestException as e:
            raise ConnectionError(f"无法访问题目页面：{self.problem_url}，错误：{e}")

        try:
            self.json = self._extract_json_from_html(self.html)['data']['problem']
        except (KeyError, ValueError) as e:
            raise RuntimeError(f"解析题目数据失败：{e}")

        self.title = self.json.get('title', '')
        self.background = self.json['contenu'].get('background', '')
        self.description = self.json['contenu'].get('description', '')
        self.formatI = self.json['contenu'].get('formatI', '')
        self.formatO = self.json['contenu'].get('formatO', '')
        self.hint = self.json['contenu'].get('hint', '')
        self.samples = self.json.get('samples', [])

    def _extract_json_from_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            script_tag = soup.find('script', {'id': 'lentille-context', 'type': 'application/json'})
            if not script_tag:
                raise ValueError("无法找到指定的JSON脚本标签")
            return json.loads(script_tag.string)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失败：{e}")
        except Exception as e:
            raise RuntimeError(f"HTML 解析失败：{e}")

    def gen_problem_md(self):
        try:
            md = f"# {self.title}"
            if self.background:
                md += f"\n\n## 【题目背景】\n{self.background}"
            if self.description:
                md += f"\n\n## 【题目描述】\n{self.description}"
            if self.formatI:
                md += f"\n\n## 【输入格式】\n{self.formatI}"
            if self.formatO:
                md += f"\n\n## 【输出格式】\n{self.formatO}"
            if self.hint:
                md += f"\n\n## 【提示】\n{self.hint}"

            with open(f"{self.problem_id}.md", "w", encoding="utf8") as f:
                f.write(md)
        except IOError as e:
            raise RuntimeError(f"写入题面Markdown文件失败：{e}")

    def gen_samples(self):
        try:
            os.makedirs("samples", exist_ok=True)
            cnt = 1
            for sample in self.samples:
                with open(f"samples/sample_{cnt}.in", "w", encoding="utf8") as f:
                    f.write(sample[0])
                with open(f"samples/sample_{cnt}.out", "w", encoding="utf8") as f:
                    f.write(sample[1])
                cnt += 1
        except (IOError, IndexError) as e:
            raise RuntimeError(f"写入样例文件失败：{e}")

    def gen_solutions(self):
        solution_url = f"https://luogu.com.cn/problem/solution/{self.problem_id}"
        try:
            resp = requests.get(solution_url, headers=headers, cookies=cookies, timeout=10)
            resp.raise_for_status()
        except RequestException as e:
            raise ConnectionError(f"无法访问题解页面：{solution_url}，错误：{e}")

        try:
            solutions_data = self._extract_json_from_html(resp.text).get("data", {})
            solutions = solutions_data.get("solutions", {}).get("result", [])
        except (KeyError, ValueError) as e:
            raise RuntimeError(f"解析题解数据失败：{e}")

        try:
            os.makedirs("solutions", exist_ok=True)
            for solution in solutions:
                author = solution.get('author', {})
                title = solution.get('title', '未命名题解')
                lid = solution.get('lid', 'unknown')
                content = solution.get('content', '')

                markdown_content = (
                    f"# {title}\n"
                    f"> By ![{author.get('name', '')}]({author.get('avatar', '')}?"
                    "x-oss-process=image/resize,m_fixed,h_30,w_30,image/circle,r_100/format,png)"
                    f"[{author.get('name', '')}](https://luogu.com.cn/user/{author.get('uid', '')})"
                    "\n\n"
                    f"{content}"
                )

                filename = f"solutions/{title}_{lid}.md"
                with open(filename, "w", encoding="utf8") as f:
                    f.write(markdown_content)
        except IOError as e:
            raise RuntimeError(f"写入题解文件失败：{e}")

    def gen_all(self):
        try:
            os.makedirs(self.problem_id, exist_ok=True)
            os.chdir(self.problem_id)
            self.gen_problem_md()
            self.gen_samples()
            self.gen_solutions()
        except Exception as e:
            raise RuntimeError(f"生成全部内容失败：{e}")


if __name__ == "__main__":
    try:
        p = Problem("P1145")
        p.gen_all()
    except Exception as e:
        print(f"[ERROR] 发生错误：{e}")