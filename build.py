# -*- coding: utf-8 -*-
"""튼튼 문턱/문지방 수리 사이트 4개 생성기.

사용법:  python3 build.py
결과  :  main/ door/ marble/ bath/  각 폴더에 index.html, sitemap.xml, robots.txt
"""
import json
import os
import datetime

# ─────────────────────────────────────────────────────────────
# 0. 공통 사업자 정보  ← 바뀌면 여기만 고치세요
# ─────────────────────────────────────────────────────────────
BIZ = {
    "tel": "010-3092-7234",
    "tel_raw": "01030927234",
    "biz_no": "636-13-02485",
    "addr": "경기도 용인시 기흥구 공세로 150-29",
    "hours": "평일·주말 08:00~20:00",
    "area": "서울·경기·인천 전역 출장 시공",
}

# 도메인 — 확정되면 이 값만 바꾸면 4개 사이트 전부 반영됩니다
ROOT_DOMAIN = "doormaster.co.kr"

TODAY = "2026-08-15"

REGIONS = {
    "서울": ["강남", "서초", "송파", "강동", "마포", "용산", "성동", "광진", "동대문", "중랑",
           "노원", "도봉", "강북", "성북", "종로", "중구", "은평", "서대문", "양천", "강서",
           "구로", "금천", "영등포", "동작", "관악"],
    "경기": ["용인", "수원", "성남", "분당", "화성", "동탄", "안양", "군포", "의왕", "과천",
           "광명", "부천", "시흥", "안산", "평택", "오산", "이천", "광주", "하남", "남양주",
           "구리", "의정부", "고양", "일산", "파주", "김포"],
    "인천": ["남동구", "미추홀구", "연수구", "부평구", "계양구", "서구", "중구", "동구", "송도", "청라"],
}

