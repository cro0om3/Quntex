# Lark Café — QX Executive Suite (Streamlit Demo)

Premium, AI-first demo for Lark Café owners/managers. All data is local JSON; AED-only; dark glass UI; QX-branded intelligence.

## Run
```bash
cd lark_demo
streamlit run app.py
```
Auth PIN: `2025` (set in pages/1_Login.py).

## Structure
- `app.py` — entry, CTA to Login/Dashboard.
- `pages/` — multipage app:
  - `1_Login.py` — PIN gate.
  - `2_Executive_Dashboard.py` — KPIs with sparklines, sales/hour with AI peak, category donut, top items bar, weekly trend, info grid, insights, AI strip, PDF snapshot.
  - `3_IntaAgent_AI.py` — QX Intelligence hub: smart alerts, profit drivers, fast/slow movers, demand prediction, heatmap, rotating feed.
  - `4_Inventory_Brain.py` — card grid with status bars, AI risk zone, waste/loss charts, smart reorder + supplier list, forecast, depletion timeline, AI commentary.
  - `5_Products_Cost.py` — margin-colored pricing table.
  - `6_Executive_Reports.py` — tabbed reports, AI snapshot, AI-insight table, mini visuals, commentary strip, PDF preview + download.
  - `7_QR_Menu_Demo.py` — QR ordering demo with cart + checkout.
  - `8_POS_Lite.py` — POS-lite flow with cart and receipt.
  - `9_Settings.py` — logo/name/tax/service charge, live preview, experience options (session-only).
- `demo_data/` — JSON seeds (sales, products, inventory, ai, reports).
- `utils/` — `theme.py` (dark/glass, mobile zoom), `loader.py` (JSON loader), `sidebar.py` (nav + accent picker).
- `assets/` — logo, icons, `qx/qx_icon.svg`.

## Data
All sourced from `demo_data/*.json`; no backend calls. Currency AED only.

## Branding
- AI brand: QX (Qx™). Footer: “Powered by Quantex — QX Active”.
- Sidebar accent picker (Blue/Gold); default collapsed.

## Mobile
Dark enforced. Viewport initial-scale ~0.47; mobile zoom 47%; sidebar hidden on small screens.

## PDFs / Downloads
- Dashboard: Executive Snapshot PDF.
- Reports: Executive Report PDF (enhanced button).
- Inventory: Supplier list (text/PDF-ready content).

## Notes
- Settings are session-only; not persisted.
- If not authed, pages redirect to Login.
