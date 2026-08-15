# doormaster.co.kr — 튼튼 문턱·문지방 수리 사이트 4개

## 이 폴더가 뭔가요

사이트 4개의 소스입니다. **네 사이트는 색상·구조·디자인이 각각 다릅니다.**

| 폴더 | 주소 | 상호 |
|---|---|---|
| `main/` | https://doormaster.co.kr | 튼튼 욕실문턱 문지방 문틀 수리 |
| `door/` | https://door.doormaster.co.kr | 튼튼 방문 도어 문턱 수리 |
| `marble/` | https://marble.doormaster.co.kr | 튼튼 오래된 문턱 대리석 교체 |
| `bath/` | https://bath.doormaster.co.kr | 튼튼 욕실 안방 문짝 교체 |

호스팅은 Cloudflare Pages입니다. **GitHub에 push하면 1~2분 안에 자동 반영**됩니다.
FTP 업로드 같은 건 없습니다.

---

## 처음 한 번만 하는 준비

컴퓨터에 **Git**과 **Python**이 있어야 합니다.

- Git: https://git-scm.com/download/win
- Python: https://www.python.org/downloads/
  (설치 화면에서 **"Add Python to PATH"** 체크 꼭 하세요)

설치했으면 터미널을 열고 소스를 내려받습니다.

```bash
cd C:\작업폴더경로
git clone https://github.com/sinkmaster/doormaster-site.git
cd doormaster-site
```

이후로는 이 `doormaster-site` 폴더에서 작업하시면 됩니다.

---

## 평소 작업 순서

### 1. 내용 고치기

**사이트마다 디자인이 다릅니다.** 고칠 사이트의 `index.html` 을 직접 여세요.

| 고칠 사이트 | 파일 |
|---|---|
| doormaster.co.kr | `main/index.html` |
| door.doormaster.co.kr | `door/index.html` |
| marble.doormaster.co.kr | `marble/index.html` |
| bath.doormaster.co.kr | `bath/index.html` |

전화번호처럼 4개 전부 바꿔야 하는 건 4개 파일을 다 고쳐야 합니다.
Claude Code에 "4개 사이트 전화번호를 ○○로 바꿔줘" 라고 시키면 한 번에 해줍니다.

`build.py` 는 이제 **sitemap.xml 과 robots.txt 만** 만듭니다.
index.html 은 절대 건드리지 않으니 안심하고 직접 편집하셔도 됩니다.

### 2. 배포하기

터미널에서 한 줄이면 끝입니다.

**윈도우**
```
deploy.bat
```

**맥 / 리눅스 / Git Bash**
```bash
./deploy.sh
```

무엇을 고쳤는지 메모를 남기고 싶으면 뒤에 붙이세요.

```
deploy.bat 전화번호 변경
./deploy.sh "전화번호 변경"
```

이 명령 하나가 **sitemap 갱신 → 커밋 → GitHub push** 를 다 합니다.
push가 끝나면 Cloudflare가 알아서 4개 사이트를 다시 배포합니다.

### 3. 확인

1~2분 뒤 브라우저에서 열어보세요. 화면이 그대로면 **Ctrl + F5** 로 새로고침하시면 됩니다.

---

## 미리보기 (배포 전에 확인하고 싶을 때)

고친 `index.html` 파일을 그냥 **더블클릭해서 브라우저로 열어보면 됩니다.**
서버 없이도 그대로 보입니다. 확인 후 괜찮으면 `deploy` 를 실행하세요.

---

## 시공 사진 넣기

각 사이트 사진 자리는 `.ph-placeholder` 라는 이름으로 되어 있습니다.

각 사이트의 `images/` 폴더에 사진을 넣습니다.

```
main/images/case-1.jpg  ~  case-6.jpg
```

권장: 가로 800px 이상, 4:3 비율.

사진을 넣은 뒤 해당 `index.html` 에서
`<div class="ph-placeholder">시공 사진 자리...</div>` 부분을
`<img src="images/case-1.jpg" alt="설명">` 으로 바꾸면 됩니다.

Claude Code에 "main 사이트 시공사진 자리에 images 폴더 사진 넣어줘" 라고 시키면 알아서 해줍니다.

---

## 자주 겪는 문제

**`git push` 할 때 로그인하라고 나옴**
GitHub 계정으로 로그인하면 됩니다. 비밀번호 대신 토큰을 요구하면
GitHub → Settings → Developer settings → Personal access tokens 에서 발급하세요.
한 번 로그인하면 다음부터는 안 물어봅니다.

**`python` 명령을 못 찾는다고 나옴**
Python 설치 시 "Add Python to PATH"를 체크 안 한 겁니다. 다시 설치하면서 체크하세요.

**바꿨는데 사이트에 반영이 안 됨**
- Cloudflare 대시보드 → Workers & Pages → 해당 프로젝트 → Deployments 에서
  배포가 실패했는지 확인
- 브라우저 캐시일 수 있으니 Ctrl + F5

**실수로 잘못 올렸을 때**
```bash
git log --oneline        # 커밋 목록 확인
git revert 커밋번호       # 그 변경만 되돌리기
git push
```

---

## 다른 사람 컴퓨터에서 작업하다 왔다면

작업 시작 전에 최신 내용을 받아오세요.

```bash
git pull
```

---

## 검색등록 현황 (2026-08-15 기준)

- 구글 서치콘솔: 도메인 속성 `doormaster.co.kr` 등록 완료, 사이트맵 4개 제출 완료
- 네이버 서치어드바이저: 사이트 4개 소유확인 완료, 사이트맵 제출 완료

사이트 내용을 크게 바꿨을 때는 서치콘솔에서 사이트맵을 다시 제출할 필요는 없습니다.
구글이 주기적으로 다시 읽어갑니다.
