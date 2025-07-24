import reflex as rx

config = rx.Config(
    app_name="shiatzen_web",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    prerender=False
)