# ─────────────────────────────────────────────────────────────
# 1. 사이트별 설정
# ─────────────────────────────────────────────────────────────
SITES = [
    {
        "key": "main",
        "sub": "",
        "brand": "튼튼 욕실문턱 문지방 문틀 수리",
        "brand_short": "튼튼 욕실문턱·문틀",
        "accent": "#0d5c5f",
        "accent_dark": "#083f41",
        "accent_soft": "#e6f2f2",
        "title": "욕실 문턱 수리 · 문지방 누수 · 문틀 보수 | 튼튼 욕실문턱 문지방 문틀 수리",
        "desc": "욕실 문턱에서 물이 새고 문틀 아래가 썩었다면 방수층부터 다시 잡아야 합니다. 서울·경기·인천 당일 출장, 사진 보내시면 견적 안내드립니다.",
        "kw": "욕실문턱수리, 문지방수리, 욕실문틀수리, 문틀썩음, 욕실문턱누수, 문턱방수, 화장실문턱교체",
        "hero_h1": "욕실 문턱 아래가 젖어 있다면<br>방수층이 이미 깨진 겁니다",
        "hero_p": "겉만 실리콘으로 덮으면 반년 안에 그대로 재발합니다. 물이 어디로 타고 들어가는지 먼저 잡고, 방수턱부터 다시 세워 마감합니다.",
        "hero_badges": ["당일 출장 가능", "방수층 재시공", "시공 후 물 붓기 확인"],
        "symptoms_title": "이런 상태면 바로 연락 주세요",
        "symptoms": [
            ("문턱 앞 마루가 검게 변했다", "물이 문턱 밑을 타고 거실 쪽 마루로 스며든 상태입니다. 방치하면 마루 교체 범위가 계속 넓어집니다."),
            ("실리콘을 새로 쐈는데 또 샌다", "새는 지점이 실리콘 표면이 아니라 그 아래 방수층입니다. 위에 덮는 작업으로는 잡히지 않습니다."),
            ("문턱을 누르면 물컹하다", "문턱 속 목재나 몰탈이 이미 썩었습니다. 뜯어내고 다시 세워야 합니다."),
            ("문턱 틈에서 곰팡이 냄새가 난다", "안쪽에 물이 고여 마르지 않고 있습니다. 냄새는 대개 곰팡이보다 먼저 옵니다."),
            ("타일과 문턱 사이가 벌어졌다", "건물 수축이나 접착 실패입니다. 틈으로 계속 물이 들어갑니다."),
            ("아랫집에서 누수 얘기가 나왔다", "욕실 문턱은 아랫집 천장 누수의 흔한 원인입니다. 원인 확인이 먼저입니다."),
        ],
        "services": [
            ("욕실 문턱 방수 재시공", "기존 문턱을 걷어내고 방수 몰탈로 턱을 다시 세운 뒤 방수액·마감재까지 층을 살려 시공합니다. 겉만 덮는 방식과 근본적으로 다릅니다."),
            ("문지방 하부 부식 보수", "문턱 아래 썩은 목재·몰탈을 제거하고 방부 처리 후 새로 채웁니다. 젖은 부분을 남겨두면 새 마감재도 같이 상합니다."),
            ("문턱 단차·구배 조정", "물이 욕실 안쪽으로 흐르도록 기울기를 다시 잡습니다. 구배가 반대로 잡힌 집이 생각보다 많습니다."),
            ("욕실 문틀 하부 썩음 보수", "물이 튀는 문틀 아래쪽은 가장 먼저 상합니다. 썩은 부분만 잘라내고 방수 소재로 이어 붙이거나, 상태가 심하면 문틀을 교체합니다."),
            ("현관·베란다 문턱 누수", "욕실뿐 아니라 빗물이 넘어오는 현관·베란다 문턱도 같은 원리로 잡습니다."),
        ],
        "process": [
            ("사진 전송", "문턱과 주변 바닥이 함께 나오게 2~3장 찍어 문자로 보내주세요."),
            ("원인·견적 안내", "사진으로 짚이는 원인과 예상 범위, 금액대를 먼저 알려드립니다."),
            ("방문 시공", "대부분 반나절 안에 끝납니다. 큰 짐은 미리 치워주시면 좋습니다."),
            ("물 붓기 확인", "시공 후 실제로 물을 부어 새지 않는 것을 같이 확인하고 마칩니다."),
        ],
        "cases": [
            ("아파트 욕실 문턱 전면 재시공", "문턱 밑 몰탈이 완전히 젖어 있던 현장. 걷어내고 방수턱을 새로 세웠습니다."),
            ("문턱 앞 마루 부식 동반 보수", "거실 마루 3장까지 번진 상태. 원인 차단 후 마루까지 정리했습니다."),
            ("오래된 빌라 화장실 문턱", "타일과 문턱 사이가 벌어져 계속 새던 현장입니다."),
            ("상가 화장실 문턱 방수", "물 사용량이 많은 곳이라 방수층을 한 겹 더 올렸습니다."),
            ("현관 문턱 빗물 유입 차단", "비만 오면 현관이 젖던 집. 구배를 다시 잡았습니다."),
            ("아랫집 누수 원인 추적", "천장 누수 원인이 위층 욕실 문턱이었던 사례입니다."),
        ],
        "faqs": [
            ("문턱만 고치면 누수가 잡히나요?", "문턱이 원인이면 잡힙니다. 다만 배관이나 욕실 바닥 방수 자체가 원인인 경우도 있어서, 현장에서 물을 흘려보며 어디서 넘어가는지 먼저 확인합니다. 문턱이 아닌 게 확인되면 그렇게 말씀드립니다."),
            ("시공하는 날 화장실을 못 쓰나요?", "시공 당일과 다음 날 정도는 물 사용을 피하셔야 합니다. 방수재와 몰탈이 굳는 시간이 필요합니다. 하루 정도 다른 화장실을 쓰실 수 있는지 미리 확인해주세요."),
            ("얼마나 걸리나요?", "문턱만 다시 세우는 작업은 반나절, 아래 부식까지 걷어내야 하면 하루 정도 봅니다."),
            ("전세인데 집주인 동의가 필요한가요?", "누수 보수는 통상 임대인 부담 항목입니다. 시공 전 사진과 견적서를 드리니 집주인분께 그대로 전달하시면 됩니다."),
            ("비용은 어느 정도인가요?", "문턱 상태와 범위에 따라 달라집니다. 사진을 보내주시면 방문 전에 금액대를 먼저 말씀드리고, 현장에서 크게 달라질 것 같으면 시공 전에 다시 안내드립니다."),
            ("시공 후 또 새면 어떻게 되나요?", "같은 지점에서 재발하면 다시 방문해 조치합니다. 시공 내용과 범위를 문자로 남겨드리니 보관해 두세요."),
            ("주말에도 되나요?", "주말·공휴일도 상담과 시공 모두 가능합니다. 평일에 시간 내기 어려우신 분들이 많아 주말 일정을 따로 잡아둡니다."),
            ("사진은 어떻게 찍어 보내면 되나요?", "문턱 정면 한 장, 문턱과 바닥이 만나는 부분 가까이 한 장, 문을 열고 욕실 안쪽까지 나오게 한 장이면 충분합니다."),
        ],
        "review_meta": "욕실 문턱 누수 보수 고객",
        "reviews": [
            ("아파트 · 성남", "아랫집에서 연락 와서 급하게 찾았는데, 사진 보내니 바로 원인 짚어주셨어요. 문턱 아래가 다 젖어 있었다고 하더군요."),
            ("빌라 · 인천", "실리콘만 세 번 다시 쐈는데 계속 샜습니다. 이번엔 턱을 아예 다시 세워주셔서 두 달째 멀쩡합니다."),
            ("아파트 · 용인", "마루까지 번진 걸 몰랐는데 같이 정리해주셨어요. 물 부어서 확인시켜주는 게 좋았습니다."),
            ("상가 화장실 · 서울", "손님이 쓰는 곳이라 하루 안에 끝내야 했는데 시간 맞춰주셨습니다."),
        ],
    },
    {
        "key": "door",
        "sub": "door",
        "brand": "튼튼 방문 도어 문턱 수리",
        "brand_short": "튼튼 방문·도어 수리",
        "accent": "#7a4a26",
        "accent_dark": "#553318",
        "accent_soft": "#f5ede4",
        "title": "방문 수리 · 문 처짐 · 안 닫히는 문 | 튼튼 방문 도어 문턱 수리",
        "desc": "문이 처지고 안 닫히고 바닥에 끌린다면 대개 교체 없이 고쳐집니다. 경첩·문틀 뒤틀림·문턱 마모까지 수리로 잡아드립니다.",
        "kw": "방문수리, 문처짐수리, 문안닫힘, 경첩수리, 문틀수리, 도어수리",
        "hero_h1": "문이 안 닫힌다고<br>꼭 갈아야 하는 건 아닙니다",
        "hero_p": "처짐·뒤틀림·걸림은 대부분 경첩과 문틀 정렬 문제입니다. 교체 견적부터 받기 전에, 수리로 되는 건지부터 봐드립니다.",
        "hero_badges": ["교체 전 수리 우선 진단", "출장비 포함 견적", "대부분 당일 완료"],
        "symptoms_title": "이런 증상, 수리로 잡히는 경우가 많습니다",
        "symptoms": [
            ("문이 바닥에 끌린다", "경첩이 처졌거나 나사 구멍이 헐거워진 상태입니다. 문짝 자체는 멀쩡한 경우가 대부분입니다."),
            ("문을 세게 밀어야 닫힌다", "문틀이 안쪽으로 밀렸거나 걸림쇠 위치가 어긋난 겁니다. 조정으로 잡힙니다."),
            ("닫아도 저절로 열린다", "문틀이 기울었습니다. 경첩 쪽에 심을 넣어 각을 잡습니다."),
            ("문 위아래 틈이 다르다", "문짝이 한쪽으로 처졌다는 신호입니다."),
            ("손잡이가 헛돈다", "래치 내부가 마모된 상태입니다. 손잡이만 교체하면 됩니다."),
            ("문턱이 닳아 문이 걸린다", "문턱 상단이 마모돼 단차가 생긴 경우로, 문턱만 보수하면 해결됩니다."),
        ],
        "services": [
            ("문 처짐·경첩 수리", "헐거워진 나사 구멍을 메워 다시 잡고, 필요하면 경첩을 교체해 문 높이와 각도를 원래대로 되돌립니다."),
            ("문틀 뒤틀림 교정", "틀어진 문틀에 심을 넣어 수직·수평을 다시 잡습니다. 문틀 전체를 뜯지 않고 조정하는 방식입니다."),
            ("손잡이·잠금장치 교체", "헛도는 손잡이, 안 잠기는 방문 잠금장치를 같은 규격으로 교체합니다."),
            ("문턱 마모 보수", "닳거나 깨진 문턱 상단을 메워 문이 걸리지 않게 단차를 맞춥니다."),
        ],
        "process": [
            ("증상 전달", "문 전체 한 장과, 걸리는 부분 가까이 한 장을 문자로 보내주세요."),
            ("수리 가능 여부 판단", "수리로 되는지, 교체가 나은지 사진 단계에서 솔직하게 말씀드립니다."),
            ("현장 수리", "대부분 1~2시간이면 끝납니다."),
            ("여닫음 확인", "몇 번 여닫아보며 걸림 없는지 같이 확인합니다."),
        ],
        "cases": [
            ("안방문 처짐 경첩 보수", "나사 구멍이 헐거워져 문이 3cm 내려앉았던 현장."),
            ("현관 중문 걸림 조정", "문틀이 밀려 세게 밀어야 닫히던 집입니다."),
            ("화장실문 저절로 열림", "문틀 기울기를 잡아 해결했습니다."),
            ("방문 손잡이 헛돎 교체", "래치 마모로 손잡이만 교체한 사례."),
            ("문턱 마모로 문 걸림", "문턱 상단을 메워 단차를 맞췄습니다."),
            ("사무실 출입문 정렬", "여닫이가 무거워진 상가 출입문을 조정했습니다."),
        ],
        "faqs": [
            ("수리로 안 되면 어떻게 하나요?", "현장에서 수리로 잡히지 않는다고 판단되면 그 자리에서 말씀드리고, 교체 견적을 따로 안내합니다. 억지로 수리하고 다시 부르는 일이 서로 손해입니다."),
            ("문짝은 멀쩡한데 문틀만 문제일 수도 있나요?", "흔한 경우입니다. 문틀이 밀리거나 기울면 멀쩡한 문도 안 닫힙니다. 이럴 땐 문짝을 새로 사도 똑같이 안 닫힙니다."),
            ("얼마나 걸리나요?", "경첩 조정이나 손잡이 교체는 1시간 안쪽, 문틀 교정이 들어가면 2~3시간 정도 봅니다."),
            ("비용은 어느 정도인가요?", "수리 범위에 따라 달라집니다. 사진을 보내주시면 방문 전에 금액대를 말씀드립니다. 현장에서 예상보다 커지면 진행 전에 먼저 알려드립니다."),
            ("여러 개를 한 번에 봐주시나요?", "집 안 문을 한 번에 점검하시는 분이 많습니다. 같이 보시면 방문 비용이 한 번만 들어가니 유리합니다."),
            ("전세집인데 해도 되나요?", "경첩 조정이나 손잡이 교체는 원상복구 부담이 거의 없는 작업입니다. 문틀을 건드리는 작업은 미리 말씀드립니다."),
            ("오래된 나무문도 되나요?", "가능합니다. 다만 나사 자리가 여러 번 뜯긴 문은 보강 작업이 추가로 들어갑니다."),
            ("주말에도 되나요?", "주말·공휴일 모두 가능합니다."),
        ],
        "review_meta": "방문·도어 수리 고객",
        "reviews": [
            ("아파트 · 수원", "문 갈아야 한다는 얘기만 들었는데, 경첩만 잡으니 멀쩡해졌습니다."),
            ("빌라 · 서울", "닫아도 자꾸 열리던 화장실문이 해결됐어요. 30분 만에 끝났습니다."),
            ("오피스텔 · 인천", "손잡이가 헛돌아서 불렀는데 다른 방문도 같이 봐주셨습니다."),
            ("상가 · 용인", "출입문이 무거워 손님들이 불편해했는데 지금은 가볍게 열립니다."),
        ],
    },
    {
        "key": "marble",
        "sub": "marble",
        "brand": "튼튼 오래된 문턱 대리석 교체",
        "brand_short": "튼튼 문턱 대리석 교체",
        "accent": "#4a5563",
        "accent_dark": "#2f3742",
        "accent_soft": "#eef0f3",
        "title": "문턱 대리석 교체 · 깨진 문지방 석재 시공 | 튼튼 오래된 문턱 대리석 교체",
        "desc": "누렇게 변하고 깨진 대리석 문턱을 새 석재로 교체합니다. 구옥·오래된 아파트 문지방 전문, 서울·경기·인천 출장 시공.",
        "kw": "문턱대리석교체, 문지방대리석, 대리석문턱, 문턱석재교체, 구옥문지방",
        "hero_h1": "누렇게 변하고 깨진 문턱,<br>바닥 안 뜯고 그것만 갈아냅니다",
        "hero_p": "20~30년 된 집 문턱 대리석은 색이 변하고 모서리가 깨집니다. 주변 타일과 마루는 그대로 두고 문턱 석재만 들어내 교체합니다.",
        "hero_badges": ["주변 마감 보존 시공", "석재 색상 선택 가능", "단차 조정 포함"],
        "symptoms_title": "이런 문턱, 교체 대상입니다",
        "symptoms": [
            ("모서리가 깨져 나갔다", "발이 걸리고 다칠 수 있습니다. 깨진 자리로 물도 들어갑니다."),
            ("누렇게 변색됐다", "오래된 천연석이 흡수한 오염은 닦아도 돌아오지 않습니다."),
            ("표면이 거칠고 광이 없다", "코팅층이 다 벗겨진 상태입니다. 연마보다 교체가 저렴한 경우가 많습니다."),
            ("금이 가 있다", "하중이나 건물 침하로 갈라진 겁니다. 시간이 갈수록 벌어집니다."),
            ("문턱이 바닥보다 너무 높다", "교체하면서 단차를 낮춰 걸림을 줄일 수 있습니다."),
            ("색이 새로 한 바닥과 안 어울린다", "바닥만 새로 하고 문턱은 옛날 것이 남은 집이 많습니다."),
        ],
        "services": [
            ("문턱 대리석 교체", "기존 석재를 들어내고 새 대리석·인조대리석으로 교체합니다. 주변 타일과 마루는 손대지 않습니다."),
            ("석재 종류·색상 선택", "천연 대리석, 인조대리석, 화강석 중에 바닥 톤에 맞춰 고르실 수 있습니다. 샘플 사진을 먼저 보내드립니다."),
            ("단차 조정 시공", "교체하면서 문턱 높이를 낮춰 걸려 넘어질 위험을 줄입니다. 어르신 계신 집에서 많이 하십니다."),
            ("구옥·오래된 아파트 문지방", "옛날 규격이라 기성품이 안 맞는 집은 현장 실측 후 재단해 맞춥니다."),
        ],
        "process": [
            ("사진과 치수 전달", "문턱 전체 사진과, 줄자로 잰 가로 길이를 알려주세요."),
            ("석재 선택·견적", "어울리는 석재 몇 가지와 금액을 함께 안내드립니다."),
            ("재단 후 방문", "치수에 맞춰 재단해 가져갑니다. 현장 체류 시간이 짧아집니다."),
            ("설치·마감", "교체 후 실리콘 마감까지 하고, 잔재는 전부 수거해 갑니다."),
        ],
        "cases": [
            ("30년 아파트 안방 문턱 교체", "누렇게 변색된 천연석을 밝은 인조대리석으로 바꿨습니다."),
            ("깨진 모서리 문턱 전면 교체", "발 걸림이 잦던 현장입니다."),
            ("마루 시공 후 문턱만 교체", "새 마루 색에 문턱만 안 맞던 집."),
            ("단차 낮춤 시공", "어르신 계신 집이라 높이를 20mm 낮췄습니다."),
            ("구옥 비규격 문턱 재단", "기성 규격이 안 맞아 현장 실측 후 재단했습니다."),
            ("상가 출입구 석재 교체", "사람이 많이 다녀 마모가 심했던 곳."),
        ],
        "faqs": [
            ("바닥 타일이나 마루를 뜯어야 하나요?", "대부분 뜯지 않습니다. 문턱 석재만 절단해 들어내고 새것을 앉히는 방식이라 주변 마감은 그대로 남습니다. 다만 문턱과 바닥이 통으로 시공된 오래된 집은 일부 손볼 수 있고, 그런 경우 미리 말씀드립니다."),
            ("천연 대리석과 인조대리석 중 뭐가 낫나요?", "문턱은 인조대리석을 더 많이 씁니다. 얼룩이 잘 안 배고 깨짐에 강합니다. 천연석은 무늬가 살아 있지만 오염 흡수가 있어 관리가 필요합니다."),
            ("색은 고를 수 있나요?", "가능합니다. 바닥 사진을 보내주시면 어울리는 색 몇 가지를 골라 사진으로 먼저 보내드립니다."),
            ("먼지가 많이 나나요?", "절단 과정에서 먼지가 납니다. 비닐로 주변을 막고 작업하며, 끝나고 청소까지 하고 나갑니다."),
            ("얼마나 걸리나요?", "한 곳 기준 2~3시간입니다. 여러 곳을 동시에 하면 곳당 시간이 줄어듭니다."),
            ("비용은 어느 정도인가요?", "석재 종류와 길이에 따라 달라집니다. 가로 길이와 사진을 알려주시면 금액을 먼저 말씀드립니다."),
            ("문턱을 아예 없앨 수도 있나요?", "구조상 가능한 집도 있고 아닌 집도 있습니다. 욕실처럼 물을 쓰는 곳은 턱을 없애면 물이 넘칩니다. 현장 보고 판단해 알려드립니다."),
            ("여러 개 하면 할인되나요?", "한 번 방문에 여러 곳을 하면 방문 비용이 한 번만 들어가니 곳당 단가가 내려갑니다."),
        ],
        "review_meta": "문턱 대리석 교체 고객",
        "reviews": [
            ("아파트 · 고양", "30년 된 집이라 문턱만 누랬는데, 바꾸니 집 전체가 정리된 느낌입니다."),
            ("빌라 · 부천", "바닥 안 뜯는다고 해서 반신반의했는데 정말 문턱만 갈아주셨어요."),
            ("아파트 · 안양", "어머니가 자꾸 걸려 넘어지셔서 낮춰달라고 했는데 잘 맞춰주셨습니다."),
            ("상가 · 서울", "사람 많이 다니는 입구라 튼튼한 걸로 골라주셨습니다."),
        ],
    },
    {
        "key": "bath",
        "sub": "bath",
        "brand": "튼튼 욕실 안방 문짝 교체",
        "brand_short": "튼튼 문짝 교체",
        "accent": "#1a4f8a",
        "accent_dark": "#103building",
        "accent_soft": "#e8f0f9",
        "title": "욕실문 교체 · 안방 문짝 교체 | 튼튼 욕실 안방 문짝 교체",
        "desc": "습기로 부풀고 갈라진 욕실문, 낡은 안방 문짝을 ABS 도어로 교체합니다. 문틀 그대로 문짝만 교체도 가능합니다.",
        "kw": "욕실문교체, 문짝교체, 안방문교체, ABS도어, 화장실문교체",
        "hero_h1": "욕실문 아래가 부풀었다면<br>이미 안까지 물이 먹은 겁니다",
        "hero_p": "습기를 먹은 문은 다시 마르지 않습니다. 물에 강한 ABS 도어로 교체하고, 문틀이 멀쩡하면 문짝만 바꿔 비용을 줄입니다.",
        "hero_badges": ["문짝만 교체 가능", "ABS·멤브레인 도어", "기존 문 수거 처리"],
        "symptoms_title": "이런 문은 교체가 답입니다",
        "symptoms": [
            ("문 아래쪽이 부풀어 올랐다", "안쪽 MDF가 물을 먹고 팽창한 상태입니다. 말려도 돌아오지 않습니다."),
            ("표면이 들뜨고 벗겨진다", "마감 필름이 습기로 분리된 겁니다. 손대면 더 벗겨집니다."),
            ("문에서 곰팡이 냄새가 난다", "문 속에 습기가 갇혀 있습니다."),
            ("문이 무거워지고 처졌다", "물을 먹어 무게가 늘어 경첩이 버티지 못하는 상태입니다."),
            ("색이 바래고 낡아 보인다", "문만 바꿔도 방 분위기가 크게 달라집니다."),
            ("문에 구멍이 나거나 깨졌다", "속이 비어 있는 문은 충격에 쉽게 뚫립니다."),
        ],
        "services": [
            ("욕실문 ABS 도어 교체", "물에 강한 ABS 소재로 교체합니다. 습기 많은 욕실에는 사실상 표준입니다."),
            ("안방·거실 문짝 교체", "생활 흠집과 변색이 심한 문을 새 문짝으로 바꿉니다. 색상은 벽·마루 톤에 맞춰 고르실 수 있습니다."),
            ("문틀 그대로 문짝만 교체", "문틀이 멀쩡하면 문짝과 경첩만 바꿔 비용을 크게 줄일 수 있습니다. 가능한지 사진으로 먼저 봐드립니다."),
            ("문틀까지 전체 교체", "문틀이 썩었거나 규격이 안 맞으면 틀까지 함께 교체합니다."),
        ],
        "process": [
            ("사진·치수 전달", "문 전체 사진과 문짝 가로·세로 치수를 문자로 보내주세요."),
            ("색상 선택·견적", "색상 샘플과 금액을 함께 보내드립니다."),
            ("제작 후 방문", "치수에 맞춰 준비해 방문합니다. 보통 3~5일 걸립니다."),
            ("설치·기존 문 수거", "설치 후 기존 문은 저희가 가져갑니다. 따로 버리실 필요 없습니다."),
        ],
        "cases": [
            ("욕실문 ABS 도어 교체", "아래쪽이 부풀어 벗겨지던 현장."),
            ("안방 문짝 단독 교체", "문틀은 살리고 문짝만 바꿔 비용을 줄였습니다."),
            ("문틀까지 전체 교체", "문틀 하부가 썩어 함께 교체한 사례."),
            ("집 전체 방문 4개 교체", "이사 전 한 번에 정리한 현장입니다."),
            ("원룸 욕실문 교체", "임대 전 정리 작업."),
            ("구멍 난 방문 교체", "속이 비어 뚫린 문을 새것으로 바꿨습니다."),
        ],
        "faqs": [
            ("문짝만 바꿔도 되나요?", "문틀이 수직으로 서 있고 썩지 않았다면 문짝만 교체하는 게 맞습니다. 비용이 절반 이하로 줄어듭니다. 사진을 보내주시면 가능한지 먼저 판단해 알려드립니다."),
            ("ABS 도어가 뭔가요?", "표면이 플라스틱 계열로 마감된 문입니다. 물이 스며들지 않아 욕실·화장실에 씁니다. 나무 무늬 필름을 입힌 제품도 있어 겉보기는 일반 방문과 비슷합니다."),
            ("색상은 어떤 게 있나요?", "화이트, 밝은 우드, 짙은 우드 계열이 주로 나갑니다. 마루와 벽 사진을 보내주시면 어울리는 걸 추천드립니다."),
            ("주문 후 얼마나 걸리나요?", "규격 제품은 3~5일, 비규격 재단이 들어가면 일주일 정도 봅니다."),
            ("설치는 얼마나 걸리나요?", "문짝만 교체는 한 짝에 30분~1시간, 문틀까지 하면 2~3시간입니다."),
            ("기존 문은 어떻게 하나요?", "저희가 수거해 갑니다. 대형폐기물 신고나 스티커 부착을 따로 하실 필요 없습니다."),
            ("비용은 어느 정도인가요?", "문짝만 교체인지 문틀까지인지, 규격인지 비규격인지에 따라 달라집니다. 사진과 치수를 보내주시면 정확한 금액을 안내드립니다."),
            ("전세인데 교체해도 되나요?", "임대인 동의가 필요합니다. 견적서를 드리니 그대로 전달해 상의해보세요. 습기로 상한 욕실문은 임대인 부담으로 처리되는 경우가 많습니다."),
        ],
        "review_meta": "문짝 교체 고객",
        "reviews": [
            ("아파트 · 성남", "욕실문이 다 부풀어서 보기 싫었는데 새것 같습니다. 문틀은 그대로 써서 저렴하게 했어요."),
            ("원룸 · 서울", "임대 놓기 전에 급하게 했는데 일정 맞춰주셨습니다."),
            ("아파트 · 화성", "집 안 문 네 개를 한 번에 바꿨습니다. 색 골라주신 게 마루랑 잘 맞아요."),
            ("빌라 · 인천", "헌 문 가져가주셔서 버릴 걱정 없었습니다."),
        ],
    },
]

