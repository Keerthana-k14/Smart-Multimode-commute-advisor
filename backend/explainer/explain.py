def build_explanation(best_mode: str, times: dict, time_of_day: str, congestion: str) -> str:
    mode = best_mode.replace("_time", "")
    best_time  = times[f'{mode}_time']
    worst_time = max(times.values())
    saved      = round(worst_time - best_time, 1)

    lines = []

    # Congestion context
    if congestion == "high":
        lines.append("Heavy traffic congestion detected on road routes.")
    elif congestion == "medium":
        lines.append("Moderate traffic on road routes.")

    # Peak hour context
    if time_of_day == "evening":
        lines.append("Evening peak hours — road traffic is at its worst.")
    elif time_of_day == "morning":
        lines.append("Morning rush hour detected.")

    # Recommendation reason
    if mode == "metro":
        lines.append(f"Metro is unaffected by road congestion and saves {saved} min vs the slowest option.")
    elif mode == "car":
        lines.append(f"Roads are clear enough that car is the fastest, saving {saved} min.")
    elif mode == "bus":
        lines.append(f"Bus is the best option here, saving {saved} min vs other modes.")

    # Times breakdown
    lines.append(
        f"Estimated times → Car: {times['car_time']} min | "
        f"Metro: {times['metro_time']} min | Bus: {times['bus_time']} min."
    )

    return " ".join(lines)