// Copyright (c) 2026, FEDCO
// License: MIT

/**
 * Small runtime touches the stylesheet cannot express.
 * Deliberately minimal — anything achievable in CSS stays in CSS, because
 * JS that reshapes the desk breaks on every framework upgrade.
 */
frappe.provide("fedco.theme");

fedco.theme = {
	BRAND: "#984A35",

	init() {
		this.setThemeColor();
		this.watchColorScheme();
	},

	/** Colours the mobile browser chrome to match the navbar. */
	setThemeColor() {
		const dark = document.documentElement.getAttribute("data-theme") === "dark";
		const color = dark ? "#1D1512" : "#FFFFFF";

		let meta = document.querySelector('meta[name="theme-color"]');
		if (!meta) {
			meta = document.createElement("meta");
			meta.name = "theme-color";
			document.head.appendChild(meta);
		}
		meta.content = color;
	},

	/** Keeps the browser chrome in step when the user flips light/dark. */
	watchColorScheme() {
		const observer = new MutationObserver(() => this.setThemeColor());
		observer.observe(document.documentElement, {
			attributes: true,
			attributeFilter: ["data-theme"],
		});
	},
};

$(document).ready(() => {
	try {
		fedco.theme.init();
	} catch (e) {
		console.warn("FEDCO theme init skipped:", e);
	}
});
