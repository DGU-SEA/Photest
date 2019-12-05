# Photest

> 소프트웨어공학 프로젝트

## Photo contest

> 사용자가 자신이 찍은 사진을 자유롭게 업로드할 수 있고, 다운로드 받을 수 있습니다. <br>
> 오늘의 해시태그를 가진 사진은 좋아요 순으로 랭크되며, 1등이 될 경우 그에 따른 보상을 받을 수 있는 웹사이트입니다.

## 개발 환경
<pre>
- Develop Tool: Django, python3
- OS : MAC OS, Windows 10
</pre>

## 시작하기 

### 1. 가상환경 만들기

> (전제 조건) python3, pip 설치

(1) virtualenv 설치
<pre>
$ pip install virtualenv
</pre>

(2) 가상환경 생성, 실행
<pre>
원하는 경로로 이동
$ python3 -m venv myvenv // myvenv를 원하는 이름으로 변경
$ source venv/bin/activate
(myvenv) $ // 성공
</pre>

(3) 가상환경 종료
<pre>
$ deactivate
</pre>

### 2. 라이브러리 설치
<pre>
$ python3 -m pip install --upgrade pip
$ myvenv/bin/pip install -r requirements.txt
</pre>

### 3. 실행하기
<pre>
$ python manage.py runserver
</pre>

## 팀원
<pre>
김예지 : Front-end
김혜지 : Back-end
이선영 : Back-end
한유진 : Front-end
</pre>

