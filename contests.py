class Contest:
    def __init__(self, contest_id, unrated=False):
        self.contest_id = contest_id
        self.unrated = unrated
        self.contest_url = f"https://luogu.com.cn/contest/{contest_id}"
        self.join_url = f"https://www.luogu.com.cn/fe/api/contest/join/{contest_id}"

        # 动态设置 Referer
        self.headers = BASE_HEADERS.copy()
        self.headers['Referer'] = self.contest_url

        self.csrf_token = self._get_csrf_token()
        self._join_contest()

    def _get_csrf_token(self):
        resp = requests.get(
            self.contest_url,
            headers=self.headers,
            cookies=cookies
        )
        soup = BeautifulSoup(resp.text, 'html.parser')
        meta_tag = soup.find('meta', {'name': 'csrf-token'})
        if meta_tag:
            return meta_tag.get('content')
        else:
            raise ValueError("无法找到 csrf-token")

    def _join_contest(self):
        headers = self.headers.copy()
        headers['X-CSRF-Token'] = self.csrf_token

        data = {"unrated": str(self.unrated).lower()}

        resp = requests.post(
            self.join_url,
            headers=headers,
            cookies=cookies,
            json=data
        )

        print(f"Status Code: {resp.status_code}")
        print(f"Response Text: {resp.text}")