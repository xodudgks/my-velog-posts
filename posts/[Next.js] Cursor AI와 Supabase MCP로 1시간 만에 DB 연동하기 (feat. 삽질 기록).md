## [[Next.js] Cursor AI와 Supabase MCP로 1시간 만에 DB 연동하기 (feat. 삽질 기록)](https://velog.io/@xodud_05/Next.js-Cursor-AI%EC%99%80-Supabase-MCP%EB%A1%9C-1%EC%8B%9C%EA%B0%84-%EB%A7%8C%EC%97%90-DB-%EC%97%B0%EB%8F%99%ED%95%98%EA%B8%B0-feat.-%EC%82%BD%EC%A7%88-%EA%B8%B0%EB%A1%9D)

**작성일:** Mon, 04 May 2026 16:27:49 GMT

**링크:** [바로가기](https://velog.io/@xodud_05/Next.js-Cursor-AI%EC%99%80-Supabase-MCP%EB%A1%9C-1%EC%8B%9C%EA%B0%84-%EB%A7%8C%EC%97%90-DB-%EC%97%B0%EB%8F%99%ED%95%98%EA%B8%B0-feat.-%EC%82%BD%EC%A7%88-%EA%B8%B0%EB%A1%9D)

---

<h2 id="supabase-도입">Supabase 도입</h2>
<h3 id="하드-코딩의-한계점">하드 코딩의 한계점</h3>
<p>summit-concert 페이지 제작을 하는데 프론트 코드만 작성하다보니 mock data만 가지고 페이지를 구성하려고 하니까 손수 노가다가 너무 비효율적으로 느껴졌다. 하지만 그렇다고 지금 내가 당장 SQL을 공부할 수 있는 것도 아닌 상황... 그래서 이번에 <strong>Supabase MCP</strong>를 활용해서 DB를 직접 설계해보기로 결심했다.</p>
<h3 id="supabase-도입-목표">Supabase 도입 목표</h3>
<p>이전에 동적 모션이 있는 카드 리스트를 만들었지만 이번에는 DB를 직접 설계해서 이제 나중에 6월달에 있을 정기공연의 포스터를 DB에만 넣으면 바로 프론트의 카드 리스트들이 바뀌도록 세팅하는 것이 가장 큰 목표이다.</p>
<hr />
<h2 id="데이터베이스-설계-및-입력-과정">데이터베이스 설계 및 입력 과정</h2>
<h3 id="테이블-생성">테이블 생성</h3>
<p><img alt="" src="https://velog.velcdn.com/images/xodud_05/post/0e3cc908-c560-4656-b29f-651c0725be6a/image.png" /> 먼저 setlist라는 테이블을 만들고 team_name, day, image_src 컬럼 구성해서 카드 리스트들을 쭉 만들었다. 만들 때 직접 team_name, day, image_src 구성을 전부 손수로 작성해야하다 보니 초기 파일 세팅의 중요함을 새삼 깨닫게 되었다. 또한 DB가 많아질수록 <strong>개발자들이 왜 어드민 페이지를 만드는지</strong>도 다시 한 번 깨닫게 되었다. (시간나면 다음에 도전해보도록 하겠다.)</p>
<h3 id="이미지-경로-전략">이미지 경로 전략</h3>
<h4 id="한글-파일명과의-작별-normalization-이슈">한글 파일명과의 작별 (Normalization 이슈)</h4>
<p>일단 처음에는 <strong>&quot;1-1 우연아니고운명.png&quot;</strong>처럼 직관적인 한글 이름을 사용했지만, 이를 즉시 영어로 교체했다. 웹 환경(특히 리눅스 서버)에서는 한글 파일명이 URL 인코딩(%EC%9A%B0...) 과정을 거치며 깨지거나, 서버 OS에 따라 파일을 찾지 못하는 404 에러가 빈번하게 발생하는 것을 깨닫게 되었다.</p>
<h4 id="nextjs-public-폴더와-절대-경로">Next.js public 폴더와 절대 경로</h4>
<p>Next.js의 특성을 활용한 효율적인 경로 지정 방식으로 <strong>절대 경로 방식</strong>은 public 폴더 안에 있는 자원은 배포 시 루트(/) 경로로 잡히는 특징이 있다. 따라서 DB의 image_src 컬럼에는 <strong>public/</strong>을 제외한 /day1-team1.png와 같은 절대 경로 형식으로 저장했다. 이렇게 하면 코드 내에서 <strong>Image src=&quot;{item.image_src}&quot;/</strong> 한 줄로 모든 포스터를 동적으로 불러올 수 있게 되었다.</p>
<h4 id="dbsupabase와-로컬-파일의-싱크sync">DB(Supabase)와 로컬 파일의 싱크(Sync)</h4>
<p>Supabase 테이블의 image_src 텍스트 값과 로컬 public 폴더 내의 실제 파일명이 1:1로 일치해야 한다는 것을 깨닫고 14개의 포스터 파일명을 바꾼 후, Supabase 대시보드에서 image_src 데이터를 일일이 수정하여 데이터 무결성을 맞췄다.</p>
<hr />
<h2 id="트러블슈팅--실전-배포-과정">트러블슈팅 : 실전 배포 과정</h2>
<p><strong>분량이 많아서 별도 포스팅으로 정리했다.</strong></p>
<h3 id="1-useeffect의-함정-setstate-연쇄-호출">1. useEffect의 함정: setState 연쇄 호출</h3>
<p><a href="https://velog.io/@xodud_05/React-useEffect%EC%9D%98-%ED%95%A8%EC%A0%95-setState-%EC%97%B0%EC%87%84-%ED%98%B8%EC%B6%9CCascading-Updates-%ED%83%88%EC%B6%9C%ED%95%98%EA%B3%A0-%EB%A0%8C%EB%8D%94%EB%A7%81-%EC%B5%9C%EC%A0%81%ED%99%94%ED%95%98%EA%B8%B0">https://velog.io/@xodud_05/React-useEffect의-함정-setState-연쇄-호출Cascading-Updates-탈출하고-렌더링-최적화하기</a></p>
<h3 id="2-배포의-늪-빈-배열과-forbidden-에러-탈출기">2. 배포의 늪: 빈 배열과 Forbidden 에러 탈출기</h3>
<p>(작성중...)</p>
<h2 id="구현-결과">구현 결과</h2>
<h2 id="마무리">마무리</h2>
