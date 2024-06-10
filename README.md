# 📖Novel Stella
스파르타 AI 6기 최종 프로젝트

# 📝프로젝트 소개
이번 프로젝트의 목표는 사용자들이 간단하게 즐길 수 있고 창작의 재미를 느낄 수 있는 **AI 기반 콘텐츠 생성 서비스**를 제공하는 것입니다. 기존의 AI 생성 서비스는 처음에는 결과물이 흥미롭지만, 시간이 지남에 따라 프롬프트 작성이나 요구사항 전달이 어려워지면서 사용자에게 스트레스를 주는 경우가 많았습니다. 

이를 해결하기 위해, 우리 서비스는 AI가 자동으로 제안하는 3가지 옵션 중에서 선택하거나 수정하여 최종 결과물을 생성하는 방식을 채택했습니다.

또한, 다양한 콘텐츠 형식을 지원하는 것이 큰 장점입니다. 텍스트 기반의 글 생성, AI 그림 생성 모델을 통한 이미지 생성등 사용자가 원하는 방식으로 창작할 수 있는 기능을 제공합니다. 이로 인해 사용자는 자신의 창작 욕구를 다양한 방식으로 표현할 수 있습니다.

결론적으로, 이 서비스는 사용자들이 창작의 재미를 느끼고 프롬프트 작성의 스트레스를 줄일 수 있도록 도와줍니다. 다양한 콘텐츠 형식을 지원하고, 최신 AI 모델을 빠르게 도입할 수 있는 유연한 구조를 통해 사용자들에게 최상의 창작 경험을 제공합니다.

# 🗓️개발 기간
- 24.05.13. ~ 24.06.12.
<br/>
# 팀 멤버 구성 🧑‍💻

<br/>

👩‍💻 **프론트엔드**

- 김동환 [@1489ehdghks] (https://github.com/1489ehdghks)
- 이환희 [@tia4613] (https://github.com/tia4613)

<br/>

👨‍💻 **백엔드**

- 허준혁 [@Juunsik] (https://github.com/Juunsik)
- 이혜민 [@LeeJS9856] (https://github.com/hy2min)

<br/>
<br/>

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


# 💭기술적 의사결정

<details>
<summary>tailwind VS zustand</summary>
<div>

Loot를 사용해서 전역적으로 색상 상태값들을 관리할지 고민했습니다.

react를 사용하지 않아도 이해하기 쉬운건 zustand와 index.scss에서 :Loot를 사용해서 색상을 가져오는 편이 더 좋을 것 같아 후자를 선택했습니다.

</div>
</details>

<details>
<summary>OpenAI assistant VS LangChain</summary>
<div>

비록 LangChain을 사용하는 것이 더 어려운 길일 수 있지만, 장기적인 관점에서 보았을 때 OpenAI보다 더 나은 LLM(대형 언어 모델)들이 출시되면 두고두고 후회할 것 같았습니다. 이러한 점에서 LangChain을 선택하는 것은 미래 지향적인 결정입니다.

LangChain은 다양한 LLM들과의 통합을 지원하여, 프로젝트가 특정 모델에 종속되지 않고 유연하게 대응할 수 있게 합니다. 이를 통해 프로젝트는 새로운 기술 발전에 발맞추어 지속적으로 업그레이드될 수 있습니다. 특히, LangChain의 체이닝 기능과 MemoryBuffer를 사용한 이전 답변 저장 기능은 프로젝트의 특성과 매우 잘 맞아떨어지기에 이를 사용하기로 결정했습니다.

</div>
</details>

<details>
<summary>DeepL VS google</summary>
<div>

`DeepL API`는 세계 각국 언어로의 우수한 번역 품질을 제공합니다. 우리는 이를 선택하여 동화를 다국어로 서비스하고 있습니다.

이 기술적 선택은 다문화적 고객층에 접근하는데 효과적이며, 글로벌 시장에서의 소통과 이해를 강화하여 향후 확장과 성장을 위한 강력한 기반을 제공합니다. 이를 통해 사용자는 다양한 언어로 동화를 즐길 수 있으며, 언어 장벽을 허물어 더 넓은 사용자층에 도달할 수 있습니다.

</div>
</details>

<details>
<summary>PostgreSQL</summary>
<div>

`PostgreSQL`는 안정적이고 확장성이 뛰어난 오픈 소스 관계형 데이터베이스 관리 시스템입니다. 우리는 이를 사용하여 사용자 데이터와 동화 콘텐츠를 안전하고 효율적으로 관리하고 있습니다.

이 기술적 선택은 데이터의 무결성과 보안을 보장하며, 대규모 데이터 처리와 복잡한 쿼리 실행에 적합합니다. 또한, 오픈 소스 특성상 비용 효율적이며, 다양한 기능과 강력한 커뮤니티 지원을 통해 시스템의 유연성과 확장성을 제공합니다.
</div>
</details>

<details>
<summary>React</summary>
<div>

`React`는 사용자 인터페이스를 구축하기 위한 오픈 소스 자바스크립트 라이브러리입니다. 우리는 이를 사용하여 동화 애플리케이션의 프론트엔드를 개발하고 있습니다.

이 기술적 선택은 컴포넌트 기반 아키텍처를 통해 재사용 가능하고 유지보수가 쉬운 코드를 작성할 수 있게 합니다. 또한, 가상 DOM을 활용하여 성능을 최적화하고, 사용자에게 빠르고 반응성 높은 경험을 제공합니다. React의 강력한 커뮤니티와 생태계는 다양한 라이브러리와 도구들을 활용할 수 있게 하여 개발 속도와 품질을 높여줍니다.
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
