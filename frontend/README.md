## 처음 할때

npm install 을 사용해서 node_modules를 설치 후
npm start를 사용하여 실행



## 기술적 의사결정

- `zustand` : 전역상태 관리 라이브러리 (사용자 세션, UI 상태, 폼 데이터 등을 관리하기 위해 Zustand를 사용. 이는 상태 관리의 복잡성을 줄이고, 애플리케이션 상태를 더 쉽게 추적하고 업데이트 할 수있게 합니다.

- `Axios` : 인터셉터를 사용하여 요청마다 JWT access 토큰을 헤더에 자동으로 추가하고, 응답에서 refresh 토큰을 관리할 수 있다. 브라우저 환경에서 완벽하게 작동하므로, React 와 같은 프론트엔드의 라이브러리에서도 HTTP 요청을 쉽게 관리할 수 있습니다.
  
- `warning` : LF will be replaced by CRLF in (파일경로)The file will have its original line endings in your working directory
위의 에러를 아래의 명령어로 해결 (git config --global core.autocrlf true)

- 로그인,로그아웃 등 `AUTH` 와 관련된 기능들 LoginInstance,AuthInstance,SignupInstance 관리

- enter, esc를 사용한 `사용자 편의성` 추가



AI

나라 라이브러리 i18n-iso를 사용해서 전세계 표시할 수 있는 select를 생성함
i18n-iso가 나라로 표현되서 아쉬움. 언어로 변경함. 예를 들어 한국을 south korea로 나타나지만 이걸 Korean으로 변경함








# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.


