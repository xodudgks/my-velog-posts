## [[React] useEffect의 함정: setState 연쇄 호출(Cascading Updates) 탈출하고 렌더링 최적화하기](https://velog.io/@xodud_05/React-useEffect%EC%9D%98-%ED%95%A8%EC%A0%95-setState-%EC%97%B0%EC%87%84-%ED%98%B8%EC%B6%9CCascading-Updates-%ED%83%88%EC%B6%9C%ED%95%98%EA%B3%A0-%EB%A0%8C%EB%8D%94%EB%A7%81-%EC%B5%9C%EC%A0%81%ED%99%94%ED%95%98%EA%B8%B0)

**작성일:** Tue, 05 May 2026 14:03:41 GMT

**링크:** [바로가기](https://velog.io/@xodud_05/React-useEffect%EC%9D%98-%ED%95%A8%EC%A0%95-setState-%EC%97%B0%EC%87%84-%ED%98%B8%EC%B6%9CCascading-Updates-%ED%83%88%EC%B6%9C%ED%95%98%EA%B3%A0-%EB%A0%8C%EB%8D%94%EB%A7%81-%EC%B5%9C%EC%A0%81%ED%99%94%ED%95%98%EA%B8%B0)

---

<h2 id="intro">Intro</h2>
<p>SUMMIT 공연 웹페이지를 개발하며 가장 신경 썼던 부분 중 하나는, 관객들이 지난 공연과 다가올 공연의 포스터를 넘겨볼 수 있는 카루셀 UI였다.</p>
<p>데이터베이스(Supabase)에서 동적으로 포스터 리스트를 받아와 화면에 뿌려주는 기능을 구현하던 중, 콘솔창에서 찝찝한 노란색 경고창을 마주하게 되었다.</p>
<blockquote>
<p>Warning: react-hooks/set-state-in-effect</p>
</blockquote>
<p>단순한 경고로 넘어갈 수 있지만 프론트엔드 단의 성능과 직결되는 렌더링 최적화 문제였기에 원인을 깊게 파헤치고 구조를 개선해 본 과정을 기록해보았다.</p>
<hr />
<h2 id="문제-발생--끝없는-리렌더링의-늪">문제 발생 : 끝없는 리렌더링의 늪</h2>
<p>처음에 의도한 바는 다음과 같았다.</p>
<blockquote>
<p>서버에서 데이터를 받아오거나 카드가 삭제될 때, 현재 가리키고 있는 인덱스(activeIndex)가 전체 카드 개수를 넘어가면 에러가 나니까, useEffect를 써서 인덱스를 강제로 0으로 초기화해주자.</p>
</blockquote>
<p>하지만 카루셀 인덱스를 조정하기 위해 useEffect 내부에 setState를 사용했더니, 다음과 같은 ESLint 경고가 발생했다.</p>
<h3 id="문제의-코드-before">문제의 코드 (before)</h3>
<pre><code class="language-tsx">useEffect(() =&gt; {
  if (activeIndex &gt;= totalCards &amp;&amp; totalCards &gt; 0) {
    setActiveIndex(0);
  }
}, [activeIndex, totalCards]);</code></pre>
<p>이 코드는 리액트에서 지양하는 안티 패턴 중 하나였다. 바로 불필요한 연속 렌더링을 유발하기 때문이다.</p>
<ol>
<li>상태가 변함 -&gt; 1차 렌더링</li>
<li>화면을 그린 후 useEffect가 실행됨</li>
<li>조건에 맞아 setActiveIndex(0)이 실행됨</li>
<li>리액트가 화면을 또 다시 그림 (2차 렌더링)</li>
</ol>
<p>사용자는 한 번만 봐도 될 화면을 위해 리액트는 내부적으로 두 번씩 일을 하고 있었고, ESLint 역시 이를 감지하고 경고를 보내고 있었다.</p>
<h3 id="해결한-코드-after">해결한 코드 (After)</h3>
<pre><code class="language-tsx">const [activeIndex, setActiveIndex] = useState(0);
const [posterCards, setPosterCards] = useState([]);

const totalCards = posterCards.length;

const safeActiveIndex = totalCards === 0 
  ? 0 
  : Math.min(activeIndex, totalCards - 1);

const activeCard = totalCards &gt; 0 ? posterCards[safeActiveIndex] : null;</code></pre>
<p>리액트 공식 문서에서는 이럴 때 &quot;상태를 동기화하기 위해 useEffect를 쓰지 말고, 렌더링 중에 직접 계산하라&quot;고 권장한다.</p>
<p>굳이 activeIndex를 0으로 바꾸라고 리액트에게 억지로 명령(setState)할 필요 없이, 화면을 그리는 렌더링 시점에 안전한 인덱스를 실시간으로 계산해서 변수에 담아 쓰면 되는 것이었다.</p>
<p>이를 <strong>파생 상태(Derived State)</strong>라고 부른다.</p>
<hr />
<h2 id="개선된-코드의-핵심-원리">개선된 코드의 핵심 원리</h2>
<ol>
<li><p><strong>useEffect 완전 제거</strong> : 상태를 강제로 업데이트하는 사이드 이펙트를 없애 더블 렌더링을 방지했다.</p>
</li>
<li><p><strong>Math.min() 활용</strong> : 현재 인덱스가 아무리 커져도, 실제 배열의 마지막 인덱스(totalCards - 1)를 절대 넘지 못하도록 가둬두는 역할을 한다.</p>
</li>
<li><p><strong>데이터 안정성</strong> : 데이터가 하나도 없을 때(totalCards === 0)를 대비한 방어 로직까지 추가하여 에러를 원천 차단했다.</p>
</li>
</ol>
<hr />
<h2 id="결과-및-마무리-회고">결과 및 마무리 회고</h2>
<p><img alt="" src="https://velog.velcdn.com/images/xodud_05/post/d5f8a047-daf2-44a0-989a-d204967c4eef/image.jpg" /></p>
<p>이렇게 구조를 변경하니 지긋지긋하던 ESLint 경고가 사라졌다. useEffect에 의존하던 복잡한 상태 동기화 로직을 걷어내고, 렌더링 과정에서 값을 계산하게 만들어 앱의 성능과 코드의 가독성을 모두 잡을 수 있었다.</p>
<p>이번 트러블슈팅을 통해 단순히 <strong>화면이 돌아가게</strong> 만드는 것을 넘어, 리액트의 렌더링 라이프사이클을 이해하고 데이터 흐름을 최적화하는 방법에 대해 한 단계 더 배울 수 있었다. <strong>무심코 쓰기 쉬운 useEffect가 오히려 앱의 성능을 갉아먹을 수 있다는 점을 항상 명심하며 코드를 짜야겠다</strong>는 가르침도 얻었다!</p>
