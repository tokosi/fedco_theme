# FEDCO Theme for ERPNext v16

Brand theme for ERPNext v16 / Frappe v16 covering the desk, the login page and
the employee portal.

## Palette

Sampled directly from the FEDCO mark, not approximated.

| Token | Hex | Contrast on white | Use |
|---|---|---|---|
| Terracotta | `#984A35` | 6.24:1 — AA | Brand. Buttons, links, active states |
| Deep | `#6B3222` | 9.98:1 — AAA | Sidebar panel, headings |
| Gold | `#F8C525` | **1.61:1 — fails** | Accent only. Never carries white text |
| Green | `#1D9644` | 3.82:1 — large only | Fills, icons, indicator dots |
| Green (text) | `#17803A` | 5.02:1 — AA | Any green that carries text |
| Ink | `#2A1A14` | 15.2:1 — AAA | Body text |

**The gold rule matters.** White text on gold is 1.61:1, which fails WCAG badly.
Gold appears only as a surface with ink text (`.btn-fedco-accent`), or as a thin
rule that carries no text. Anywhere green carries text it steps down to
`#17803A`.

## What it changes

- **Desk** — navbar, sidebar, buttons, forms, cards, list and report views,
  tabs, modals, dropdowns, indicators, scrollbars
- **Login** — split-screen layout with a curved brand panel echoing the circular
  FEDCO mark, collapsing to a single column under 992px
- **Portal** — employee self-service pages for claims, advances and payslips
- **Dark mode** — full support; the brand steps up the ramp to `#DDA08B`
  because terracotta is unreadable on a dark ground
- **Responsive** — 44px minimum touch targets, 16px inputs (stops iOS zooming
  on focus), reduced list columns on phones, horizontally scrollable reports
- **Accessibility** — visible focus rings throughout, `prefers-reduced-motion`
  honoured
- **Print** — chrome hidden, colours dropped to monochrome

## Install

```bash
cd ~/frappe-bench
bench get-app https://github.com/YOURUSER/fedco_theme.git
bench --site yoursite install-app fedco_theme
bench build --app fedco_theme
bench --site yoursite clear-cache
```

Then restart web and queue processes. Hard-refresh the browser (Ctrl-Shift-R) —
CSS bundles are cached aggressively.

## After install

The logo, favicon and splash are set automatically on Website Settings, but only
where those fields are blank — an administrator's own upload always wins. To
override manually: **Website Settings → Brand**.

To re-apply or remove:

```python
from fedco_theme.install import reapply_branding, reset_branding
reapply_branding()   # or reset_branding()
```

## Customising

Every colour is a CSS custom property in `public/css/fedco_theme.css`. To shift
the brand, change the `--fedco-*` ramp at the top; everything downstream
follows. Re-check contrast after any change — the ratios above are what make
the theme accessible, and they are easy to break by eye.

## Notes

- The theme rides on Frappe's CSS variables rather than overriding component
  internals, so it survives framework upgrades better than a fork would.
- `!important` is used only where a framework inline style must be beaten.
- The runtime JS is deliberately tiny: it only keeps the mobile browser chrome
  colour in step with light/dark. Anything achievable in CSS stays in CSS.

## License

MIT
