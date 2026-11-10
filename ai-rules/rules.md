# AI Coding Rules

Rules an AI assistant must follow when working on this project. Keep this
short and enforceable — this is read at the start of every AI session.

## Always
- For any frontend (`*.ts` / `*.html` / `*.scss`) change, follow the Angular +
  PrimeNG standard in
  `coding-standards/frontend-angular-primeng.md` — it is mandatory for all
  frontend code.
- Access oilfield data through `ApiService` + `BOQuery` (PDM), not ad-hoc HTTP.
- Route feature backend calls through the MFE-resolved service name / module
  endpoint (see `MODULE_END_POINT`, `SERVICES_ROUTES`, `MfeInit`).
- Keep feature code inside its `libs/<feature>/` module; use lazy loading.
- Preserve the `language` + `timezone` fields injected by `ApiService.postApi`
  (oilfield data is timezone/locale sensitive).
- Use NgRx for cross-component feature state (filters, active page).

## Never
- Never call PDM endpoints directly bypassing the WAF rules service
  (`WafRulesWellSurvellianceService.byPassWAFRequestBody`).
- Never hardcode a host remote URL; MFE wiring comes from `reg_app.json` /
  webpack module-federation config.
- Never assume a unit — oilfield data mixes metric & imperial.

## Domain-specific gotchas
- Unit conversions: always state units explicitly (metric vs imperial) —
  see domain-knowledge/units-and-standards/. PDM BO attributes carry a
  `unitPolicy`; respect it.
- PDM responses signal success via `status.statusCode === 1`; any other value
  is an error and must be rejected/handled.
- BO query results are nested under `data.<boName>.list`.
