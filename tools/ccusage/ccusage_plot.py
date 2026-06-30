#!/usr/bin/env python3
"""
Visualize ccusage --json output.

Usage:
    npx ccusage --json | python3 ccusage_plot.py
    npx ccusage --json | python3 ccusage_plot.py --output usage.png
    npx ccusage --json | python3 ccusage_plot.py --cost-only
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ---------------------------------------------------------------------------
# Provider detection
# ---------------------------------------------------------------------------

def infer_provider(model_name: str) -> str:
    if model_name.startswith("claude"):
        return "Claude"
    if model_name.startswith(("gpt", "o1", "o3", "o4", "codex")):
        return "OpenAI"
    if model_name.startswith("gemini"):
        return "Gemini"
    return "Other"


# ---------------------------------------------------------------------------
# Visual config
# ---------------------------------------------------------------------------

PROVIDER_PALETTE = {
    "Claude":  "#5B8DD9",   # steel blue
    "OpenAI":  "#E07B39",   # burnt orange
    "Gemini":  "#4CAF78",   # teal-green
    "Other":   "#9E9E9E",
}

# Each provider gets its own set of line styles cycling through this list
LINESTYLES = ["-", "--", "-.", ":", (0, (3, 1, 1, 1)), (0, (5, 2))]

STYLE = "seaborn-v0_8-whitegrid"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data(fp):
    data = json.load(fp)
    daily = data["daily"]

    # model -> datetime -> accumulated metrics
    model_days: dict[str, dict[datetime, dict]] = defaultdict(
        lambda: defaultdict(lambda: dict(cost=0.0, input=0, output=0,
                                        cache_read=0, cache_create=0))
    )
    # provider -> datetime -> {actual_tokens, cache_tokens}
    provider_days: dict[str, dict[datetime, dict]] = defaultdict(
        lambda: defaultdict(lambda: dict(actual=0, cache=0))
    )

    for entry in daily:
        dt = datetime.strptime(entry["period"], "%Y-%m-%d")
        for mb in entry.get("modelBreakdowns", []):
            model = mb["modelName"]
            provider = infer_provider(model)

            d = model_days[model][dt]
            d["cost"]         += mb.get("cost", 0.0)
            d["input"]        += mb.get("inputTokens", 0)
            d["output"]       += mb.get("outputTokens", 0)
            d["cache_read"]   += mb.get("cacheReadTokens", 0)
            d["cache_create"] += mb.get("cacheCreationTokens", 0)

            pd = provider_days[provider][dt]
            pd["actual"] += mb.get("inputTokens", 0) + mb.get("outputTokens", 0) + mb.get("cacheCreationTokens", 0)
            pd["cache"]  += mb.get("cacheReadTokens", 0)

    sorted_dates = sorted({dt for m in model_days.values() for dt in m})
    return model_days, provider_days, sorted_dates, data.get("totals", {})


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def short_model_name(model: str, provider: str) -> str:
    """Strip redundant prefix so legend labels stay compact."""
    if provider == "Claude":
        return model.replace("claude-", "")
    if provider == "OpenAI":
        return model.replace("-codex", "").replace("gpt-", "gpt-")
    if provider == "Gemini":
        return model.replace("gemini-", "")
    return model


def plot(model_days, provider_days, sorted_dates, totals, output, cost_only):
    plt.style.use(STYLE)

    # Group models by provider (sorted for determinism)
    models_by_provider: dict[str, list[str]] = defaultdict(list)
    for model in sorted(model_days):
        models_by_provider[infer_provider(model)].append(model)

    n_panels = 1 if cost_only else 2
    fig, axes = plt.subplots(
        n_panels, 1,
        figsize=(14, 9 if not cost_only else 5.5),
        gridspec_kw={"height_ratios": [3, 1.6]} if not cost_only else None,
    )
    if n_panels == 1:
        axes = [axes]

    ax_cost = axes[0]

    # -----------------------------------------------------------------------
    # Panel 1 — daily cost per model
    # -----------------------------------------------------------------------
    style_counter: dict[str, int] = defaultdict(int)

    for provider in sorted(models_by_provider):
        color = PROVIDER_PALETTE.get(provider, "#999999")
        for model in models_by_provider[provider]:
            idx = style_counter[provider]
            style_counter[provider] += 1
            ls = LINESTYLES[idx % len(LINESTYLES)]

            xs = sorted(model_days[model])
            ys = [model_days[model][dt]["cost"] for dt in xs]

            label = f"{provider} · {short_model_name(model, provider)}"
            ax_cost.plot(
                xs, ys,
                linestyle=ls,
                color=color,
                linewidth=1.9,
                marker="o",
                markersize=4.5,
                markeredgewidth=0,
                alpha=0.92,
                label=label,
                zorder=3,
            )

    # Annotations: total cost
    total_cost = totals.get("totalCost", sum(
        v["cost"] for m in model_days.values() for v in m.values()
    ))
    date_range = f"{sorted_dates[0]:%b %d, %Y} – {sorted_dates[-1]:%b %d, %Y}"
    ax_cost.set_title(
        "AI Coding Tool Usage — Daily Cost by Model",
        fontsize=13, fontweight="bold", pad=10,
    )
    ax_cost.text(
        0.99, 0.97,
        f"Total: ${total_cost:,.2f}   ({date_range})",
        transform=ax_cost.transAxes,
        ha="right", va="top",
        fontsize=9, color="#444444",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7, edgecolor="none"),
    )

    ax_cost.set_ylabel("Daily Cost (USD)", fontsize=10)
    ax_cost.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.2f"))
    _format_xaxis(ax_cost, sorted_dates, rotate=cost_only)
    ax_cost.grid(True, axis="y", alpha=0.4, linestyle="--")
    ax_cost.spines["top"].set_visible(False)
    ax_cost.spines["right"].set_visible(False)

    n_models = sum(len(v) for v in models_by_provider.values())
    ax_cost.legend(
        loc="upper left",
        fontsize=8,
        framealpha=0.88,
        ncol=2 if n_models > 7 else 1,
        handlelength=2.4,
        columnspacing=1.0,
    )

    # -----------------------------------------------------------------------
    # Panel 2 — daily tokens by provider (actual vs cache-read)
    # -----------------------------------------------------------------------
    if not cost_only:
        ax_tok = axes[1]
        bar_w = np.timedelta64(16, "h")
        providers_ordered = sorted(provider_days)

        # Two-pass stacking: all actual bars first, then all cache bars above them.
        # A single-pass interleave produces wrong bottoms when providers overlap.
        actual_by_provider = {}
        cache_by_provider  = {}
        for provider in providers_ordered:
            actual_by_provider[provider] = np.array(
                [provider_days[provider].get(dt, {}).get("actual", 0) / 1e6 for dt in sorted_dates]
            )
            cache_by_provider[provider] = np.array(
                [provider_days[provider].get(dt, {}).get("cache", 0) / 1e6 for dt in sorted_dates]
            )

        bottoms = np.zeros(len(sorted_dates))
        for provider in providers_ordered:
            color = PROVIDER_PALETTE.get(provider, "#999999")
            ax_tok.bar(sorted_dates, actual_by_provider[provider], bottom=bottoms,
                       color=color, alpha=0.90, width=bar_w, label=f"{provider} (actual)")
            bottoms += actual_by_provider[provider]

        for provider in providers_ordered:
            color = PROVIDER_PALETTE.get(provider, "#999999")
            ax_tok.bar(sorted_dates, cache_by_provider[provider], bottom=bottoms,
                       color=color, alpha=0.35, width=bar_w, label=f"{provider} (cache read)",
                       hatch="////", edgecolor="none")
            bottoms += cache_by_provider[provider]

        ax_tok.set_ylabel("Tokens / Day (M)", fontsize=10)
        _format_xaxis(ax_tok, sorted_dates, rotate=True)
        ax_tok.grid(True, axis="y", alpha=0.4, linestyle="--")
        ax_tok.spines["top"].set_visible(False)
        ax_tok.spines["right"].set_visible(False)
        ax_tok.set_title("Daily Token Volume by Provider  (solid = actual · hatched = cache read)",
                         fontsize=9.5, pad=6, color="#444444")
        ax_tok.legend(
            loc="upper left", fontsize=7.5, framealpha=0.85,
            ncol=3, handlelength=1.8,
        )

    fig.tight_layout(pad=2.2, h_pad=2.5)

    if output:
        fig.savefig(output, dpi=150, bbox_inches="tight")
        print(f"Saved → {output}", file=sys.stderr)
    else:
        plt.show()


def _format_xaxis(ax, sorted_dates, rotate=True):
    span_days = (sorted_dates[-1] - sorted_dates[0]).days if len(sorted_dates) > 1 else 1
    if span_days > 180:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    elif span_days > 60:
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    else:
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    if rotate:
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right", fontsize=8.5)
    else:
        plt.setp(ax.xaxis.get_majorticklabels(), fontsize=8.5)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Plot ccusage --json output. Pipe JSON on stdin.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example:\n  npx ccusage --json | python3 ccusage_plot.py --output usage.png",
    )
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="Save figure to file (png/pdf/svg) instead of displaying")
    parser.add_argument("--cost-only", action="store_true",
                        help="Omit the token-volume panel")
    args = parser.parse_args()

    if sys.stdin.isatty():
        print("No input — pipe ccusage JSON:  npx ccusage --json | python3 ccusage_plot.py",
              file=sys.stderr)
        sys.exit(1)

    model_days, provider_days, sorted_dates, totals = load_data(sys.stdin)
    plot(model_days, provider_days, sorted_dates, totals, args.output, args.cost_only)


if __name__ == "__main__":
    main()