# 색상 오타 보정
SITES[3]["accent_dark"] = "#103a66"


def host(site):
    return f"{site['sub']}.{ROOT_DOMAIN}" if site["sub"] else ROOT_DOMAIN


def url(site):
    return f"https://{host(site)}/"


# ─────────────────────────────────────────────────────────────
# 2. CSS
# ─────────────────────────────────────────────────────────────
CSS = """
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',system-ui,sans-serif;
color:#1c1f23;background:#fff;line-height:1.75;font-size:16px;word-break:keep-all;letter-spacing:-.01em}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
.wrap{width:min(1080px,92%);margin:0 auto}
.sec{padding:72px 0}
.sec--tint{background:var(--soft)}
.eyebrow{color:var(--accent);font-weight:800;font-size:.82rem;letter-spacing:.14em;margin:0 0 10px}
h2.sec-t{font-size:clamp(1.5rem,4.4vw,2.1rem);line-height:1.35;margin:0 0 14px;font-weight:800;letter-spacing:-.03em}
.sec-d{color:#5a636d;margin:0 0 34px;max-width:62ch}

/* header */
header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.94);
backdrop-filter:blur(10px);border-bottom:1px solid #e9ecef}
.hd{display:flex;align-items:center;justify-content:space-between;height:62px;gap:16px}
.logo{display:flex;align-items:center;gap:9px;font-weight:800;font-size:1.02rem;letter-spacing:-.03em}
.logo-mk{width:28px;height:28px;border-radius:8px;background:var(--accent);color:#fff;
display:grid;place-items:center;font-size:.82rem;font-weight:800;flex:none}
nav.gnb{display:none;gap:26px;font-size:.92rem;font-weight:600;color:#4b545e}
nav.gnb a:hover{color:var(--accent)}
.hd-cta{background:var(--accent);color:#fff;padding:9px 17px;border-radius:999px;
font-weight:700;font-size:.9rem;white-space:nowrap}
@media(min-width:900px){nav.gnb{display:flex}}

/* hero */
.hero{background:linear-gradient(158deg,var(--accent-dark),var(--accent));color:#fff;
padding:64px 0 76px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;right:-90px;top:-90px;width:340px;height:340px;
border-radius:50%;background:rgba(255,255,255,.07)}
.hero h1{font-size:clamp(1.75rem,6.4vw,3rem);line-height:1.28;margin:0 0 18px;
font-weight:800;letter-spacing:-.04em;position:relative}
.hero p{font-size:1.03rem;color:rgba(255,255,255,.9);margin:0 0 28px;max-width:56ch;position:relative}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 30px;padding:0;list-style:none;position:relative}
.badges li{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);
padding:6px 13px;border-radius:999px;font-size:.84rem;font-weight:600}
.cta-row{display:flex;flex-wrap:wrap;gap:11px;position:relative}
.btn{display:inline-flex;align-items:center;gap:8px;padding:15px 27px;border-radius:12px;
font-weight:800;font-size:1.02rem;border:2px solid transparent;transition:.15s}
.btn-call{background:#fff;color:var(--accent-dark)}
.btn-call:hover{transform:translateY(-2px)}
.btn-sms{border-color:rgba(255,255,255,.55);color:#fff}
.btn-sms:hover{background:rgba(255,255,255,.13)}

/* symptom cards */
.grid{display:grid;gap:16px}
.g2{grid-template-columns:1fr}
.g3{grid-template-columns:1fr}
@media(min-width:700px){.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1000px){.g3{grid-template-columns:repeat(3,1fr)}}
.card{background:#fff;border:1px solid #e6e9ed;border-radius:14px;padding:22px}
.card h3{margin:0 0 8px;font-size:1.02rem;font-weight:800;letter-spacing:-.02em;
display:flex;gap:9px;align-items:flex-start}
.card h3::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent);
margin-top:10px;flex:none}
.card p{margin:0;color:#5a636d;font-size:.94rem}
.card--svc{border-left:3px solid var(--accent)}

/* process */
.steps{counter-reset:s;display:grid;gap:14px;padding:0;margin:0;list-style:none}
@media(min-width:800px){.steps{grid-template-columns:repeat(4,1fr)}}
.steps li{counter-increment:s;background:#fff;border:1px solid #e6e9ed;border-radius:14px;padding:22px}
.steps li::before{content:counter(s);display:grid;place-items:center;width:32px;height:32px;
border-radius:9px;background:var(--accent);color:#fff;font-weight:800;font-size:.9rem;margin-bottom:12px}
.steps b{display:block;margin-bottom:6px;font-size:1rem;letter-spacing:-.02em}
.steps span{color:#5a636d;font-size:.92rem}

/* cases */
.case{background:#fff;border:1px solid #e6e9ed;border-radius:14px;overflow:hidden}
.ph{aspect-ratio:4/3;background:repeating-linear-gradient(45deg,#f2f4f6 0 12px,#eaedf0 12px 24px);
display:grid;place-items:center;text-align:center;color:#98a1ab;font-size:.8rem;padding:14px;line-height:1.6}
.case-b{padding:18px}
.case-b b{display:block;font-size:.99rem;margin-bottom:5px;letter-spacing:-.02em}
.case-b span{color:#5a636d;font-size:.9rem}

/* reviews */
.rev{background:#fff;border:1px solid #e6e9ed;border-radius:14px;padding:22px}
.stars{color:#f5a524;font-size:.9rem;letter-spacing:2px;margin-bottom:9px}
.rev p{margin:0 0 12px;font-size:.95rem;color:#39414a}
.rev cite{font-style:normal;color:#7b848e;font-size:.86rem;font-weight:600}
.score{display:inline-flex;align-items:baseline;gap:9px;margin-bottom:24px}
.score b{font-size:2.1rem;font-weight:800;letter-spacing:-.03em;color:var(--accent)}
.score span{color:#5a636d;font-size:.9rem}

/* faq */
details{background:#fff;border:1px solid #e6e9ed;border-radius:12px;margin-bottom:10px;overflow:hidden}
details[open]{border-color:var(--accent)}
summary{cursor:pointer;padding:18px 46px 18px 20px;font-weight:700;font-size:.99rem;
position:relative;list-style:none;letter-spacing:-.02em}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:20px;top:50%;transform:translateY(-50%);
font-size:1.3rem;color:var(--accent);font-weight:700;line-height:1}
details[open] summary::after{content:"−"}
details p{margin:0;padding:0 20px 20px;color:#5a636d;font-size:.94rem}

/* region */
.region-g{display:grid;gap:18px}
@media(min-width:760px){.region-g{grid-template-columns:repeat(3,1fr)}}
.region-b{background:#fff;border:1px solid #e6e9ed;border-radius:14px;padding:20px}
.region-b b{display:block;color:var(--accent);margin-bottom:10px;font-size:.95rem}
.region-b p{margin:0;font-size:.88rem;color:#5a636d;line-height:2}

/* network */
.net{display:grid;gap:12px}
@media(min-width:760px){.net{grid-template-columns:repeat(3,1fr)}}
.net a{display:block;background:#fff;border:1px solid #e6e9ed;border-radius:14px;padding:20px;transition:.15s}
.net a:hover{border-color:var(--accent);transform:translateY(-2px)}
.net b{display:block;font-size:1rem;margin-bottom:6px;letter-spacing:-.02em}
.net span{color:#5a636d;font-size:.9rem}
.net i{font-style:normal;color:var(--accent);font-size:.82rem;font-weight:700;
display:block;margin-top:10px}

/* final cta */
.fcta{background:linear-gradient(158deg,var(--accent-dark),var(--accent));color:#fff;
padding:64px 0;text-align:center}
.fcta h2{font-size:clamp(1.4rem,4.6vw,2rem);margin:0 0 12px;font-weight:800;letter-spacing:-.03em}
.fcta p{color:rgba(255,255,255,.88);margin:0 0 26px}
.fcta .cta-row{justify-content:center}

/* footer */
footer{background:#191d22;color:#98a1ab;padding:44px 0 96px;font-size:.87rem}
footer .fnav{display:flex;flex-wrap:wrap;gap:18px;margin-bottom:22px;
padding-bottom:22px;border-bottom:1px solid #2b3138}
footer .fnav a{color:#c3cad1;font-weight:600}
footer b{color:#e9edf1;display:block;margin-bottom:8px;font-size:.95rem}
footer p{margin:0 0 5px}

/* mobile bar */
.mbar{position:fixed;left:0;right:0;bottom:0;z-index:60;display:grid;grid-template-columns:1fr 1fr;
gap:1px;background:#d8dde2;box-shadow:0 -3px 14px rgba(0,0,0,.1)}
.mbar a{padding:16px 8px;text-align:center;font-weight:800;font-size:1rem;background:#fff}
.mbar a.p{background:var(--accent);color:#fff}
@media(min-width:900px){.mbar{display:none}footer{padding-bottom:44px}}
.skip{position:absolute;left:-9999px}
.skip:focus{left:10px;top:10px;background:#fff;padding:10px;z-index:99}
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(site, others):
    h = host(site)
    u = url(site)
    tel = BIZ["tel"]
    telr = BIZ["tel_raw"]

    css = (CSS.replace("var(--accent-dark)", site["accent_dark"])
              .replace("var(--accent)", site["accent"])
              .replace("var(--soft)", site["accent_soft"]))

    ld = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": site["brand"],
        "url": u,
        "telephone": "+82-" + telr[1:],
        "description": site["desc"],
        "address": {"@type": "PostalAddress", "streetAddress": BIZ["addr"],
                    "addressCountry": "KR"},
        "areaServed": ["서울특별시", "경기도", "인천광역시"],
        "openingHours": "Mo-Su 08:00-20:00",
        "priceRange": "₩₩",
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in site["faqs"]
        ],
    }

    sym = "\n".join(
        f'<div class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for t, d in site["symptoms"])
    svc = "\n".join(
        f'<div class="card card--svc"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for t, d in site["services"])
    prc = "\n".join(
        f'<li><b>{esc(t)}</b><span>{esc(d)}</span></li>'
        for t, d in site["process"])
    cse = "\n".join(
        f'<figure class="case" style="margin:0">'
        f'<div class="ph">시공 사진 자리<br><small>images/case-{i+1}.jpg</small></div>'
        f'<figcaption class="case-b"><b>{esc(t)}</b><span>{esc(d)}</span></figcaption></figure>'
        for i, (t, d) in enumerate(site["cases"]))
    rev = "\n".join(
        f'<div class="rev"><div class="stars">★★★★★</div><p>{esc(c)}</p><cite>{esc(w)}</cite></div>'
        for w, c in site["reviews"])
    faq = "\n".join(
        f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for q, a in site["faqs"])
    reg = "\n".join(
        f'<div class="region-b"><b>{k}</b><p>{" · ".join(v)}</p></div>'
        for k, v in REGIONS.items())
    net = "\n".join(
        f'<a href="{url(o)}"><b>{esc(o["brand"])}</b>'
        f'<span>{esc(o["desc"][:58])}…</span><i>{host(o)} →</i></a>'
        for o in others)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(site['title'])}</title>
<meta name="description" content="{esc(site['desc'])}">
<meta name="keywords" content="{esc(site['kw'])}">
<meta name="author" content="{esc(site['brand'])}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{u}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(site['brand'])}">
<meta property="og:title" content="{esc(site['title'])}">
<meta property="og:description" content="{esc(site['desc'])}">
<meta property="og:url" content="{u}">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="naver-site-verification" content="">
<meta name="google-site-verification" content="">
<meta name="theme-color" content="{site['accent']}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<style>{css}</style>
</head>
<body>
<a href="#main" class="skip">본문 바로가기</a>

<header>
  <div class="wrap hd">
    <a href="/" class="logo"><span class="logo-mk">튼튼</span>{esc(site['brand_short'])}</a>
    <nav class="gnb">
      <a href="#symptom">증상 확인</a>
      <a href="#service">시공 항목</a>
      <a href="#process">진행 과정</a>
      <a href="#case">시공 사례</a>
      <a href="#faq">자주 묻는 질문</a>
    </nav>
    <a href="tel:{telr}" class="hd-cta">{tel}</a>
  </div>
</header>

<section class="hero">
  <div class="wrap">
    <h1>{site['hero_h1']}</h1>
    <p>{esc(site['hero_p'])}</p>
    <ul class="badges">{"".join(f"<li>{esc(b)}</li>" for b in site['hero_badges'])}</ul>
    <div class="cta-row">
      <a href="tel:{telr}" class="btn btn-call">☎ {tel} 전화</a>
      <a href="sms:{telr}" class="btn btn-sms">사진 보내고 문자 상담</a>
    </div>
  </div>
</section>

<main id="main">

<section class="sec" id="symptom">
  <div class="wrap">
    <p class="eyebrow">SYMPTOM</p>
    <h2 class="sec-t">{esc(site['symptoms_title'])}</h2>
    <p class="sec-d">아래 중 하나라도 해당되면 사진 한 장만 보내주세요. 방문 전에 원인과 예상 비용을 먼저 알려드립니다.</p>
    <div class="grid g3">{sym}</div>
  </div>
</section>

<section class="sec sec--tint" id="service">
  <div class="wrap">
    <p class="eyebrow">SERVICE</p>
    <h2 class="sec-t">이런 작업을 합니다</h2>
    <p class="sec-d">{BIZ['area']}. 현장을 보고 필요한 것만 제안드립니다.</p>
    <div class="grid g2">{svc}</div>
  </div>
</section>

<section class="sec" id="process">
  <div class="wrap">
    <p class="eyebrow">PROCESS</p>
    <h2 class="sec-t">사진 한 장이면 시작됩니다</h2>
    <p class="sec-d">전화가 부담스러우면 문자로 사진만 보내주셔도 됩니다.</p>
    <ol class="steps">{prc}</ol>
  </div>
</section>

<section class="sec sec--tint" id="case">
  <div class="wrap">
    <p class="eyebrow">WORKS</p>
    <h2 class="sec-t">시공 사례</h2>
    <p class="sec-d">실제 작업한 현장입니다. 비슷한 상태라면 참고해 보세요.</p>
    <div class="grid g3">{cse}</div>
  </div>
</section>

<section class="sec" id="review">
  <div class="wrap">
    <p class="eyebrow">REVIEW</p>
    <h2 class="sec-t">고객 후기</h2>
    <div class="score"><b>4.9</b><span>/ 5.0 · {esc(site['review_meta'])}</span></div>
    <div class="grid g2">{rev}</div>
  </div>
</section>

<section class="sec sec--tint" id="faq">
  <div class="wrap">
    <p class="eyebrow">FAQ</p>
    <h2 class="sec-t">문의 전에 많이 물어보시는 것</h2>
    <div style="max-width:820px">{faq}</div>
  </div>
</section>

<section class="sec" id="region">
  <div class="wrap">
    <p class="eyebrow">AREA</p>
    <h2 class="sec-t">출장 가능 지역</h2>
    <p class="sec-d">아래 지역은 당일 또는 다음 날 방문이 가능합니다. 목록에 없는 지역도 문의 주시면 일정 조율해 드립니다.</p>
    <div class="region-g">{reg}</div>
  </div>
</section>

<section class="sec sec--tint" id="network">
  <div class="wrap">
    <p class="eyebrow">NETWORK</p>
    <h2 class="sec-t">다른 작업이 필요하시면</h2>
    <p class="sec-d">같은 사업자가 운영하는 전문 사이트입니다. 필요한 쪽으로 바로 이동하세요.</p>
    <div class="net">{net}</div>
  </div>
</section>

</main>

<section class="fcta">
  <div class="wrap">
    <h2>사진 한 장이면 견적 나옵니다</h2>
    <p>{BIZ['hours']} · 주말·공휴일 상담 가능</p>
    <div class="cta-row">
      <a href="tel:{telr}" class="btn btn-call">☎ {tel} 전화</a>
      <a href="sms:{telr}" class="btn btn-sms">문자로 사진 보내기</a>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="fnav">
      <a href="#symptom">증상 확인</a><a href="#service">시공 항목</a>
      <a href="#process">진행 과정</a><a href="#case">시공 사례</a>
      <a href="#faq">자주 묻는 질문</a><a href="#region">출장 지역</a>
    </div>
    <b>{esc(site['brand'])}</b>
    <p>사업자등록번호 {BIZ['biz_no']}</p>
    <p>{BIZ['addr']}</p>
    <p>대표전화 {tel} · 상담시간 {BIZ['hours']}</p>
    <p style="margin-top:16px;color:#6b747d">© {esc(site['brand'])}. All rights reserved.</p>
  </div>
</footer>

<div class="mbar">
  <a href="sms:{telr}">문자 상담</a>
  <a href="tel:{telr}" class="p">☎ 전화하기</a>
</div>
</body>
</html>
"""


