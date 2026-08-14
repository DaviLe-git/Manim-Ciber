from manim import *


class WebsiteRequest(Scene):
    def construct(self):

        browser = RoundedRectangle(
            width=3.5,
            height=2.5
        )

        browser_label = Text("Browser")
        browser_label.move_to(browser)

        browser_group = VGroup(browser, browser_label)
        browser_group.move_to(LEFT * 3)

        server = RoundedRectangle(
            width=3.5,
            height=2.5
        )

        server_label = Text("Web Server")
        server_label.move_to(server)

        server_group = VGroup(server, server_label)
        server_group.move_to(RIGHT * 3)

        arrow = Arrow(
            browser_group.get_right(),
            server_group.get_left()
        )

        request = Text("HTTP Request")
        request.next_to(arrow, UP)

        self.play(Create(browser))
        self.play(Write(browser_label))

        self.play(Create(server))
        self.play(Write(server_label))

        self.play(Create(arrow))
        self.play(Write(request))

        self.wait(2)
