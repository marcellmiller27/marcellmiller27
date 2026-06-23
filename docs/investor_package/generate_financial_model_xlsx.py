from pathlib import Path

import xlsxwriter

OUT = Path(__file__).resolve().parent
WORKBOOK_PATH = OUT / "JOHN_HENRY_INVESTMENTS_FINANCIAL_MODEL.xlsx"


def money(workbook):
    return workbook.add_format({"num_format": "$#,##0", "border": 1})


def number(workbook):
    return workbook.add_format({"num_format": "#,##0", "border": 1})


def percent(workbook):
    return workbook.add_format({"num_format": "0.0%", "border": 1})


def header(workbook):
    return workbook.add_format({"bold": True, "font_color": "white", "bg_color": "#0B1B2A", "border": 1})


def title(workbook):
    return workbook.add_format({"bold": True, "font_size": 16, "font_color": "#0B1B2A"})


def write_table(ws, workbook, start_row, start_col, headers, rows, formats=None):
    hdr = header(workbook)
    for c, value in enumerate(headers):
        ws.write(start_row, start_col + c, value, hdr)
    for r, row in enumerate(rows, start_row + 1):
        for c, value in enumerate(row):
            fmt = formats[c] if formats else None
            ws.write(r, start_col + c, value, fmt)


def build_workbook() -> None:
    workbook = xlsxwriter.Workbook(WORKBOOK_PATH)
    fmt_money = money(workbook)
    fmt_number = number(workbook)
    fmt_percent = percent(workbook)
    fmt_title = title(workbook)

    years = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    users = [1000, 5000, 15000, 50000, 100000]
    revenue = [1336440, 6682200, 20046600, 66822000, 133644000]
    platform_ops = [120000, 480000, 1200000, 4800000, 11400000]
    staffing = [960000, 2100000, 4800000, 18000000, 45600000]
    legal = [84000, 180000, 600000, 1800000, 5400000]
    marketing = [180000, 750000, 2250000, 8000000, 14000000]
    processing = [40093, 200466, 601398, 2004660, 4009320]
    opex = [1384093, 3710466, 9451398, 34604660, 80409320]
    ebitda = [-47653, 2971734, 10595202, 32217340, 53234680]
    fcf = [-141204, 1906645, 7100592, 21175091, 34036757]

    ws = workbook.add_worksheet("Summary")
    ws.write("A1", "John Henry Investments Financial Model", fmt_title)
    write_table(
        ws,
        workbook,
        2,
        0,
        ["Metric", *years],
        [
            ["Users", *users],
            ["Revenue", *revenue],
            ["Total operating expenses", *opex],
            ["EBITDA", *ebitda],
            ["Free cash flow", *fcf],
        ],
        [None, fmt_number, fmt_number, fmt_number, fmt_number, fmt_number],
    )
    ws.set_column("A:A", 28)
    ws.set_column("B:F", 16)

    chart = workbook.add_chart({"type": "column"})
    chart.add_series({"name": "Revenue", "categories": "=Summary!$B$3:$F$3", "values": "=Summary!$B$4:$F$4"})
    chart.set_title({"name": "Revenue Projection"})
    chart.set_y_axis({"name": "USD"})
    ws.insert_chart("A10", chart, {"x_scale": 1.35, "y_scale": 1.15})

    chart2 = workbook.add_chart({"type": "line"})
    chart2.add_series({"name": "EBITDA", "categories": "=Summary!$B$3:$F$3", "values": "=Summary!$B$6:$F$6"})
    chart2.set_title({"name": "EBITDA Projection"})
    chart2.set_y_axis({"name": "USD"})
    ws.insert_chart("H10", chart2, {"x_scale": 1.25, "y_scale": 1.15})

    ws2 = workbook.add_worksheet("Operating Model")
    write_table(
        ws2,
        workbook,
        0,
        0,
        [
            "Year",
            "Users",
            "Revenue",
            "Platform ops",
            "Staffing/pro services",
            "Legal/compliance",
            "Marketing",
            "Payment processing",
            "Total opex",
            "EBITDA",
            "EBITDA margin",
        ],
        [
            [years[i], users[i], revenue[i], platform_ops[i], staffing[i], legal[i], marketing[i], processing[i], opex[i], ebitda[i], ebitda[i] / revenue[i]]
            for i in range(5)
        ],
        [None, fmt_number, fmt_money, fmt_money, fmt_money, fmt_money, fmt_money, fmt_money, fmt_money, fmt_money, fmt_percent],
    )
    ws2.set_column("A:K", 18)

    ws3 = workbook.add_worksheet("DCF")
    dcf_rows = [
        ["Discount rate", 0.18],
        ["Terminal growth", 0.03],
        ["Terminal value", 233719066],
        ["PV terminal value", 102160758],
        ["Estimated enterprise value", 133531712],
    ]
    write_table(ws3, workbook, 0, 0, ["Metric", "Value"], dcf_rows, [None, fmt_money])
    write_table(
        ws3,
        workbook,
        8,
        0,
        ["Year", "Revenue", "EBITDA", "Free cash flow"],
        [[years[i], revenue[i], ebitda[i], fcf[i]] for i in range(5)],
        [None, fmt_money, fmt_money, fmt_money],
    )
    ws3.set_column("A:D", 22)

    ws4 = workbook.add_worksheet("Marketing")
    new_users = [1000, 4000, 10000, 35000, 50000]
    cac = [180, 187.5, 225, 228.57, 280]
    write_table(
        ws4,
        workbook,
        0,
        0,
        ["Year", "Marketing spend", "New users", "Blended CAC"],
        [[years[i], marketing[i], new_users[i], cac[i]] for i in range(5)],
        [None, fmt_money, fmt_number, fmt_money],
    )
    ws4.set_column("A:D", 18)

    ws5 = workbook.add_worksheet("Personnel")
    headcount_low = [3, 8, 20, 75, 150]
    headcount_high = [7, 15, 45, 160, 350]
    write_table(
        ws5,
        workbook,
        0,
        0,
        ["Year", "Headcount low", "Headcount high", "Staffing/pro services"],
        [[years[i], headcount_low[i], headcount_high[i], staffing[i]] for i in range(5)],
        [None, fmt_number, fmt_number, fmt_money],
    )
    ws5.set_column("A:D", 22)

    workbook.close()
    print(f"Generated {WORKBOOK_PATH}")


if __name__ == "__main__":
    build_workbook()