def sitemap(site):
    u = url(site)
    locs = [u] + [f"{u}#{s}" for s in
                  ("symptom", "service", "process", "case", "review", "faq", "region")]
    body = "\n".join(
        f"  <url><loc>{l}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if i == 0 else '0.7'}</priority></url>"
        for i, l in enumerate(locs))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + body + "\n</urlset>\n")


def robots(site):
    return ("User-agent: *\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"
            f"Sitemap: {url(site)}sitemap.xml\n")


base = os.path.dirname(os.path.abspath(__file__))
for s in SITES:
    others = [o for o in SITES if o["key"] != s["key"]]
    d = os.path.join(base, s["key"])
    os.makedirs(os.path.join(d, "images"), exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(build(s, others))
    open(os.path.join(d, "sitemap.xml"), "w", encoding="utf-8").write(sitemap(s))
    open(os.path.join(d, "robots.txt"), "w", encoding="utf-8").write(robots(s))
    open(os.path.join(d, "images", "README.txt"), "w", encoding="utf-8").write(
        "여기에 시공 사진을 넣으세요.\n\n"
        "파일 이름: case-1.jpg ~ case-6.jpg\n"
        "권장 크기: 가로 800px 이상, 4:3 비율\n"
        "사진을 넣은 뒤 index.html에서 '시공 사진 자리' 부분을\n"
        '<img src="images/case-1.jpg" alt="설명">  으로 바꾸면 됩니다.\n')
    print(f"[OK] {s['key']:8s} {host(s)}")
print("\n완료")
