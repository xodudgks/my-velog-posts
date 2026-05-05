## [[Next.js-Supabase] 배포의 늪: 빈 배열과 Forbidden 에러 탈출기 (RLS & 환경 변수)](https://velog.io/@xodud_05/Next.jsSupabase-%EB%B0%B0%ED%8F%AC%EC%9D%98-%EB%8A%AA-%EB%B9%88-%EB%B0%B0%EC%97%B4%EA%B3%BC-Forbidden-%EC%97%90%EB%9F%AC-%ED%83%88%EC%B6%9C%EA%B8%B0-RLS-%ED%99%98%EA%B2%BD-%EB%B3%80%EC%88%98)

**작성일:** Tue, 05 May 2026 14:28:20 GMT

**링크:** [바로가기](https://velog.io/@xodud_05/Next.jsSupabase-%EB%B0%B0%ED%8F%AC%EC%9D%98-%EB%8A%AA-%EB%B9%88-%EB%B0%B0%EC%97%B4%EA%B3%BC-Forbidden-%EC%97%90%EB%9F%AC-%ED%83%88%EC%B6%9C%EA%B8%B0-RLS-%ED%99%98%EA%B2%BD-%EB%B3%80%EC%88%98)

---

<h2 id="intro">Intro</h2>
<p>SUMMIT 콘서트 웹페이지의 카루셀 렌더링 최적화까지 마치고, &quot;이제 진짜 끝났다!&quot;라는 마음으로 Vercel 배포를 진행했다.</p>
<p>로컬 환경(localhost:3000)에서는 Supabase와 완벽하게 통신하며 14장의 포스터가 아름답게 렌더링되는 것을 확인했기 때문에, 당연히 한 번에 성공할 줄 알았다.</p>
<p>하지만 인프라, 환경 설정 등에서 문제가 발생했고 이와 관련된 내용을 글로 정리해보았다.</p>
<hr />
<h2 id="1-소리-없는-에러-데이터-증발-사건-supabase-rls">1. 소리 없는 에러, 데이터 증발 사건 (Supabase RLS)</h2>
<h3 id="현상--통신은-200-ok-근데-데이터는-어딨지">현상 : 통신은 200 OK, 근데 데이터는 어딨지?</h3>
<p><img alt="" src="https://velog.velcdn.com/images/xodud_05/post/b2833011-74a5-4210-baed-3884720bdff9/image.png" /></p>
<p>로컬 개발 중 콘솔을 확인해 보니 통신 에러도 전혀 없었고, HTTP 상태 코드도 정상(200)이었다.</p>
<p>그런데 화면에는 내가 정성스럽게 넣은 DB와 다르게 예외 처리로 띄워둔 &quot;아직 등록된 포스터가 없습니다&quot;라는 문구만 덩그러니 떠있었다.</p>
<p>네트워크 탭을 뜯어보니 데이터를 받아오긴 했는데, 알맹이가 없는 빈 배열이 들어오고 있었다. </p>
<p>DB에는 분명 데이터가 있는데 왜 빈 배열을 주는 걸까?</p>
<h3 id="원인-secure-by-default-기본-보안-설정">원인: Secure by Default (기본 보안 설정)</h3>
<p>범인은 바로 Supabase의 RLS (Row Level Security) 정책이었다.</p>
<p>Supabase는 보안이 매우 철저해서, 테이블을 처음 생성하면 기본적으로 &quot;인증되지 않은 사용자는 데이터를 읽고 쓸 수 없도록&quot; 자물쇠를 꽉 채워둔다.</p>
<p>Next.js에서 데이터를 달라는 요청은 잘 도착했지만, Supabase 입장에선 빈 배열만 던져준 것이다.</p>
<h3 id="해결-용도에-맞는-보안-정책-설정">해결: 용도에 맞는 보안 정책 설정</h3>
<p>어짜피 현재 만들고 있는 웹은 공개용 콘서트 웹페이지이기 때문에 굳이 읽기 권한을 막아둘 필요가 없기 때문에 Supabase 대시보드에서 setlist 테이블의 RLS 정책을 Disable로 변경해 누구나 데이터를 조회할 수 있도록 공용 접근을 허용했다.</p>
<p>(만약 개인정보고 담기는 서비스라면 SELECT 정책을 세밀하게 세워야한다 ^^)</p>
<hr />
<h2 id="2-vercel-배포-지옥과-환경-변수">2. Vercel 배포 지옥과 환경 변수</h2>
<p>DB 자물쇠를 풀고 로컬에서도 성공을 한 뒤 Vercel에 코드를 푸시했다. 그런데 이번엔 아예 사이트 접속이 안 되거나 빌드가 터지는 현상이 발생했다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/xodud_05/post/928e1df4-0073-4fdd-ae31-5610fb79db66/image.png" /></p>
<h3 id="현상-접속했더니-403-forbidden">현상: 접속했더니 403 Forbidden...?</h3>
<p>빌드는 성공해서 초록색 체크(Ready)가 떴는데, 막상 Vercel이 준 링크로 접속하니 새하얀 화면에 403 Forbidden 에러만 떠 있었다.</p>
<h3 id="원인--해결">원인 &amp; 해결</h3>
<p>이건 코드 문제가 아니라 Vercel의 Deployment Protection (보호 기능) 때문이었다. </p>
<p>배포된 사이트를 아무나 보지 못하게 Vercel 자체적으로 로그인 자물쇠를 걸어버린 상태였다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/xodud_05/post/dab77178-1c48-4951-8b9f-94511cf8d945/image.png" /></p>
<p>Vercel Settings &gt; Deployment Protection 메뉴로 들어가서 Vercel Authentication을 Disabled로 변경하여 비밀번호 없이 누구나 사이트를 볼 수 있게 해제했다.</p>
<blockquote>
<h4 id="vercel-캐시-비우고-재배포하기">Vercel 캐시 비우고 재배포하기</h4>
<p>환경 변수를 수정했거나 설정을 바꾼 후에는 반드시 Vercel 대시보드에서 <strong>Redeploy</strong>를 해줘야 적용된다.
이때 기존 설정이 꼬이는 것을 막기 위해 Use existing Build Cache 체크를 해제하고 완전히 새롭게 빌드하는 것이 정신 건강에 좋은 것 같다...ㅎ</p>
</blockquote>
<hr />
<h2 id="결과-및-마무리-회고">결과 및 마무리 회고</h2>
<blockquote>
<p><strong>결국 모든 문제는 오타 하나, 체크박스 하나에 있었다.</strong></p>
</blockquote>
<p>AI의 도움을 받으면 코드 작성 속도는 비약적으로 빨라지지만 결국 환경 변수를 세팅하고 DB의 권한을 관리하고 인프라 배포 설정을 만지는 것은 온전히 개발자의 몫이라는 것을 뼈저리게 느낀 하루였다.</p>
<p>코드 로직이 아무리 완벽해도 인프라 설정이 받쳐주지 않으면 서비스는 세상에 나올 수 없다.</p>
<p>이번 삽질(?)을 통해 로컬 환경과 프로덕션 환경의 차이를 명확히 이해하게 되었다.</p>
<p>앞으로는 배포 환경 세팅부터 두 번 세 번 체크하는 습관을 들여야겠다!</p>
<p><img alt="" src="https://velog.velcdn.com/images/xodud_05/post/7acd58aa-7ba7-4f64-b464-46c02f04130e/image.png" /></p>
