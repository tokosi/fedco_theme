# Copyright (c) 2026, FEDCO
# License: MIT

"""
Applies the FEDCO brand at the settings level.

The stylesheets handle appearance; this handles the things that live in the
database rather than in CSS — the navbar logo, favicon, splash and the Website
Theme record. All of it is idempotent, and none of it overwrites a value an
administrator has deliberately set.
"""

import os

import frappe

LOGO = "/assets/fedco_theme/images/fedco_logo.png"
FAVICON = "/assets/fedco_theme/images/fedco_favicon.png"
THEME_NAME = "FEDCO"

BRAND = {
	"primary": "#984A35",
	"gold": "#F8C525",
	"green": "#1D9644",
}


def after_install():
	setup()


def after_migrate():
	setup()


def setup():
	apply_navbar_branding()
	create_website_theme()
	frappe.db.commit()


def apply_navbar_branding():
	"""Logo, favicon and splash on Website Settings and Navbar Settings."""
	try:
		settings = frappe.get_single("Website Settings")
		changed = False

		for field, value in (
			("app_logo", LOGO),
			("banner_image", LOGO),
			("favicon", FAVICON),
			("splash_image", LOGO),
			("app_name", "FEDCO"),
		):
			if not settings.meta.has_field(field):
				continue
			# Only fill blanks: an administrator's own upload wins.
			if not settings.get(field):
				settings.set(field, value)
				changed = True

		if changed:
			settings.flags.ignore_permissions = True
			settings.flags.ignore_mandatory = True
			settings.save(ignore_permissions=True)
	except Exception:
		frappe.log_error(
			title="FEDCO Theme: navbar branding skipped", message=frappe.get_traceback()
		)


def create_website_theme():
	"""
	A Website Theme record so the brand also reaches server-rendered pages.

	Frappe compiles this to SCSS variables, which is the supported route for
	portal styling; the CSS bundle then refines what SCSS variables cannot
	express.
	"""
	try:
		if not frappe.db.exists("DocType", "Website Theme"):
			return

		if frappe.db.exists("Website Theme", THEME_NAME):
			doc = frappe.get_doc("Website Theme", THEME_NAME)
		else:
			doc = frappe.new_doc("Website Theme")
			doc.theme = THEME_NAME

		doc.custom = 1
		if doc.meta.has_field("primary_color"):
			doc.primary_color = BRAND["primary"]
		if doc.meta.has_field("text_color"):
			doc.text_color = "#2A1A14"
		if doc.meta.has_field("background_color"):
			doc.background_color = "#FFFFFF"
		if doc.meta.has_field("button_gradients"):
			doc.button_gradients = 0

		if doc.meta.has_field("custom_scss"):
			doc.custom_scss = (
				"$primary: {primary};\n"
				"$brand-primary: {primary};\n"
				"$link-color: #863F2C;\n"
				"$body-bg: #FFFFFF;\n"
				"$body-color: #2A1A14;\n"
				"$border-radius: 8px;\n"
			).format(primary=BRAND["primary"])

		doc.flags.ignore_permissions = True
		doc.save(ignore_permissions=True)

		# Publishing recompiles the SCSS and points the site at this theme.
		if hasattr(doc, "set_as_default"):
			doc.set_as_default()
	except Exception:
		frappe.log_error(
			title="FEDCO Theme: website theme skipped", message=frappe.get_traceback()
		)


@frappe.whitelist()
def reapply_branding():
	"""Re-run branding from the console or a client script."""
	setup()
	return "FEDCO branding applied."


@frappe.whitelist()
def reset_branding():
	"""Clear the logo fields so stock Frappe branding returns."""
	settings = frappe.get_single("Website Settings")
	for field in ("app_logo", "banner_image", "favicon", "splash_image"):
		if settings.meta.has_field(field) and settings.get(field, "").startswith("/assets/fedco_theme"):
			settings.set(field, None)
	settings.flags.ignore_permissions = True
	settings.save(ignore_permissions=True)
	frappe.db.commit()
	return "FEDCO branding removed."
