def process_employees(employees):
    """Process employee records and return summary.

    Takes a list of employee dicts with keys: name, department, salary, years.
    Returns a dict with department summaries.
    """
    result = {}

    for emp in employees:
        dept = emp["department"]
        if dept not in result:
            result[dept] = {
                "count": 0,
                "total_salary": 0,
                "avg_salary": 0,
                "senior_count": 0,
                "junior_count": 0,
            }

        result[dept]["count"] = result[dept]["count"] + 1
        result[dept]["total_salary"] = result[dept]["total_salary"] + emp["salary"]
        result[dept]["avg_salary"] = result[dept]["total_salary"] / result[dept]["count"]

        if emp["years"] >= 5:
            result[dept]["senior_count"] = result[dept]["senior_count"] + 1

        if emp["years"] < 5:
            result[dept]["junior_count"] = result[dept]["junior_count"] + 1

    for dept in result:
        result[dept]["avg_salary"] = result[dept]["total_salary"] / result[dept]["count"]

    return result
