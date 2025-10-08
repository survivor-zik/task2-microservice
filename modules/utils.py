async def calculate_totals(request):
    """
    Calculate line totals and grand total for a quote request.
    """
    line_totals = []
    for item in request.items:
        price_per_unit = item.unit_cost * (1 + (item.margin_pct / 100))
        line_total = price_per_unit * item.qty
        line_totals.append(line_total)

    grand_total = sum(line_totals)
    return grand_total,line_totals
