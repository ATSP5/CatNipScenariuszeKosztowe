# CatNip Interactive Report — generated from the block's page (markup, Python, style).
# Edit it in the block's editor: this file is rewritten whenever the editor is saved.
import base64 as _ir_base64
import html as _ir_html
import io as _ir_io
import json as _ir_json_module
import math as _ir_math
import os as _ir_os
import sys as _ir_sys
import threading as _ir_threading
import traceback as _ir_traceback
import uuid as _ir_uuid


class ScenariuszeKosztowe:
    TITLE = 'Co jeśli zdrożeją surowce?'
    HEIGHT = 1700
    KEEP_ALIVE = True
    ACTIONS = {}
    CATNIP_LIVE_ACTIONS = ()
    MARKUP = (
        '<div class="cn-page">\n'
        '  <h1>Co się stanie, jeśli zdrożeją surowce?</h1>\n'
        '  <p class="cn-muted">{source_note} · BOM (CSV) + produkty (Excel) + ceny surowców i koszty stałe (JSON) → Data Scan → model kosztowy → scenariusze</p>\n'
        '\n'
        '  <div class="cn-card">\n'
        '    <div class="cn-row">\n'
        '      {select("resource", resource_options, label="Surowiec")}\n'
        '      {slider("shock", -20, 60, step=1, label="Zmiana ceny surowca %")}\n'
        '      {slider("pass_through", 0, 100, step=5, label="Przerzucenie na ceny %")}\n'
        '      {slider("volume", -30, 20, step=1, label="Zmiana wolumenu %")}\n'
        '    </div>\n'
        '  </div>\n'
        '\n'
        '  <div class="cn-grid-4">\n'
        '    {self._kpi("EBITDA — " + r.scenario.name, f.short_zl(r.ebitda), f.short_zl(r.ebitda - base.ebitda) + " vs BASE", r.ebitda - base.ebitda)}\n'
        '    {self._kpi("Marża EBITDA", f.pct(r.ebitda_margin), f.pp(r.ebitda_margin - base.ebitda_margin), r.ebitda_margin - base.ebitda_margin)}\n'
        '    {self._kpi("Próg rentowności (przychód)", f.short_zl(r.break_even_revenue), f.short_zl(r.break_even_revenue - base.break_even_revenue), r.break_even_revenue - base.break_even_revenue, good_up=False)}\n'
        '    {self._kpi("Produkty zagrożone", str(risk_count) + " z " + str(len(r.products)), "marża pokrycia < 5%" if risk_count else "brak", -risk_count)}\n'
        '  </div>\n'
        '\n'
        '  <div class="cn-grid-2">\n'
        '    <div class="cn-card answer">\n'
        '      <h3>Odpowiedź</h3>\n'
        '      {findings_html}\n'
        '    </div>\n'
        '    <div class="cn-card">\n'
        '      <h3>Drabina scenariuszy: {resource_name}</h3>\n'
        '      {ladder_chart}\n'
        '    </div>\n'
        '  </div>\n'
        '\n'
        '  <div class="cn-grid-2">\n'
        '    <div class="cn-card"><h3>Który surowiec boli najbardziej? (+10% ceny)</h3>{tornado_chart}</div>\n'
        '    <div class="cn-card"><h3>Marża pokrycia produktów: przed i po</h3>{margin_chart}</div>\n'
        '  </div>\n'
        '\n'
        '  <div class="cn-card">\n'
        '    <h3>Produkty w scenariuszu — od najsłabszej marży</h3>\n'
        '    {table(product_rows, page_size=10, id="products")}\n'
        '  </div>\n'
        '\n'
        '  <div class="cn-grid-2">\n'
        '    <div class="cn-card"><h3>Struktura kosztów (BASE, rocznie)</h3>{structure_chart}</div>\n'
        '    <div class="cn-card">\n'
        '      <h3>Data Scan — co CatNip rozpoznał w danych</h3>\n'
        '      <pre class="scan">{scan_tree}</pre>\n'
        '      <p><b>Powiązania wykryte automatycznie</b></p>\n'
        '      {relations_html}\n'
        '      {table(pipeline_rows, filter=False, sortable=False, id="pipeline")}\n'
        '    </div>\n'
        '  </div>\n'
        '</div>\n'
        ''
    )
    STYLE = (
        '.cn-page h1 { margin-bottom: 2px; }\n'
        '.cn-card h3 { margin-top: 0; }\n'
        '.answer .headline { font-size: 1.15em; font-weight: 600; }\n'
        '.answer ol, .answer ul { margin-top: 4px; padding-left: 22px; }\n'
        '.answer li { margin: 3px 0; }\n'
        'pre.scan { font-size: 0.82em; line-height: 1.35; max-height: 420px; overflow: auto; background: rgba(127,127,127,0.08); padding: 10px; border-radius: 6px; }\n'
        '.cn-kpi-value { font-size: 1.35em; }\n'
        '.flag { display: inline-block; padding: 1px 6px; margin: 1px; border-radius: 4px; font-size: 0.85em; background: rgba(220,57,18,0.12); }\n'
        ''
    )

    def __init__(self, engine=None, advisor=None, formatter=None):
        self.engine = engine
        self.advisor = advisor
        self.formatter = formatter
        self.data = engine
        _ir_init(self, {'engine': engine, 'advisor': advisor, 'formatter': formatter})

    def show(self):
        """Shows the page in the Run Engine's Output tab, or updates it when it is already there."""
        return _ir_show(self)

    def set(self, name, value, refresh=False):
        """Sets a state value; the markup sees it by name. refresh=True renders the page again."""
        self.state[name] = value
        if refresh:
            self.refresh()

    def get(self, name, default=None):
        """A state value — what a control bound to that name holds."""
        return self.state.get(name, default)

    def values(self):
        """A copy of the page's state."""
        return dict(self.state)

    def refresh(self):
        """Renders the page again and sends it to the Run Engine."""
        if self._ir['shown'] and not self._ir['closed']:
            _ir_push(self)

    def toast(self, message, kind='info'):
        """A short message over the page; kind is info, success, warning or error."""
        if self._ir['shown'] and not self._ir['closed'] and _ir_engine():
            _ir_send({'op': 'toast', 'id': self._ir['id'], 'message': str(message), 'kind': kind})
        else:
            print('[%s] %s' % (kind, message), flush=True)

    def close(self):
        """Closes the page; once every page is closed the run may end."""
        _ir_close(self)

    def bind_action(self, name, handler):
        """Calls handler(values) on every click of the action's button — what the generated main does with a live action."""
        _ir_bind(self, name, handler)

    # ── The Python tab ─────────────────────────────────────────────────────

    def setup(self):
        ids = [rid for rid, _ in self.engine.resource_options()]
        self.set("resource", "R-AL" if "R-AL" in ids else ids[0])
        self.set("shock", 15)
        self.set("pass_through", 0)
        self.set("volume", 0)

    def prepare(self):
        e = self.engine
        f = self.formatter
        resource = self.get("resource")
        shock = float(self.get("shock"))
        pass_through = float(self.get("pass_through"))
        volume = float(self.get("volume"))
        base = e.base()
        result = e.shock(resource, shock, pass_through, volume)
        ladder = e.ladder(resource, pass_through, volume, shocks=sorted({0.0, 10.0, 15.0, 25.0, shock}))
        scan = e.model.scan
        return {
            "f": f,
            "base": base,
            "r": result,
            "resource_name": e.resource_names[resource],
            "resource_options": e.resource_options(),
            "findings_html": html("<ul>%s</ul>" % "".join("<li>%s</li>" % esc(line) for line in self.advisor.findings(e, base, result, resource))),
            "ladder_chart": self._ladder_chart(ladder, resource, shock),
            "tornado_chart": self._tornado_chart(e.sensitivity(10.0)),
            "margin_chart": self._margin_chart(result),
            "structure_chart": chart("donut", [{"Pozycja": k, "zł": round(v)} for k, v in e.cost_structure().items()], labels="Pozycja", values="zł", height=320),
            "product_rows": self._product_rows(result),
            "risk_count": len(result.at_risk()),
            "scan_tree": scan.tree_text(),
            "relations_html": html("<ul>%s</ul>" % "".join("<li>%s</li>" % esc(r) for r in scan.relations())),
            "pipeline_rows": scan.pipeline_rows(),
            "source_note": "dane demonstracyjne wygenerowane przed chwilą w input/" if e.model.demo else "dane z folderu input/",
        }

    def _ladder_chart(self, ladder, resource, chosen):
        f = self.formatter
        shocks = [r.scenario.shocks.get(resource, 0.0) for r in ladder]
        names = ["BASE" if not s else "%+g%%" % s for s in shocks]
        colors = ["#3366cc" if not s else ("#c0392b" if s == chosen else "#f0ad4e") for s in shocks]
        trace = {"type": "bar", "x": names, "y": [round(r.ebitda) for r in ladder], "marker": {"color": colors},
                 "text": [f.short_zl(r.ebitda) + "<br>" + f.pct(r.ebitda_margin) for r in ladder], "textposition": "outside"}
        layout = {"height": 330, "margin": {"l": 60, "r": 20, "t": 30, "b": 40}, "yaxis": {"title": {"text": "EBITDA [zł]"}},
                  "paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "rgba(0,0,0,0)", "showlegend": False}
        return plotly({"data": [trace], "layout": layout}, height=330)

    def _tornado_chart(self, impact):
        f = self.formatter
        names = list(impact)[::-1]
        values = [round(impact[n]) for n in names]
        trace = {"type": "bar", "orientation": "h", "y": names, "x": values, "marker": {"color": "#d9534f"},
                 "text": [f.short_zl(v) for v in values], "textposition": "auto"}
        layout = {"height": 330, "margin": {"l": 160, "r": 20, "t": 30, "b": 40}, "xaxis": {"title": {"text": "zmiana EBITDA przy +10% ceny"}},
                  "paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "rgba(0,0,0,0)", "showlegend": False}
        return plotly({"data": [trace], "layout": layout}, height=330)

    def _margin_chart(self, result):
        rows = [{"Produkt": p.name.split(" (")[0], "Przed": round(p.base_margin_pct, 1), "Po": round(p.margin_pct, 1)} for p in result.products]
        return chart("bar", rows, x="Produkt", y=["Przed", "Po"], height=330, y_title="marża pokrycia %", colors=["#3366cc", "#d9534f"])

    def _product_rows(self, result):
        return [{"Produkt": p.name, "Cena": round(p.price, 2), "Koszt jedn. przed": round(p.base_unit_cost, 2),
                 "Koszt jedn. po": round(p.unit_cost, 2), "Marża przed %": round(p.base_margin_pct, 1),
                 "Marża po %": round(p.margin_pct, 1), "Potrzebna podwyżka %": round(p.required_price_increase_pct, 1),
                 "Wolumen": round(p.volume), "Status": p.status} for p in sorted(result.products, key=lambda p: p.margin_pct)]

    def _kpi(self, label, value, delta=None, change=0.0, good_up=True):
        """Kafelek KPI: strzałka i kolor biorą się z liczby change, a opis zmiany (delta) jest już po polsku."""
        extra = ""
        if delta is not None:
            tone = "cn-good" if (change >= 0) == good_up else "cn-bad"
            arrow = "▲" if change > 0 else ("▼" if change < 0 else "•")
            extra = '<div class="cn-kpi-delta %s">%s %s</div>' % (tone, arrow, esc(delta))
        return html('<div class="cn-kpi"><div class="cn-kpi-label">%s</div><div class="cn-kpi-value">%s</div>%s</div>'
                    % (esc(label), esc(value), extra))


# ── CatNip interactive report runtime ─────────────────────────────────────────
# Generated with the class above; everything here is shared by every interactive report of a
# process through one hub, so two reports on one page of output never fight over stdin.
#
# The page lives in CatNip's Run Engine. It reaches this process as lines on stdin
# (__CATNIP_UI__ {json}) and this process answers through the ordinary visual stream
# (__VISUAL_START__ {"type": "interactive", ...} __VISUAL_END__) — the two channels every kind of
# run already has, locally, in Docker, in a compiled executable and on the CatNip Server.

_IR_PREFIX = '__CATNIP_UI__'
_IR_LOCAL = _ir_threading.local()


class Html(str):
    """Text that goes into the page as HTML instead of being escaped."""
    __slots__ = ()

    def __html__(self):
        return str(self)


def html(text):
    """Marks text as HTML, to be inserted as it is."""
    return Html('' if text is None else text)


def esc(value):
    """Escapes a value for the page."""
    return _ir_html.escape('' if value is None else str(value), quote=True)


def fmt(value, spec=None):
    """Formats a value with a format spec (',.2f', '.1%', ...); None reads as empty."""
    if value is None:
        return ''
    if not spec:
        return str(value)
    try:
        return format(value, spec)
    except (TypeError, ValueError):
        return str(value)


# ── The hub: one per process ──────────────────────────────────────────────────

def _ir_hub():
    hub = getattr(_ir_sys, '_catnip_interactive_hub', None)
    if hub is None:
        hub = {
            'pages': {},
            'lock': _ir_threading.RLock(),
            'out': _ir_threading.Lock(),
            'reader': None,
            'keeper': None,
            'closed': _ir_threading.Event(),
            'eof': False,
        }
        setattr(_ir_sys, '_catnip_interactive_hub', hub)
    return hub


def _ir_engine():
    """True when a CatNip engine is listening on the other end of stdout and stdin."""
    env = _ir_os.environ
    return bool(env.get('CATNIP_MAIN_PY') or env.get('CATNIP_SCRIPT')
                or env.get('CATNIP_ENGINE') or env.get('CATNIP_INTERACTIVE'))


def _ir_plain(value):
    """A value JSON can carry: numpy scalars, dates, decimals and the like are reduced to one."""
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return value if _ir_math.isfinite(value) else None
    if isinstance(value, (list, tuple)):
        return [_ir_plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _ir_plain(v) for k, v in value.items()}
    if hasattr(value, 'item') and not hasattr(value, '__len__'):
        try:
            return _ir_plain(value.item())
        except Exception:
            pass
    if hasattr(value, 'tolist'):
        try:
            return _ir_plain(value.tolist())
        except Exception:
            pass
    if hasattr(value, 'isoformat'):
        try:
            return value.isoformat()
        except Exception:
            pass
    try:
        import decimal
        if isinstance(value, decimal.Decimal):
            return float(value)
    except Exception:
        pass
    return str(value)


def _ir_json(value):
    return _ir_json_module.dumps(_ir_plain(value), separators=(',', ':'), ensure_ascii=False)


def _ir_send(message):
    body = _ir_json(message).encode('utf-8')
    payload = _ir_json_module.dumps({
        'type': 'interactive',
        'title': message.get('title', ''),
        'data': _ir_base64.b64encode(body).decode('ascii'),
    })
    with _ir_hub()['out']:
        _ir_sys.stdout.write('__VISUAL_START__' + payload + '__VISUAL_END__\n')
        _ir_sys.stdout.flush()


def _ir_register(page, keep_alive):
    hub = _ir_hub()
    with hub['lock']:
        hub['pages'][page._ir['id']] = page
        if hub['eof']:
            return
        if hub['reader'] is None:
            hub['reader'] = _ir_threading.Thread(target=_ir_read_loop, name='catnip-interactive', daemon=True)
            hub['reader'].start()
        # The keeper is what keeps the process alive after the flow finished: the reader is a
        # daemon thread and would die with the main one.
        if keep_alive and hub['keeper'] is None:
            hub['keeper'] = _ir_threading.Thread(target=hub['closed'].wait, name='catnip-interactive-keeper')
            hub['keeper'].start()


def _ir_unregister(page_id):
    hub = _ir_hub()
    with hub['lock']:
        hub['pages'].pop(page_id, None)
        if not hub['pages']:
            hub['closed'].set()


def _ir_read_loop():
    hub = _ir_hub()
    stream = _ir_sys.stdin
    while True:
        try:
            line = stream.readline() if stream is not None else ''
        except Exception:
            line = ''
        if not line:
            # Nobody will ever answer again (the run was stopped, or nothing was attached):
            # whoever is waiting for a click must be let go, and the process may end.
            with hub['lock']:
                hub['eof'] = True
                pages = list(hub['pages'].values())
            for page in pages:
                _ir_release_waiters(page)
            hub['closed'].set()
            return
        line = line.strip()
        if not line.startswith(_IR_PREFIX):
            continue
        try:
            message = _ir_json_module.loads(line[len(_IR_PREFIX):])
        except ValueError:
            continue
        with hub['lock']:
            page = hub['pages'].get(message.get('page'))
        if page is None:
            continue
        try:
            _ir_dispatch(page, message)
        except Exception:
            _ir_traceback.print_exc()


# ── A page ────────────────────────────────────────────────────────────────────

def _ir_init(page, inputs):
    page.state = {}
    page._ir = {
        'id': _ir_uuid.uuid4().hex,
        'shown': False,
        'closed': False,
        'bindings': {},
        'waiters': {},
        'pending': {},
        'controls': {},
        'counter': 0,
        'inputs': inputs,
        'lock': _ir_threading.RLock(),
    }
    setup = getattr(page, 'setup', None)
    if callable(setup):
        setup()


def _ir_show(page):
    ir = page._ir
    if ir['closed']:
        return None
    if not _ir_engine():
        print('[CatNip] %s: an interactive report is shown by the CatNip Run Engine; '
              'outside it there is no page to show.' % type(page).TITLE, flush=True)
        return None
    if _ir_sys.gettrace() is not None:
        # A debugger reads stdin too, and the page would steal its commands.
        print('[CatNip] %s: the page stays static while debugging.' % type(page).TITLE, flush=True)
        ir['shown'] = True
        _ir_push(page, interactive=False)
        return None
    ir['shown'] = True
    _ir_register(page, type(page).KEEP_ALIVE)
    _ir_push(page)
    return None


def _ir_push(page, interactive=True):
    """Renders the page and sends it; the Run Engine replaces the card with the same id."""
    cls = type(page)
    try:
        body = _ir_render(page)
    except Exception as ex:
        _ir_traceback.print_exc()
        body = '<div class="cn-error-page"><b>The page could not be rendered.</b><pre>%s</pre></div>' % esc(
            '%s: %s' % (type(ex).__name__, ex))
    _ir_send({
        'op': 'render',
        'id': page._ir['id'],
        'title': cls.TITLE,
        'height': cls.HEIGHT,
        'css': cls.STYLE,
        'html': body,
        'interactive': interactive,
        'actions': dict(cls.ACTIONS),
    })


def _ir_namespace(page):
    namespace = dict(globals())
    prepare = getattr(page, 'prepare', None)
    extra = prepare() if callable(prepare) else None
    namespace.update(page.state)
    for name, value in page._ir['inputs'].items():
        namespace[name] = getattr(page, name, value)
    namespace.update({'self': page, 'state': page.state, 'data': page.data, 'title': type(page).TITLE})
    if isinstance(extra, dict):
        namespace.update(extra)
    return namespace


def _ir_render(page):
    with page._ir['lock']:
        page._ir['counter'] = 0
        page._ir['controls'] = {}
        previous = (getattr(_IR_LOCAL, 'page', None), getattr(_IR_LOCAL, 'namespace', None))
        _IR_LOCAL.page = page
        _IR_LOCAL.namespace = None
        try:
            namespace = _ir_namespace(page)
            # A control placed further up gives its state value a default as it renders; the holes
            # below it must see that value, so the namespace is shared with _ir_default.
            _IR_LOCAL.namespace = namespace
            return _ir_template(type(page).MARKUP, namespace)
        finally:
            _IR_LOCAL.page, _IR_LOCAL.namespace = previous


def _ir_current():
    page = getattr(_IR_LOCAL, 'page', None)
    if page is None:
        raise RuntimeError('controls, charts and tables are placed from the markup, while the page renders')
    return page


def _ir_next_id(prefix):
    page = getattr(_IR_LOCAL, 'page', None)
    if page is None:
        return 'cn-%s-%s' % (prefix, _ir_uuid.uuid4().hex[:8])
    page._ir['counter'] += 1
    return 'cn-%s-%d' % (prefix, page._ir['counter'])


def _ir_dispatch(page, message):
    op = message.get('op')
    if op == 'ready':
        _ir_push(page)
        return
    if op == 'close':
        _ir_close(page, notify=False)
        return
    if op == 'change':
        name = str(message.get('name') or '')
        if not name:
            return
        value = message.get('value')
        page.state[name] = value
        hook = getattr(page, 'on_%s_change' % name, None)
        if callable(hook):
            _ir_guard(page, hook, value)
        else:
            hook = getattr(page, 'on_change', None)
            if callable(hook):
                _ir_guard(page, hook, name, value)
        _ir_push(page)
        return
    if op == 'call':
        name = str(message.get('name') or '')
        method = getattr(page, name, None) if name and not name.startswith('_') else None
        if callable(method):
            _ir_guard(page, method)
        else:
            page.toast('The page has no method called %s.' % name, 'error')
        _ir_push(page)
        return
    if op == 'action':
        _ir_fire(page, str(message.get('name') or ''))


def _ir_guard(page, func, *args):
    try:
        return func(*args)
    except Exception as ex:
        _ir_traceback.print_exc()
        page.toast('%s: %s' % (type(ex).__name__, ex), 'error')
        return None


def _ir_payload(page, name):
    values = dict(page.state)
    hook = getattr(page, 'on_' + name, None)
    if callable(hook):
        result = hook(values)
        if result is not None:
            return result
    return values


def _ir_fire(page, name):
    ir = page._ir
    if name not in type(page).ACTIONS:
        page.toast('The page has no action called %s.' % name, 'error')
        return
    with ir['lock']:
        waiter = ir['waiters'].pop(name, None)
        binding = ir['bindings'].get(name)
    try:
        payload = _ir_payload(page, name)
    except Exception as ex:
        _ir_traceback.print_exc()
        page.toast('%s: %s' % (type(ex).__name__, ex), 'error')
        return
    if waiter is not None:
        waiter['payload'] = payload
        waiter['event'].set()
        return
    if (binding is None and type(page).ACTIONS.get(name) == 'live'
            and _ir_threading.main_thread().is_alive()
            and _ir_os.environ.get('CATNIP_INTERACTIVE') != 'preview'):
        # The generated main binds live actions after the rest of the flow has been called, and
        # the flow may still be on its way there (waiting at a submit, say): the click is kept
        # and handled the moment the binding arrives.
        with ir['lock']:
            ir['pending'][name] = payload
        page.toast('"%s" runs as soon as the flow reaches it.' % name, 'info')
        return
    if binding is None:
        if _ir_os.environ.get('CATNIP_INTERACTIVE') == 'preview':
            page.toast('%s would hand over: %s' % (name, _ir_json(payload)[:400]), 'info')
        else:
            page.toast('Nothing is waiting for "%s" — connect a block to its output and run the generated main.' % name, 'warning')
        return
    _ir_run_binding(page, name, binding, payload)


def _ir_run_binding(page, name, binding, payload):
    ir = page._ir
    _ir_send({'op': 'busy', 'id': ir['id'], 'on': True, 'label': name})
    try:
        _ir_guard(page, binding, payload)
    finally:
        _ir_send({'op': 'busy', 'id': ir['id'], 'on': False})
        _ir_push(page)


def _ir_bind(page, name, handler):
    ir = page._ir
    with ir['lock']:
        ir['bindings'][name] = handler
        pending = ir['pending'].pop(name, None)
    if pending is not None:
        _ir_run_binding(page, name, handler, pending)


def _ir_wait(page, name):
    """The output of a submit action: shows the page if it is not shown, then waits for the click."""
    ir = page._ir
    if not ir['shown']:
        page.show()
    hub = _ir_hub()
    if ir['closed'] or not _ir_engine() or hub['eof'] or _ir_sys.gettrace() is not None:
        # Nobody can click: carry on with what the page holds.
        return _ir_payload(page, name)
    waiter = {'event': _ir_threading.Event(), 'payload': None}
    with ir['lock']:
        ir['waiters'][name] = waiter
    _ir_send({'op': 'waiting', 'id': ir['id'], 'action': name})
    waiter['event'].wait()
    _ir_send({'op': 'waiting', 'id': ir['id'], 'action': None})
    return waiter['payload']


def _ir_release_waiters(page):
    with page._ir['lock']:
        waiters = list(page._ir['waiters'].values())
        page._ir['waiters'].clear()
    for waiter in waiters:
        waiter['event'].set()


def _ir_close(page, notify=True):
    ir = page._ir
    if ir['closed']:
        return
    ir['closed'] = True
    _ir_release_waiters(page)
    if notify and ir['shown']:
        _ir_send({'op': 'close', 'id': ir['id']})
    _ir_unregister(ir['id'])


# ── The template: HTML with {python} holes ───────────────────────────────────

_IR_COMPILED = {}


def _ir_template(text, namespace):
    out = []
    i = 0
    n = len(text)
    lower = text.lower()
    while i < n:
        c = text[i]
        if c == '<' and (lower.startswith('<script', i) or lower.startswith('<style', i)):
            # Script and style blocks are copied as they are: their braces are not holes.
            tag = 'script' if lower.startswith('<script', i) else 'style'
            end = lower.find('</' + tag, i)
            end = n if end < 0 else lower.find('>', end) + 1 or n
            out.append(text[i:end])
            i = end
            continue
        if c == '{':
            if text.startswith('{{', i):
                out.append('{')
                i += 2
                continue
            close = _ir_matching(text, i)
            if close < 0:
                out.append(text[i:])
                break
            out.append(_ir_hole(text[i + 1:close], namespace))
            i = close + 1
            continue
        if c == '}':
            out.append('}')
            i += 2 if text.startswith('}}', i) else 1
            continue
        nxt = min([p for p in (text.find('{', i), text.find('}', i), lower.find('<s', i)) if p >= 0] or [n])
        if nxt == i:
            nxt = i + 1
        out.append(text[i:nxt])
        i = nxt
    return ''.join(out)


def _ir_matching(text, start):
    """The brace closing the one at start, skipping braces inside strings and nested brackets."""
    depth = 0
    quote = None
    i = start
    while i < len(text):
        c = text[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if text.startswith(quote, i):
                i += len(quote)
                quote = None
                continue
        elif c in '\'"':
            quote = c * 3 if text.startswith(c * 3, i) else c
            i += len(quote)
            continue
        elif c in '{[(':
            depth += 1
        elif c in '}])':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _ir_hole(expression, namespace):
    raw = expression.startswith('!')
    source = expression[1:] if raw else expression
    source = source.strip()
    if not source:
        return ''
    try:
        code = _IR_COMPILED.get(source)
        if code is None:
            code = compile(source, '<markup {%s}>' % source[:60], 'eval')
            _IR_COMPILED[source] = code
        value = eval(code, namespace)
    except Exception as ex:
        return '<span class="cn-error" title="%s">{%s} → %s: %s</span>' % (
            esc(source), esc(source[:80]), esc(type(ex).__name__), esc(ex))
    return _ir_value(value, raw)


def _ir_value(value, raw=False):
    if value is None:
        return ''
    if hasattr(value, '__html__'):
        return str(value.__html__())
    if raw:
        return str(value)
    if hasattr(value, 'to_plotly_json'):
        return plotly(value)
    if hasattr(value, 'savefig'):
        return figure(value)
    if hasattr(value, 'columns') and hasattr(value, 'itertuples'):
        return table(value)
    if isinstance(value, float):
        return esc(_ir_number(value))
    return esc(value)


def _ir_number(value):
    if value != value:
        return ''
    if float(value).is_integer() and abs(value) < 1e15:
        return str(int(value))
    return ('%.6g' % value) if abs(value) < 1e-4 or abs(value) >= 1e15 else str(round(value, 6))


# ── Data shapes ───────────────────────────────────────────────────────────────

def _ir_table(rows, columns=None, limit=0):
    """(headers, rows of values) out of a DataFrame, numpy array, dict of columns, list of dicts
    or list of rows — resolved when the page renders, so the data may change shape between runs."""
    if rows is None:
        return [], []
    limit = int(limit or 0)
    if hasattr(rows, 'columns') and hasattr(rows, 'itertuples'):
        frame = rows[list(columns)] if columns else rows
        if limit > 0:
            frame = frame.head(limit)
        return [str(c) for c in frame.columns], [list(r) for r in frame.itertuples(index=False, name=None)]
    if hasattr(rows, 'column_names') and hasattr(rows, 'to_pylist'):          # pyarrow Table
        return _ir_table(rows.to_pylist(), columns, limit)
    if hasattr(rows, 'tolist') and not isinstance(rows, (list, tuple, dict)):
        rows = rows.tolist()
    if isinstance(rows, dict):
        headers = [str(k) for k in (columns or rows.keys())]
        cols = [rows.get(h, []) for h in headers]
        cols = [c.tolist() if hasattr(c, 'tolist') else list(c) if hasattr(c, '__iter__') and not isinstance(c, str) else [c] for c in cols]
        length = max((len(c) for c in cols), default=0)
        if limit > 0:
            length = min(length, limit)
        return headers, [[c[i] if i < len(c) else None for c in cols] for i in range(length)]
    rows = list(rows)
    if not rows:
        return [str(c) for c in (columns or [])], []
    if limit > 0:
        rows = rows[:limit]
    if isinstance(rows[0], dict):
        headers = [str(k) for k in (columns or rows[0].keys())]
        return headers, [[row.get(h) for h in headers] for row in rows]
    if hasattr(rows[0], '_fields'):                                            # namedtuple
        headers = list(columns or rows[0]._fields)
        return headers, [[getattr(row, h, None) for h in headers] for row in rows]
    cells = [list(row) if hasattr(row, '__iter__') and not isinstance(row, str) else [row] for row in rows]
    width = max(len(r) for r in cells)
    headers = [str(c) for c in columns] if columns else ['Column %d' % (i + 1) for i in range(width)]
    return headers, cells


def rows_of(data, columns=None):
    """Any tabular shape as a list of dicts — the easiest form to compute with in a report."""
    if data is None:
        return []
    headers, cells = _ir_table(data, columns)
    return [dict(zip(headers, row)) for row in cells]


def column(data, key):
    """One column of any tabular shape as a list; a sequence passed as the key comes back as a list."""
    if key is None:
        return None
    if not isinstance(key, str):
        return key.tolist() if hasattr(key, 'tolist') else list(key)
    if data is None:
        raise KeyError('no data to take the column %r from' % key)
    if hasattr(data, 'columns') and hasattr(data, 'itertuples'):
        return data[key].tolist()
    if isinstance(data, dict):
        values = data[key]
        return values.tolist() if hasattr(values, 'tolist') else list(values)
    headers, cells = _ir_table(data)
    if key not in headers:
        raise KeyError('no column %r — the data has %s' % (key, ', '.join(headers) or 'no columns'))
    index = headers.index(key)
    return [row[index] if index < len(row) else None for row in cells]


def _ir_data(data):
    if data is None:
        page = getattr(_IR_LOCAL, 'page', None)
        return page.data if page is not None else None
    return data


def _ir_attrs(**attributes):
    parts = []
    for key, value in attributes.items():
        if value is None or value is False:
            continue
        key = key.rstrip('_').replace('_', '-')
        parts.append(key if value is True else '%s="%s"' % (key, esc(value)))
    return ' '.join(parts)


def _ir_json_block(value):
    return _ir_json(value).replace('</', '<\\/')


def _ir_label(label, for_id, body, css='cn-field'):
    caption = '<label class="cn-label" for="%s">%s</label>' % (for_id, esc(label)) if label else ''
    return Html('<div class="%s">%s%s</div>' % (css, caption, body))


def _ir_default(name, value):
    page = _ir_current()
    if name not in page.state:
        page.state[name] = value
        namespace = getattr(_IR_LOCAL, 'namespace', None)
        if namespace is not None:
            namespace.setdefault(name, value)
    page._ir['controls'][name] = True
    return page.state[name]


# ── Controls: each one is bound to the state value of its name ───────────────

def slider(name, min=0, max=100, step=1, value=None, label=None, live=False, format=None):
    """A slider; the state value changes when it is released, or while dragging with live=True."""
    current = _ir_default(name, min if value is None else value)
    control_id = 'cn-' + name
    shown = fmt(current, format)
    body = ('<div class="cn-slider-row"><input type="range" %s/><output class="cn-slider-value" data-cn-format="%s">%s</output></div>'
            % (_ir_attrs(id=control_id, class_='cn-slider', min=min, max=max, step=step, value=current,
                         data_cn_bind=name, data_cn_type='number', data_cn_live='1' if live else None),
               esc(format or ''), esc(shown)))
    return _ir_label(label, control_id, body)


def number(name, value=None, min=None, max=None, step=None, label=None, integer=False):
    """A number box."""
    current = _ir_default(name, 0 if value is None else value)
    control_id = 'cn-' + name
    body = '<input type="number" %s/>' % _ir_attrs(
        id=control_id, class_='cn-input', value=current, min=min, max=max, step=step if step is not None else (1 if integer else 'any'),
        data_cn_bind=name, data_cn_type='int' if integer else 'number')
    return _ir_label(label, control_id, body)


def text_input(name, value='', label=None, placeholder=None):
    """A one-line text box; the state value changes when it loses focus or Enter is pressed."""
    current = _ir_default(name, value)
    control_id = 'cn-' + name
    body = '<input type="text" %s/>' % _ir_attrs(
        id=control_id, class_='cn-input', value=current, placeholder=placeholder, data_cn_bind=name, data_cn_type='text')
    return _ir_label(label, control_id, body)


def textarea(name, value='', label=None, rows=4, placeholder=None):
    """A multi-line text box."""
    current = _ir_default(name, value)
    control_id = 'cn-' + name
    body = '<textarea %s>%s</textarea>' % (_ir_attrs(
        id=control_id, class_='cn-input', rows=rows, placeholder=placeholder, data_cn_bind=name, data_cn_type='text'), esc(current))
    return _ir_label(label, control_id, body)


def _ir_options(options):
    if options is None:
        return []
    if isinstance(options, dict):
        return [(k, v) for k, v in options.items()]
    if hasattr(options, 'tolist'):
        options = options.tolist()
    result = []
    for option in options:
        if isinstance(option, (list, tuple)) and len(option) == 2:
            result.append((option[0], option[1]))
        else:
            result.append((option, option))
    return result


def _ir_option_type(pairs):
    values = [v for v, _ in pairs]
    if values and all(isinstance(v, bool) for v in values):
        return 'bool'
    if values and all(isinstance(v, int) and not isinstance(v, bool) for v in values):
        return 'int'
    if values and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
        return 'number'
    return 'text'


def select(name, options, value=None, label=None):
    """A combo box. Options are values, (value, caption) pairs or a {value: caption} dictionary."""
    pairs = _ir_options(options)
    current = _ir_default(name, value if value is not None else (pairs[0][0] if pairs else None))
    control_id = 'cn-' + name
    items = ''.join('<option value="%s"%s>%s</option>' % (esc(v), ' selected' if v == current else '', esc(c)) for v, c in pairs)
    body = '<select %s>%s</select>' % (_ir_attrs(
        id=control_id, class_='cn-input', data_cn_bind=name, data_cn_type=_ir_option_type(pairs)), items)
    return _ir_label(label, control_id, body)


def multiselect(name, options, value=None, label=None, size=5):
    """A list in which several options may be chosen; the state value is a list."""
    pairs = _ir_options(options)
    current = _ir_default(name, list(value or []))
    control_id = 'cn-' + name
    items = ''.join('<option value="%s"%s>%s</option>' % (esc(v), ' selected' if v in (current or []) else '', esc(c)) for v, c in pairs)
    body = '<select multiple %s>%s</select>' % (_ir_attrs(
        id=control_id, class_='cn-input', size=size, data_cn_bind=name, data_cn_type='multi:' + _ir_option_type(pairs)), items)
    return _ir_label(label, control_id, body)


def radio(name, options, value=None, label=None, inline=True):
    """A group of radio buttons."""
    pairs = _ir_options(options)
    current = _ir_default(name, value if value is not None else (pairs[0][0] if pairs else None))
    control_id = 'cn-' + name
    kind = _ir_option_type(pairs)
    items = ''.join('<label class="cn-choice"><input type="radio" name="%s" value="%s"%s/> %s</label>'
                    % (control_id, esc(v), ' checked' if v == current else '', esc(c)) for v, c in pairs)
    body = '<div %s>%s</div>' % (_ir_attrs(id=control_id, class_='cn-radio' + (' cn-inline' if inline else ''),
                                           data_cn_bind=name, data_cn_type=kind), items)
    return _ir_label(label, control_id, body)


def checkbox(name, label='', value=False):
    """A check box; the state value is True or False."""
    current = bool(_ir_default(name, bool(value)))
    control_id = 'cn-' + name
    return Html('<label class="cn-choice cn-field"><input type="checkbox" %s/> %s</label>' % (_ir_attrs(
        id=control_id, checked=current, data_cn_bind=name, data_cn_type='bool'), esc(label)))


def toggle(name, label='', value=False):
    """An on/off switch; the state value is True or False."""
    current = bool(_ir_default(name, bool(value)))
    control_id = 'cn-' + name
    return Html('<label class="cn-toggle cn-field"><input type="checkbox" %s/><span class="cn-toggle-track"></span> %s</label>' % (_ir_attrs(
        id=control_id, checked=current, data_cn_bind=name, data_cn_type='bool'), esc(label)))


def date_input(name, value=None, label=None):
    """A date picker; the state value is an ISO date string ('2026-10-05')."""
    if value is not None and hasattr(value, 'isoformat'):
        value = value.isoformat()[:10]
    current = _ir_default(name, value or '')
    control_id = 'cn-' + name
    body = '<input type="date" %s/>' % _ir_attrs(id=control_id, class_='cn-input', value=current, data_cn_bind=name, data_cn_type='text')
    return _ir_label(label, control_id, body)


def color_input(name, value='#3366cc', label=None):
    """A colour picker; the state value is '#rrggbb'."""
    current = _ir_default(name, value)
    control_id = 'cn-' + name
    body = '<input type="color" %s/>' % _ir_attrs(id=control_id, class_='cn-color', value=current, data_cn_bind=name, data_cn_type='text')
    return _ir_label(label, control_id, body)


def button(label, action=None, call=None, kind='primary', confirm=None, disabled=False):
    """A button. action= fires one of the report's actions (an output of the block); call= runs a
    method of the report and renders the page again."""
    return Html('<button type="button" %s>%s</button>' % (_ir_attrs(
        class_='cn-button cn-' + kind, data_cn_action=action, data_cn_call=call, data_cn_confirm=confirm,
        disabled=bool(disabled)), esc(label)))


# ── Displays ──────────────────────────────────────────────────────────────────

def table(rows=None, columns=None, page_size=20, height=None, sortable=True, filter=True, select=None,
          formats=None, max_rows=20000, id=None):
    """A table with sorting, filtering and pages. select= names a state value that receives the
    clicked row as a dictionary."""
    headers, cells = _ir_table(_ir_data(rows), columns)
    total = len(cells)
    cells = cells[:max_rows] if max_rows else cells
    if select:
        _ir_default(select, None)
    spec = {
        'columns': headers, 'rows': cells, 'total': total, 'pageSize': page_size,
        'sortable': sortable, 'filter': filter, 'select': select, 'formats': formats or {},
    }
    style = 'max-height:%dpx' % height if height else None
    return Html('<div %s><script type="application/json">%s</script></div>' % (_ir_attrs(
        id=id or _ir_next_id('table'), class_='cn-table', data_cn_table='1', data_cn_opaque='1', style=style),
        _ir_json_block(spec)))


_IR_PALETTE = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099', '#0099c6', '#dd4477', '#66aa00', '#b82e2e', '#316395']


def _ir_series(data, keys):
    if keys is None:
        return []
    if isinstance(keys, str):
        return [(keys, column(data, keys))]
    keys = keys.tolist() if hasattr(keys, 'tolist') else list(keys)
    if keys and all(isinstance(k, str) for k in keys) and data is not None:
        return [(k, column(data, k)) for k in keys]
    if keys and all(isinstance(k, (list, tuple)) or hasattr(k, 'tolist') for k in keys):
        return [('Series %d' % (i + 1), column(None, k)) for i, k in enumerate(keys)]
    return [('', keys)]


def chart(kind='line', data=None, x=None, y=None, labels=None, values=None, z=None, title='', height=360,
          colors=None, x_title=None, y_title=None, legend=True, stacked=False, size=None, text=None,
          min=None, max=None, layout=None, id=None, **trace):
    """A chart drawn with Plotly. kind: line, bar, barh, area, scatter, bubble, pie, donut,
    histogram, box, violin, heatmap, funnel, waterfall, radar, treemap, sunburst, gauge,
    indicator, candlestick. x/y/labels/values/z take column names of data or sequences; y may be
    a list of column names to draw several series."""
    data = _ir_data(data)
    kind = (kind or 'line').lower()
    palette = list(colors) if colors else _IR_PALETTE
    traces = []

    if kind in ('pie', 'donut', 'funnel', 'treemap', 'sunburst', 'funnelarea'):
        names = column(data, labels if labels is not None else x)
        amounts = column(data, values if values is not None else y)
        if kind in ('pie', 'donut'):
            t = {'type': 'pie', 'labels': names, 'values': amounts, 'marker': {'colors': palette}, 'sort': False}
            if kind == 'donut':
                t['hole'] = 0.5
        elif kind == 'funnel':
            t = {'type': 'funnel', 'y': names, 'x': amounts, 'marker': {'color': palette[0]}}
        else:
            t = {'type': kind, 'labels': names, 'values': amounts}
            parents = trace.pop('parents', None)
            t['parents'] = column(data, parents) if parents is not None else [''] * len(names or [])
        traces.append(t)
    elif kind in ('histogram',):
        for i, (name, series) in enumerate(_ir_series(data, x if x is not None else y)):
            traces.append({'type': 'histogram', 'x': series, 'name': name, 'marker': {'color': palette[i % len(palette)]}})
    elif kind in ('box', 'violin'):
        for i, (name, series) in enumerate(_ir_series(data, y if y is not None else x)):
            traces.append({'type': kind, 'y': series, 'name': name, 'marker': {'color': palette[i % len(palette)]}})
    elif kind == 'heatmap':
        matrix = z
        if isinstance(matrix, str):
            matrix = column(data, matrix)
        if matrix is None and data is not None:
            matrix = data.values.tolist() if hasattr(data, 'values') and hasattr(data, 'columns') else data
        t = {'type': 'heatmap', 'z': _ir_plain(matrix), 'colorscale': trace.pop('colorscale', 'RdYlGn')}
        if x is not None:
            t['x'] = column(data, x) if isinstance(x, str) else list(x)
        elif hasattr(data, 'columns'):
            t['x'] = [str(c) for c in data.columns]
        if y is not None:
            t['y'] = column(data, y) if isinstance(y, str) else list(y)
        traces.append(t)
    elif kind == 'radar':
        theta = column(data, labels if labels is not None else x)
        for i, (name, series) in enumerate(_ir_series(data, values if values is not None else y)):
            traces.append({'type': 'scatterpolar', 'r': series + series[:1], 'theta': theta + theta[:1], 'fill': 'toself',
                           'name': name, 'line': {'color': palette[i % len(palette)]}})
    elif kind in ('gauge', 'indicator'):
        amount = values if values is not None else y
        amount = column(data, amount)[-1] if isinstance(amount, str) else amount
        t = {'type': 'indicator', 'value': amount, 'title': {'text': title}}
        if kind == 'gauge':
            low = 0 if min is None else min
            high = 100 if max is None else max
            t['mode'] = 'gauge+number'
            t['gauge'] = {'axis': {'range': [low, high]}, 'bar': {'color': palette[0]}}
        else:
            t['mode'] = 'number'
        traces.append(t)
        title = ''
    elif kind == 'candlestick':
        t = {'type': 'candlestick', 'x': column(data, x)}
        for part in ('open', 'high', 'low', 'close'):
            t[part] = column(data, trace.pop(part, part))
        traces.append(t)
    elif kind == 'waterfall':
        traces.append({'type': 'waterfall', 'x': column(data, x), 'y': column(data, y)})
    else:
        xs = column(data, x)
        for i, (name, series) in enumerate(_ir_series(data, y)):
            color = palette[i % len(palette)]
            if kind in ('bar', 'barh', 'stacked_bar'):
                t = {'type': 'bar', 'name': name, 'marker': {'color': color}}
                if kind == 'barh':
                    t.update({'orientation': 'h', 'x': series, 'y': xs})
                else:
                    t.update({'x': xs, 'y': series})
            elif kind in ('scatter', 'bubble'):
                t = {'type': 'scatter', 'mode': 'markers', 'x': xs, 'y': series, 'name': name, 'marker': {'color': color}}
                if size is not None:
                    sizes = column(data, size)
                    # min and max are parameters here, so the builtin is reached by another name.
                    top = float(_ir_builtin_max(sizes) if sizes else 1.0) or 1.0
                    t['marker']['size'] = [6 + 40 * float(s) / top for s in sizes]
            else:
                t = {'type': 'scatter', 'mode': 'lines+markers' if kind == 'line' else 'lines', 'x': xs, 'y': series,
                     'name': name, 'line': {'color': color}}
                if kind == 'area':
                    t['fill'] = 'tonexty' if stacked and i else 'tozeroy'
                    if stacked:
                        t['stackgroup'] = 'one'
            if text is not None:
                t['text'] = column(data, text)
            traces.append(t)

    for t in traces:
        t.update(trace)
    spec_layout = {
        'title': {'text': title} if title else None,
        'height': height,
        'margin': {'l': 50, 'r': 20, 't': 50 if title else 20, 'b': 40},
        'showlegend': bool(legend) and len(traces) > 1 or (legend and kind in ('pie', 'donut')),
        'barmode': 'stack' if stacked or kind == 'stacked_bar' else 'group',
        'xaxis': {'title': {'text': x_title}} if x_title else {},
        'yaxis': {'title': {'text': y_title}} if y_title else {},
        'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',
    }
    if layout:
        spec_layout.update(layout)
    return plotly({'data': traces, 'layout': {k: v for k, v in spec_layout.items() if v is not None}}, height=height, id=id)


def _ir_builtin_max(values):
    import builtins
    return builtins.max(values)


def plotly(figure, height=None, id=None, config=None):
    """Any Plotly figure: a plotly.graph_objects Figure or a {'data': [...], 'layout': {...}} dictionary."""
    spec = figure.to_plotly_json() if hasattr(figure, 'to_plotly_json') else dict(figure)
    spec.setdefault('layout', {})
    if height:
        spec['layout'].setdefault('height', height)
    spec['config'] = dict({'displaylogo': False, 'responsive': True}, **(config or {}))
    box_height = spec['layout'].get('height') or 360
    return Html('<div %s><script type="application/json">%s</script></div>' % (_ir_attrs(
        id=id or _ir_next_id('chart'), class_='cn-chart', data_cn_chart='1', data_cn_opaque='1',
        style='min-height:%dpx' % box_height), _ir_json_block(spec)))


def figure(fig, width=None, dpi=110):
    """A matplotlib figure, as a picture."""
    buffer = _ir_io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=dpi)
    try:
        import matplotlib.pyplot as plt
        plt.close(fig)
    except Exception:
        pass
    return image(buffer.getvalue(), width=width)


def image(source, width=None, alt=''):
    """A picture: bytes, a file path, or a URL."""
    if isinstance(source, (bytes, bytearray)):
        kind = 'jpeg' if bytes(source[:3]) == b'\xff\xd8\xff' else 'png'
        src = 'data:image/%s;base64,%s' % (kind, _ir_base64.b64encode(bytes(source)).decode('ascii'))
    elif isinstance(source, str) and _ir_os.path.isfile(source):
        extension = _ir_os.path.splitext(source)[1].lower().lstrip('.') or 'png'
        mime = {'jpg': 'jpeg', 'svg': 'svg+xml'}.get(extension, extension)
        with open(source, 'rb') as handle:
            src = 'data:image/%s;base64,%s' % (mime, _ir_base64.b64encode(handle.read()).decode('ascii'))
    else:
        src = str(source)
    style = 'width:%s' % (width if isinstance(width, str) else '%dpx' % width) if width else None
    return Html('<img %s/>' % _ir_attrs(class_='cn-image', src=src, alt=alt, style=style))


_IR_DEFAULT_SCALE = ['#d73027', '#fc8d59', '#fee08b', '#91cf60', '#1a9850']


def color_bar(value, min=0, max=100, colors=None, label=None, show_value=True, format=None, height=14, ticks=True):
    """A colour scale with a marker at the value — red to green by default."""
    scale = list(colors) if colors else _IR_DEFAULT_SCALE
    try:
        position = (float(value) - float(min)) / (float(max) - float(min)) * 100.0
    except (TypeError, ValueError, ZeroDivisionError):
        position = 0.0
    position = 0.0 if position != position else position
    position = 0.0 if position < 0 else 100.0 if position > 100 else position
    gradient = 'linear-gradient(to right, %s)' % ', '.join(scale)
    caption = '<div class="cn-label">%s%s</div>' % (
        esc(label or ''), (' <b>%s</b>' % esc(fmt(value, format) if format else _ir_number(float(value)) if isinstance(value, (int, float)) else value)) if show_value else '')
    marks = ('<div class="cn-colorbar-ticks"><span>%s</span><span>%s</span></div>' % (esc(min), esc(max))) if ticks else ''
    return Html('<div class="cn-colorbar cn-field">%s<div class="cn-colorbar-track" style="height:%dpx;background:%s">'
                '<div class="cn-colorbar-marker" style="left:%.2f%%"></div></div>%s</div>'
                % (caption, height, gradient, position, marks))


def progress(value, max=100, label=None, color=None, format=None):
    """A progress bar."""
    try:
        share = float(value) / float(max) * 100.0
    except (TypeError, ValueError, ZeroDivisionError):
        share = 0.0
    share = 0.0 if share < 0 else 100.0 if share > 100 else share
    style = 'width:%.2f%%%s' % (share, ';background:%s' % color if color else '')
    caption = '<div class="cn-label">%s <b>%s</b></div>' % (esc(label or ''), esc(fmt(value, format) if format else '%.0f%%' % share))
    return Html('<div class="cn-progress cn-field">%s<div class="cn-progress-track"><div class="cn-progress-fill" style="%s"></div></div></div>'
                % (caption, style))


def kpi(label, value, delta=None, format=None, delta_format=None, good='up', color=None):
    """A headline figure with an optional change beside it."""
    shown = fmt(value, format) if format else (_ir_number(value) if isinstance(value, float) else value)
    change = ''
    if delta is not None:
        try:
            positive = float(delta) >= 0
        except (TypeError, ValueError):
            positive = True
        tone = 'cn-good' if positive == (good == 'up') else 'cn-bad'
        arrow = '▲' if positive else '▼'
        change = '<div class="cn-kpi-delta %s">%s %s</div>' % (tone, arrow, esc(fmt(delta, delta_format) if delta_format else delta))
    style = ' style="border-top-color:%s"' % esc(color) if color else ''
    return Html('<div class="cn-kpi"%s><div class="cn-kpi-label">%s</div><div class="cn-kpi-value">%s</div>%s</div>'
                % (style, esc(label), esc(shown), change))


def badge(text, color='#3366cc'):
    """A small coloured label."""
    return Html('<span class="cn-badge" style="background:%s">%s</span>' % (esc(color), esc(text)))
