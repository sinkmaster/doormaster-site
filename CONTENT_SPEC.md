# doormaster 4개 사이트 — 공통 사양

## 사업자 정보 (모든 사이트 공통)
- 전화: 010-3092-7234  (tel:01030927234 / sms:01030927234)
- 사업자등록번호: 636-13-02485
- 주소: 경기도 용인시 기흥구 공세로 150-29
- 상담시간: 평일·주말 08:00~20:00
- 서비스 지역: 서울·경기·인천 전역 출장 시공

## 사이트 매핑 (디자인 참조원 → 대상)

| 대상 폴더 | 도메인 | 상호 | 디자인 참조 |
|---|---|---|---|
| main | doormaster.co.kr | 튼튼 욕실문턱 문지방 문틀 수리 | /root/fanref/main/index.html |
| door | door.doormaster.co.kr | 튼튼 방문 도어 문턱 수리 | /root/fanref/window/index.html |
| marble | marble.doormaster.co.kr | 튼튼 오래된 문턱 대리석 교체 | /root/fanref/kitchen/index.html |
| bath | bath.doormaster.co.kr | 튼튼 욕실 안방 문짝 교체 | /root/fanref/warehouse/index.html |

## 네이버 인증 코드 (각 사이트 head에 반드시 유지)
- main:   a76859a1e98f7b47678c130f792c3fefb8d8f9d9
- door:   8282e10927aff9c49e68428c3616feeaf7792127
- marble: 3a2c299c0f68f05b3a61565e500b040f5bff27a8
- bath:   09abe6e2d685d073849e18c2f620dc119d0eed42

형식: `<meta name="naver-site-verification" content="코드">`

## 지역 목록 (지역 섹션에 사용)
- 서울: 강남 서초 송파 강동 마포 용산 성동 광진 동대문 중랑 노원 도봉 강북 성북 종로 중구 은평 서대문 양천 강서 구로 금천 영등포 동작 관악
- 경기: 용인 수원 성남 분당 화성 동탄 안양 군포 의왕 과천 광명 부천 시흥 안산 평택 오산 이천 광주 하남 남양주 구리 의정부 고양 일산 파주 김포
- 인천: 남동구 미추홀구 연수구 부평구 계양구 서구 중구 동구 송도 청라

## 사이트 간 상호링크 (각 사이트 하단 또는 사이트맵 섹션)
- https://doormaster.co.kr — 튼튼 욕실문턱 문지방 문틀 수리 (욕실 문턱 누수·방수)
- https://door.doormaster.co.kr — 튼튼 방문 도어 문턱 수리 (문 처짐·안 닫힘)
- https://marble.doormaster.co.kr — 튼튼 오래된 문턱 대리석 교체
- https://bath.doormaster.co.kr — 튼튼 욕실 안방 문짝 교체

자기 자신은 제외하고 나머지 3개만 링크.

## 시공 사진 처리 (중요)
실제 사진이 아직 없습니다. 참조 사이트의 `<img src="photos/...">` 부분은
아래 형태의 자리표시자로 바꿉니다. 레이아웃(비율·크기)은 참조 사이트와 동일하게 유지.

```html
<div class="ph-placeholder">시공 사진 자리<br><small>images/case-1.jpg</small></div>
```

CSS 추가:
```css
.ph-placeholder{aspect-ratio:4/3;background:repeating-linear-gradient(45deg,#f2f4f6 0 12px,#eaedf0 12px 24px);
display:grid;place-items:center;text-align:center;color:#98a1ab;font-size:.8rem;padding:14px;line-height:1.6}
```
파일명은 case-1.jpg ~ case-6.jpg 순으로.

## 고객 후기 (중요)
실제 후기가 아직 없습니다. **후기 섹션은 통째로 넣지 마세요.**
참조 사이트에 후기 섹션이 있으면 삭제하고 다른 섹션으로 대체하거나 생략합니다.
(표시광고법 위반 소지가 있어 허위 후기를 넣으면 안 됩니다.)

## 절대 지켜야 할 것
1. 참조 사이트의 `<style>` 블록은 **최대한 그대로 유지** — 색상 변수, 폰트, 레이아웃, 반응형 규칙 전부.
2. 섹션 순서와 마크업 구조도 참조 사이트를 따를 것.
3. 텍스트만 문틀·문지방 수리 내용으로 교체.
4. 전화번호는 반드시 010-3092-7234. 환풍기 번호(010-2680-4538)가 남으면 안 됨.
5. "환풍기", "환기", "튼튼환풍시스템", "fanmaster" 문자열이 하나도 남으면 안 됨.
6. 참조 사이트의 지역별 하위 페이지(work-*.html, area-*.html) 링크는 만들지 말 것 —
   해당 파일이 없으므로 404가 남. 지역명은 링크 없는 텍스트로만 표시.
7. lang="ko", canonical, og 태그, JSON-LD(LocalBusiness/FAQPage) 포함.
8. 단일 HTML 파일 — CSS/JS 전부 인라인.
