def generate_insight(delta_usd):
    if delta_usd > 0:
        return "📈 Cocoa rising → higher cost"
    elif delta_usd < 0:
        return "📉 Cocoa falling → lower cost"
    else:
        return "➖ No price change (weekend / stable)"