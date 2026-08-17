# Copyright (c) 2026, FEDCO
# License: MIT

app_name = "fedco_theme"
app_title = "FEDCO Theme"
app_publisher = "FEDCO"
app_description = "FEDCO brand theme for ERPNext v16: desk, login and portal"
app_email = "it@fedco.example"
app_license = "mit"
app_version = "1.0.1"

# Desk (the logged-in application)
app_include_css = "/assets/fedco_theme/css/fedco_theme.css"
app_include_js = "/assets/fedco_theme/js/fedco_theme.js"

# Website, login and portal pages
web_include_css = "/assets/fedco_theme/css/fedco_website.css"

after_install = "fedco_theme.install.after_install"
after_migrate = "fedco_theme.install.after_migrate"
