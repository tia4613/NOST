# 📖Novel Stella
스파르타 AI 6기 최종 프로젝트

# 📝프로젝트 소개
이번 프로젝트의 목표는 사용자들이 간단하게 즐길 수 있고 창작의 재미를 느낄 수 있는 **AI 기반 콘텐츠 생성 서비스**를 제공하는 것입니다. 기존의 AI 생성 서비스는 처음에는 결과물이 흥미롭지만, 시간이 지남에 따라 프롬프트 작성이나 요구사항 전달이 어려워지면서 사용자에게 스트레스를 주는 경우가 많았습니다. 

이를 해결하기 위해, 우리 서비스는 AI가 자동으로 제안하는 3가지 옵션 중에서 선택하거나 수정하여 최종 결과물을 생성하는 방식을 채택했습니다.

또한, 다양한 콘텐츠 형식을 지원하는 것이 큰 장점입니다. 텍스트 기반의 글 생성, AI 그림 생성 모델을 통한 이미지 생성등 사용자가 원하는 방식으로 창작할 수 있는 기능을 제공합니다. 이로 인해 사용자는 자신의 창작 욕구를 다양한 방식으로 표현할 수 있습니다.

결론적으로, 이 서비스는 사용자들이 창작의 재미를 느끼고 프롬프트 작성의 스트레스를 줄일 수 있도록 도와줍니다. 다양한 콘텐츠 형식을 지원하고, 최신 AI 모델을 빠르게 도입할 수 있는 유연한 구조를 통해 사용자들에게 최상의 창작 경험을 제공합니다.

# 🗓️개발 기간
- 24.05.13. ~ 24.06.12.

# 🏗️ 서비스 아키텍처
![image](https://github.com/1489ehdghks/NOST/assets/159985538/2e302b58-b82c-4cd5-8aba-0421b72836e7)

# 🖥️개발 환경
<details>
<summary>프론트엔드</summary>
<div>

React: 프론트엔드 프레임워크 <br/>
Zustand: 상태 관리 라이브러리 <br/>
Cloudflare: CDN 및 보안 서비스

</div>
</details>

<details>
<summary>백엔드</summary>
<div>

Django: 백엔드 프레임워크 <br/>
Gunicorn: WSGI HTTP 서버 <br/>
PostgreSQL: 데이터베이스 관리 시스템 <br/>
Nginx: HTTP 및 리버스 프록시 서버

</div>
</details>

<details>
<summary>클라우드 인프라</summary>
<div>

Amazon EC2: 서버 호스팅 <br/>
Amazon S3: 스토리지 서비스 <br/>

</div>
</details>

<details>
<summary>추가 서비스</summary>
<div>

GitHub: 소스 코드 관리 및 협업 도구 <br/>
LangChain: 자연어 처리 라이브러리 <br/>
DeepL: 번역 서비스 <br/>
ChatGPT: 챗봇 서비스 <br/>
DALL-E: 이미지 생성 AI 

</div>
</details>

<br/>

# ✅주요 기능
<br/>
# FRONTEND

npm install 을 사용해서 node_modules를 설치 후
<br/>
npm start를 사용하여 실행


# BACKEND

가상환경을 키고
python manage.py runserver 사용하여 실행
<br/>
pip freeze > requirements.txt  package
