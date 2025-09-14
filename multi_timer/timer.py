"""
App: Base class for all textual app

"""
from time import monotonic

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header,Button, Digits
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive

"""
Container

Container Widget은 다른 위젯들을 포함하는 형태의 위젯이다.
일반적인 레이아웃 정의시에 주로 컨테이너를 사용한다.

Stopwatch widget이 HorizontalGroup을 상속하고 있는것도 눈여겨 봐야함.
"""


class TimeDisplay(Digits):
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self, event: events.Mount) -> None:
        self.update_timer = self.set_interval(1/60, self.update_time, pause=True)

    def update_time(self) -> None:
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        min, sec = divmod(time, 60)
        hr, min = divmod(min, 60)
        self.update(f"{hr:02,.0f}:{min:02.0f}:{sec:05.2f}")

    def start(self) -> None:
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        self.total = 0
        self.time = 0



class Stopwatch(HorizontalGroup):

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if event.button.id == "start":
            time_display.start()
            self.add_class("started")
        elif event.button.id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        """
        id: 위젯의 고유 ID의미
        variant: 기본 스타일을 선택할 수 있도록함.
        """
        yield Button("Start", id="start",variant="success")
        yield Button("Stop", id="stop",variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay()


class StopwatchApp(App):
    """
    Bindings

    bindings는 tuple list이며, app에서 사용할 수 있는 단축키 매핑들을 의미한다.

    첫번째: bind할 key
    두번째: action name
    세번째: action 설명

    Action Binding관련문서: https://textual.textualize.io/guide/input/#bindings

    CSS 관련 해석

    Textual은 CSS를 지원한다. 실제 웹 css와 거의 비슷하며, 일부 문법만 이에 맞게 개량되었다.
    '$' prefix로 되어있는것은, textual 내부에 정의되어있는 변수값들을 의미한다. 색상의 경우에는 직접 색상 명시와
    rgb함수를 통해 표기할 수 있다.

    Dynamic CSS

    동적 css설정도 가능하다. (e.g: 버튼이 어떤 상태일때 등)

    textual css에는 class도 존재하며, css파일의 .started로 시작하는 것은 .started class가 적용된 위젯에 대해서만 적용된다.
    class 이름 설정은 'add_class', 'remove_class' 두가지 메소드를 활용할 수 있다.
    - https://textual.textualize.io/api/dom_node/#textual.dom.DOMNode.add_class
    - https://textual.textualize.io/api/dom_node/#textual.dom.DOMNode.remove_class
    """
    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("d","toggle_dark", "Toogle dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch(), id="timers")

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_add_stopwatch(self) -> None:
        new_stopwatch = Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self) -> None:
        timers = self.query("Stopwatch")
        if len(timers) >= 1:
            timers.last().remove()

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()