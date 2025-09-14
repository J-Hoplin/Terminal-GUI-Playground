# textual>=0.40 기준
import asyncio
from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Button, Label, LoadingIndicator, Static
from textual.containers import Center, Vertical


class LoadingOverlay(ModalScreen[None]):
    """로딩 스피너를 보여주는 모달 화면"""
    def compose(self) -> ComposeResult:
        yield Center(
            Vertical(
                LoadingIndicator(),
                Label("불러오는 중입니다..."),
                classes="p-2"
            )
        )


class ResultScreen(Screen):
    """API 결과를 보여주는 다음 페이지"""
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        yield Static(f"API 결과: {self.data}", classes="p-2")
        yield Button("뒤로 가기", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()  # 현재 화면 닫기


class HomeScreen(Screen):
    """첫 화면: 호출 버튼만 있음"""
    def compose(self) -> ComposeResult:
        yield Button("API 호출하기", id="call_api")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "call_api":
            # 직접 앱의 비동기 메서드 호출
            asyncio.create_task(self.app.start_api_flow())


class MyApp(App):
    CSS = """
    .p-2 { padding: 1; }
    """

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
    ]


    def on_mount(self) -> None:
        self.push_screen(HomeScreen())

    async def api_call(self) -> dict:
        await asyncio.sleep(2)
        return {"status": "ok", "items": [1, 2, 3]}

    async def start_api_flow(self) -> None:
        self.push_screen(LoadingOverlay())

        try:
            data = await self.api_call()
            self.pop_screen()  # 로딩 화면 닫기
            self.push_screen(ResultScreen(data))  # 결과 화면 열기
        except Exception as e:
            # 에러 처리
            self.pop_screen()  # 로딩 화면 닫기
            self.push_screen(ResultScreen({"error": str(e)}))



if __name__ == "__main__":
    MyApp().run()