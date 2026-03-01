"""Payroll report generator — needs refactoring."""


def generate_report(data):
    """Generate a payroll report. This function does too much — refactor it!"""
    result_employees = []
    total = 0

    for record in data:
        # Validation (inline)
        if not isinstance(record, dict):
            continue
        if "name" not in record or "hours" not in record or "rate" not in record:
            continue
        if not isinstance(record["name"], str) or not record["name"]:
            continue
        try:
            hours = float(record["hours"])
            rate = float(record["rate"])
        except (TypeError, ValueError):
            continue
        if hours < 0 or rate <= 0:
            continue

        # Calculate pay (inline)
        if hours > 40:
            regular = 40 * rate
            overtime = (hours - 40) * rate * 1.5
            pay = regular + overtime
        else:
            pay = hours * rate

        # Format currency (inline)
        pay_str = "${:,.2f}".format(pay)

        total += pay
        result_employees.append({
            "name": record["name"],
            "hours": hours,
            "rate": rate,
            "pay": pay,
            "formatted_pay": pay_str,
        })

    total_str = "${:,.2f}".format(total)

    return {
        "employees": result_employees,
        "total": total_str,
    }
