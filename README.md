# Wescanner Client Project

## 🌟 Wescanner Project Front Family

- F.E<br />
  우혜림
  신지훈
  김보미
  
- B.E<br />
  [정지민](https://github.com/jiminnote)

<br />

## 🌟 What is Wescanner Client Project?

- 기존의 Wescanner 사이트를 모티브로 Django를 학습
- RDS, EC2, s3 등 AWS에 대해서 심도있게 학습하기.

<br />

## 🌟개발 인원 및 기간

- 개발기간<br />2022/07/04 ~ 2022/07/15 (총 11일간)
- 개발 인원<br />프론트엔드 3명, 백엔드 1명
- 2차 프로젝트 발표 자료<br />
  [Canva](https://www.canva.com/design/DAFGYKfsJU0/6C906o0qxN2_1WMIXOed_w/edit?utm_content=DAFGYKfsJU0&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## 🌟 적용 기술 및 구현 기능

### 적용 기술

- Python
- Django
- Mysql
- Json Web Token
- S3
- AWS
- Boto3


### 구현 기능

###  우리가 목표했던 필수 기능
- 이메일 로그인, 카카오 소셜 로그인
- 메인페이지 데이터 검색기능
- 호텔 리스트 (조건 필터링)


### 목표 외의 추가 기능
- 위시 리스트
- 리뷰 업로드
- 리뷰 삭제
- 호텔 리스트 정렬(저가순, 고가순, 추천순)

## How To Use

- 이메일 로그인.    : users 테이블에 없는 이메일로 로그인하게 되면 create, 존재하는 이메일로 로그인하게 되면 get.
- 카카오 소셜 로그인 : 카카오 로그인 시 유요한 계정의 경우 프론트 쪽에서 Athorization 토큰을 넘겨주고 해당 토큰을 이용해 wescanner API의 토큰을 생성하여 저장
- 메인 페이지      :  프론트 쪽에서 구현한 검색창에서 검색한 단어에 대한 관련 검색어가 나오도록 구현
- 호텔 리스트 페이지 : 메인 페이지에서 검색한 데이터 중 여러 조건들이 필터링이 되도록 구현
- 리뷰 업로드      : login_decorator를 이용하여 해당 유저의 review테이블에 boto3를 이용한 리뷰 이미지 업로드

## 기능 구현

### 🌱modeling
<img width="1086" alt="image" src="https://user-images.githubusercontent.com/95075455/179341155-31233654-6e8f-4e7c-95c1-1b318eb31e7f.png">


### 🌱API
<img width="1127" alt="image" src="https://user-images.githubusercontent.com/95075455/179341185-cd100248-a388-4c97-afbf-08de040a2a19.png">

#### core
- core.utils.py : Kakao API & login decorator 구현
- core.s3.py    :users.ReviewView에서 사용할 boto3 클래스화 
#### users
- users.EmailLoginView : 이메일 로그인 기능
- users.kakaoLoginView : 카카오 로그인 기능
- users.ReviewView     : 리뷰 기능

#### hotels
- hotels.SearchView    : 3단계에 걸친 카테고리 전체를 조회
- hotels.HotelListView : 특정 카테고리에 대한 정보 조회 & 특정 조건에 맞는 상품들 필터링


## 🌟Contributing

- Thanks to [Wecode](https://wecode.co.kr/)

## 🌟Reference

- [Skyscanner](https://www.aesop.com/)
- [unsplash.com](https://unsplash.com/)
- [dbdiagram.io](https://dbdiagram.io/home)

---

## 🌟Links

-  프로젝트 회고
  - [2차 프로젝트 회고록](https://velog.io/@jiminnote/Wescanner2%EC%B0%A8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9A%8C%EA%B3%A0%EB%A1%9D)

- Repository
  - [프론트엔드](https://github.com/wecode-bootcamp-korea/34-2nd-Wescanner-frontend)
  - [백엔드](https://github.com/wecode-bootcamp-korea/34-2nd-Wescanner-backend)
  
- API Documentation
  - [API Documentation](https://documenter.getpostman.com/view/21511958/UzQvs4eh)
  
## License

**모든 사진은 저작권이 없는 사진을 사용했습니다.**
