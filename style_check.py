"""리포트 글의 금지어·문체 검사.

정본은 nurilab-vault `03.System/Feedback Rules.md`의 글쓰기·문체 절이고, 낱말 목록은
김누리 PC의 `~/.claude/hooks/banned_words.py`와 같다. 낱말을 더할 때는 셋을 같이 고친다.

검사를 기억에 맡기지 않으려고 만든 것이다. 에이전트는 `agent_pipeline.py check`로
돌려 0건이 될 때까지 고친 뒤 assemble 한다.
"""

import re

# (정규식, 이름, 대신 쓸 말)
PATTERNS = [
    (r"(?<!깨)닫", "닫", "완료하다 / 끝내다 / 더 해볼 게 없다"),
    (r"천장", "천장", "성능 상한"),
    (r"나침반", "나침반", "좋은 후보를 골라낼 신호"),
    (r"관문", "관문", "통과 기준 / 선결 조건"),
    (r"되감", "되감기", "되돌리기"),
    (r"계기", "계기", "측정값 / 이유"),
    (r"걸음\s*[0-9]", "걸음 N", "1단계 / step 1"),
    (r"여유분", "여유분", "얻을 수 있는 최대 이득"),
    (r"문턱", "문턱", "통과 기준 / 기준값"),
    (r"단서", "단서", "실마리 / 조건"),
    (r"열린다|열렸다", "열린다", "이 방법을 시도해볼 수 있게 됐다"),
    (r"사다리", "사다리", "단계 / 순서"),
    (r"무대", "무대", "실험 환경 / 장면"),
    (r"에스컬레이", "에스컬레이션", "다음 단계로 올림"),
    (r"접(는다|었다|자|을까)", "접다", "중단"),
    (r"값이 크|값의 전부", "값이 크다", "중요하다"),
    (r"벌크", "벌크", "N건 묶음"),
    (r"나란히", "나란히", "어디에 무엇이 오는지 그대로"),
    (r"교락", "교락", "confounding"),
    (r"쏠림", "쏠림", "bias / 한쪽으로 치우침"),
    (r"서 있", "서 있다", "지금 쓰고 있는 설명"),
    (r"무너[지졌져]", "무너지다", "0.92에서 0.37로 낮아짐 (수치를 적음)"),
    (r"버티|버틴", "버틴다", "N~M을 유지함"),
    (r"붕괴", "붕괴", "크게 낮아짐 (mode collapse 는 원어로)"),
    (r"깎", "깎는다", "낮춘다"),
    (r"떨어[지졌져짐]", "떨어지다", "낮아짐 / 내려감 (물체가 실제로 떨어지면 그대로)"),
    (r"깨[지졌져짐]", "깨지다", "틀린 것으로 드러남 / 성립하지 않음 (물건이 실제로 깨지면 그대로)"),
    (r"순서가\s*(바뀌|뒤집)", "순서가 바뀌었다", "순위가 바뀌었다"),
    (r"뼈대", "뼈대", "구조"),
    (r"가로질러", "가로질러", "여러 X에 걸쳐"),
    (r"(?i)generalization ladder|blunt instrument|buys nothing|sets the bar", "영어 비유", "평범한 서술"),
    (r"[①-⑳㉠-㉭⑴-⒇⒜-⒵]", "원문자", "일반 숫자"),
    (r"—", "줄표(—)", "문장을 끊거나 콜론(:)"),
    (r"(습니다|합니다|입니다)(\.|$)", "~습니다체", "음슴체(~함/~임)"),
    (r"[가-힣](했|였|한|된|이)다\.(\s|$)", "~다 평서형", "음슴체(~함/~임)"),
]

LONG_SENTENCE = 150  # 글자. 이보다 긴 문장은 쪼갤 후보로 표시함


def _sentences(text):
    # 길이는 화면에 보이는 글자로 잰다: markdown 링크는 글자만, 굵게 표시는 뺀다
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text).replace("**", "")
    for line in text.split("\n"):
        line = line.strip().lstrip("- ").strip()
        for s in re.split(r"(?<=[.!?])\s+|(?<=[임함됨음])\.\s*", line):
            s = s.strip()
            if s:
                yield s


def check_text(text):
    """Return a list of (name, suggestion, snippet)."""
    hits = []
    if not text:
        return hits
    for pat, name, sugg in PATTERNS:
        for m in re.finditer(pat, text):
            a, b = max(0, m.start() - 25), min(len(text), m.end() + 25)
            hits.append((name, sugg, text[a:b].replace("\n", " ")))
    for s in _sentences(text):
        if len(s) > LONG_SENTENCE:
            hits.append(("긴 문장", f"{len(s)}자, 두 문장으로 쪼갬", s[:60] + "…"))
    return hits


SKIP_KEYS = {"score", "field", "links", "text_source", "venue_score"}


def check_deep(d):
    """Check every Korean text field of one deep-review dict. Returns [(field, name, sugg, snippet)]."""
    out = []
    for k, v in (d or {}).items():
        if k in SKIP_KEYS or not isinstance(v, str):
            continue
        for name, sugg, snip in check_text(v):
            out.append((k, name, sugg, snip))
    return out
