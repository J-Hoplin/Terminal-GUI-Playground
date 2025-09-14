from textual.app import App, ComposeResult
from textual.widgets import LoadingIndicator, Static
from textual.timer import Timer


class LoadingApp(App):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield LoadingIndicator(id="loading")
        yield Static("Hello World!", id="hello", classes="hidden")

    def on_mount(self) -> None:
        # 3초 후에 로딩을 끝내고 Hello World를 표시
        self.set_timer(3.0, self.show_hello_world)

    def show_hello_world(self) -> None:
        # 로딩 인디케이터 숨기기
        loading = self.query_one("#loading", LoadingIndicator)
        loading.add_class("hidden")

        # Hello World 표시
        hello = self.query_one("#hello", Static)
        hello.remove_class("hidden")


if __name__ == "__main__":
    app = LoadingApp()
    app.run()